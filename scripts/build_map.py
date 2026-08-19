# -*- coding: utf-8 -*-
"""Build a single-file interactive trip map (index.html) from map_data.json.

Pipeline: read assets/template.html -> inject hotel/days/overview data ->
write a standalone HTML page (Leaflet + CDN tiles) that opens on any phone
browser and can be shared via a link or as a file.

Usage:
    python build_map.py map_data.json [output.html]

Data schema (see references/build-map.md):

    {
      "title": "...", "subtitle": "...", "description": "...",
      "coords": "wgs84" | "gcj02",          # default wgs84; gcj02 = Amap/Baidu raw
      "hotel": {"name": "...", "lat": 0, "lng": 0},
      "info": {"hotel": "...", "flight": "...", "transit": "...", "budget": "..."},
      "pay_summary": [{"title": "...", "text": "...", "warn": true}],
      "days": [
        {"id": 1, "label": "D1", "date": "...", "title": "...", "color": "#ff9500",
         "locations": [
           {"name": "...", "lat": 0, "lng": 0, "type": "spot",
            "time": "16:00", "desc": "...", "budget": "...", "detail": "...",
            "pay": {"alipay": 1, "wechat": 1},       # 1 = yes, 0.5 = maybe
            "xhsKeyword": "...", "dianpingKeyword": "...", "reserve": "..."}
         ]}
      ]
    }

Coordinates must be WGS84 unless "coords": "gcj02" is set; GCJ-02 (the raw
lat/lng Amap/Baidu return) is converted automatically to avoid ~500m drift
on OSM/Leaflet basemaps.
"""
import argparse
import io
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE.parent / "assets" / "template.html"


# ---------- GCJ-02 -> WGS84 ----------
_A = 6378245.0
_EE = 0.00669342162296594323


def _out_of_china(lat, lng):
    return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)


def _transform_lat(x, y):
    ret = (-100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y
           + 0.2 * math.sqrt(abs(x)))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320.0 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return ret


def _transform_lng(x, y):
    ret = (300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y
           + 0.1 * math.sqrt(abs(x)))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return ret


def gcj02_to_wgs84(lat, lng):
    """Convert GCJ-02 (Amap/Baidu-raw) coordinates to WGS84."""
    if _out_of_china(lat, lng):
        return lat, lng
    dlat = _transform_lat(lng - 105.0, lat - 35.0)
    dlng = _transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - _EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((_A * (1 - _EE)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (_A / sqrtmagic * math.cos(radlat) * math.pi)
    return lat - dlat, lng - dlng


# ---------- JS building ----------
def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def js_num(v, default=0):
    try:
        return repr(float(v))
    except (TypeError, ValueError):
        return repr(default)


def convert_coords(lat, lng, mode):
    if mode == "gcj02" and lat and lng:
        lat, lng = gcj02_to_wgs84(lat, lng)
    return round(float(lat), 6), round(float(lng), 6)


def build_hotel(hotel, mode):
    name = js_str(hotel.get("name", ""))
    lat, lng = convert_coords(hotel.get("lat", 0), hotel.get("lng", 0), mode)
    return "const HOTEL = { name: %s, lat: %s, lng: %s };" % (name, js_num(lat), js_num(lng))


def build_locations(locs, mode):
    parts = []
    for l in locs:
        lat, lng = convert_coords(l.get("lat", 0), l.get("lng", 0), mode)
        fields = [
            "name: %s" % js_str(l.get("name", "")),
            "lat: %s" % js_num(lat),
            "lng: %s" % js_num(lng),
            "type: %s" % js_str(l.get("type", "spot")),
            "time: %s" % js_str(l.get("time", "")),
            "desc: %s" % js_str(l.get("desc", "")),
        ]
        for key in ("budget", "detail", "xhs", "xhsKeyword",
                    "dianping", "dianpingKeyword", "reserve", "gmap"):
            v = l.get(key)
            if v:
                fields.append("%s: %s" % (key, js_str(v)))
        if l.get("pay"):
            fields.append("pay: %s" % json.dumps(l["pay"], ensure_ascii=False))
        parts.append("{ " + ", ".join(fields) + " }")
    return parts


def build_days(days, mode):
    lines = ["const DAYS = ["]
    lines.append("  { id: 0, label: '总览', color: '#0071e3', locations: [] },")
    for d in days:
        locs = build_locations(d.get("locations", []), mode)
        joined = (",\n      ".join(locs)) if locs else ""
        lines.append("  {")
        lines.append("    id: %s, label: %s, date: %s, title: %s, color: %s,"
                     % (js_num(d.get("id", 0)),
                        js_str(d.get("label", "")),
                        js_str(d.get("date", "")),
                        js_str(d.get("title", "")),
                        js_str(d.get("color", "#0071e3"))))
        if locs:
            lines.append("    locations: [\n      %s\n    ]" % joined)
        else:
            lines.append("    locations: []")
        lines.append("  },")
    lines.append("];")
    return "\n".join(lines)


def build_overview(data):
    def esc(s):
        return (s or "").replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    title = esc(data.get("title", "行程地图"))
    subtitle = esc(data.get("subtitle", ""))
    info = data.get("info", {})
    hotel_v = esc(info.get("hotel", ""))
    flight_v = esc(info.get("flight", ""))
    transit_v = esc(info.get("transit", ""))
    budget_v = esc(info.get("budget", ""))

    pay_cards = []
    for p in data.get("pay_summary", []):
        cls = "warn" if p.get("warn") else "ok-text"
        pay_cards.append(
            '<div class="pay-summary"><h4>%s</h4><div class="%s">%s</div></div>'
            % (esc(p.get("title", "")), cls, esc(p.get("text", ""))))
    pay_html = "\n".join(pay_cards)

    day_list_expr = ("${DAYS.slice(1).map(d=>`<div class=\"card\" onclick=\"go(${d.id})\">"
                     "<div class=\"name\"><span class=\"dot\" style=\"background:${d.color}\"></span>"
                     "${d.label} · ${d.title}</div><div class=\"desc\">${d.date}</div></div>`).join('')}")

    return (
        "function overviewContent() {\n"
        "  return `\n"
        '<div class="hero"><h1>%s</h1><p class="subtitle">%s</p></div>\n'
        '<div class="info-grid">\n'
        '  <div class="info-card"><div class="label">酒店</div><div class="value">%s</div></div>\n'
        '  <div class="info-card"><div class="label">航班/进出</div><div class="value">%s</div></div>\n'
        '  <div class="info-card"><div class="label">交通</div><div class="value">%s</div></div>\n'
        '  <div class="info-card"><div class="label">预估费用</div><div class="value">%s</div></div>\n'
        "</div>\n"
        '<div class="section-head">行程概览</div>\n'
        '<div class="day-list">%s</div>\n'
        '<div class="section-head">支付提醒</div>\n'
        "%s\n"
        '<div class="section-head">图例</div>\n'
        '<div class="legend">\n'
        '  <div class="legend-item"><div class="legend-dot" style="background:var(--tint-red)"></div>餐厅</div>\n'
        '  <div class="legend-item"><div class="legend-dot" style="background:var(--tint-blue)"></div>景点</div>\n'
        '  <div class="legend-item"><div class="legend-dot" style="background:var(--tint-purple)"></div>饮品</div>\n'
        '  <div class="legend-item"><div class="legend-dot" style="background:var(--tint-orange)"></div>酒店</div>\n'
        "</div>`;\n"
        "}"
        % (title, subtitle, hotel_v, flight_v, transit_v, budget_v,
           day_list_expr, pay_html)
    )


# ---------- template injection ----------
DATA_RE = re.compile(r"const HOTEL = \{.*?\n\];", re.DOTALL)
OVERVIEW_RE = re.compile(r"function overviewContent\(\) \{.*?\n\}", re.DOTALL)


def inject(template, data):
    title = data.get("title", "行程地图")
    description = data.get("description", "")

    t = template.replace("<title><!-- REPLACE: Trip Title --></title>",
                         "<title>%s</title>" % title.replace("</title>", ""))
    t = t.replace('<meta name="description" content="<!-- REPLACE: Trip Description -->">',
                  '<meta name="description" content="%s">'
                  % description.replace('"', "&quot;"))

    mode = "gcj02" if data.get("coords", "wgs84") == "gcj02" else "wgs84"
    data_js = build_hotel(data.get("hotel", {}), mode) + "\n\n" + \
        build_days(data.get("days", []), mode)
    overview_js = build_overview(data)

    # NOTE: use a callable replacement so re.sub does NOT interpret
    # backslash escapes (\\n etc.) inside the generated JS as control chars.
    t, n1 = DATA_RE.subn(lambda _m: data_js, t, count=1)
    t, n2 = OVERVIEW_RE.subn(lambda _m: overview_js, t, count=1)
    if n1 != 1 or n2 != 1:
        raise RuntimeError("template injection failed (data=%d, overview=%d)" % (n1, n2))
    return t


def main():
    ap = argparse.ArgumentParser(description="Build an interactive trip map HTML.")
    ap.add_argument("map_data", help="path to map_data.json")
    ap.add_argument("output", nargs="?", default="index.html",
                    help="output html path (default: index.html)")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE),
                    help="template html path")
    args = ap.parse_args()

    data_path = Path(args.map_data)
    if not data_path.exists():
        sys.exit("map data not found: %s" % data_path)
    with io.open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    with io.open(args.template, encoding="utf-8") as f:
        template = f.read()

    html = inject(template, data)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    n_days = len(data.get("days", []))
    n_locs = sum(len(d.get("locations", [])) for d in data.get("days", []))
    print("Map written: %s" % out.resolve())
    print("QA ok: %d day(s), %d location(s), coord system = %s"
          % (n_days, n_locs, data.get("coords", "wgs84")))


if __name__ == "__main__":
    main()

---
name: trip-planner
description: 'Plan scenic multi-day domestic trips (China) end-to-end and deliver a detailed, verified travel guide as Markdown + PDF. Use when the user asks for a travel itinerary/攻略 (e.g. 帮我制定北疆旅游攻略, 做个云南行程, 计划一次川西自驾). Workflow: first confirm travel dates and the scenic-spot list (from the user or researched in the browser on 小红书/马蜂窝), source long-haul transport from 12306 or airlines, plan inter-city routes with 高德地图, verify every ticket/reservation with a cited source (never fabricate), cross-reference real hotel prices on Ctrip and Fliggy and restaurant ratings on Dianping and Meituan (at least two platforms; the customer must log in via the in-app browser first, ask for help when blocked by login or CAPTCHA), then export a polished PDF. Also use when the user wants 需要预约/购票的清单, 每天吃什么, 住宿推荐, or 给我个PDF.'
---

# Trip Planner

## Overview

Produce a complete, booking-ready travel guide for a scenic multi-day domestic trip: lock dates and the scenic-spot list first, verify transport (long-haul from 12306/airlines, inter-city with 高德地图), verify every ticket/reservation with a cited source (no fabrication), then verify real accommodation prices (Ctrip) and restaurant ratings (Dianping/Meituan) — the customer must be logged in via the in-app browser first — and finally export a well-formatted Markdown + PDF guide. Only read prices/reviews; never place orders, change bookings, or pay without explicit user consent.

## 信息收集前置条件：多平台交叉参考 + 先让客户登录

- **每次上网取数前先重新打开侧边栏页面**：应用内浏览器（侧边栏）的标签页会在轮次之间被清理，**不要复用上一轮留下的标签**；每次需要取数（查房价、查餐厅、查路线）时，先在侧边栏新建标签页并重新打开目标页面（如携程/大众点评/高德 ditu.amap.com/dir）。若标签失效报错，直接新建标签即可。
- **多平台交叉参考**：住宿至少核对「携程 + 飞猪」两家；餐饮至少核对「大众点评 + 美团」两家，必要时再叠加 Trip.com/携程美食/小红书。不要只信单一平台的数据，冲突时取多数平台一致值并标注各平台来源。
- 携程/飞猪（住宿实测价）和大众点评/美团（餐厅评分、人均）都需要客户登录才能可靠取数。
- 在进入住宿、就餐步骤前，先让客户在**应用内浏览器（侧边栏）**完成对应平台的登录；未登录时先提示客户登录，不要跳过或硬凑数据。
- 大众点评 PC 端未登录基本无法搜索取数；若扫码页显示「二维码已失效」，点击「请点击刷新」再让客户扫。
- **登录/人机验证一律交给客户（硬性要求）**：遇到登录墙、短信验证码、滑块/点选验证、风控验证页（如美团 spider 验证页）或安全拦截时，**立即停下并请客户在侧边栏完成**；AI 不尝试自动破解、不绕过安全页、不反复刷新重试触发风控。客户完成后继续。

## Workflow

### Step 1 — 确定时间与景点清单

- 先和客户确认：**什么时候去**（季节/具体日期范围）、人数与房间数、预算档位、风景偏好。
- 景点来源：客户自己的想法优先；客户没有明确清单时，用浏览器去**小红书/马蜂窝/知乎/抖音**收集攻略，给出候选景点 + 最佳季节 + 路线逻辑，与客户确认后再定。
- 产出：确认后的日期范围 + 景点清单，作为后面所有排期的前提。

### Step 2 — 远程交通（12306 / 航司）

- 跨省/远程交通（飞机、高铁）：从 **12306** 官网/App（铁路时刻与票价）或**各航司**官网/App（航班时刻与票价）获取；可用携程/去哪儿比价，但以官方为准。
- 核对机场名称（注意更名，如 乌鲁木齐地窝堡→天山国际机场、阿勒泰→雪都机场）、航班号、起降时刻。
- 产出：已确认航班/车次表，标注购票提醒与衔接余量。

### Step 3 — 城际与区内交通（高德地图）

- 先在侧边栏重新打开高德网页版 ditu.amap.com/dir（或高德 MCP），再开始查路线；起终点用精确 POI（酒店/餐厅/景区名），不用城市名。
- 自驾/包车/城际移动：用**高德地图**规划路线（里程、预计用时、高速/国道、过路费参考），逐段记录，标记长线日与风险。
- 注意道路通行窗口与车辆限制（如阿禾公路 G681：每日 9:30–15:00 放行、仅限 7 座及以下、免费，出发前 1–3 天在「原行网」小程序确认预约）。
- 景区接驳：查区间车/摆渡车运营时间与末班时间，写进行程时间点。

### Step 4 — 门票与预约（必须有来源，不许瞎编）

- 每一条门票/价格/预约信息都必须注明**来源渠道**（官方小程序/公众号/官网，或 12306/航司/携程/美团/原行网等平台）与**核实日期**。
- 没有查到确切来源的信息一律不写进「已确认」列，标注「待核实」并提示客户去官方渠道确认。
- 常见核实渠道示例：白哈巴边防证「移民局12367/新疆公安微警务」（免费）；赛里木湖自驾「一部手机游赛湖」（限 3000 辆/日）；喀纳斯全域通票「喀纳斯景区」公众号/「原行网」；观鱼台现场分时预约。
- 产出：预约购票清单表——项目 | 是否需预约 | 来源渠道 | 操作步骤 | 时间节点 | 参考价 | 核实日期。

### Step 5 — 住宿（携程 + 飞猪实测价，需登录）

- 先**重新打开侧边栏标签页**并确认客户已登录携程（必要时也登录飞猪），见「信息收集前置条件」。
- 读 `references/verify-hotel-prices.md`，按实际日期/人数拿当日可订含税价；**同一晚在携程和飞猪各查一次并对比价格/是否有房**；每晚至少给 首选 + 备选，注明床型、含早、可否免费取消。
- 金秋/旺季房源紧张，看到可订就提示客户尽快锁房。

### Step 6 — 就餐安排（大众点评 + 美团，需登录）

- 先**重新打开侧边栏标签页**并确认客户已登录大众点评（见「信息收集前置条件」）。
- 读 `references/verify-restaurants.md`，逐店核对评价数/人均/营业时间；**重点店在美团再交叉核对一次**（评分、人均、营业状态），产出每日三餐表——日期 | 餐次 | 推荐店(城市/位置) | 评分参考 | 人均 | 点单建议 | 时间衔接提示，含备选行。

### Step 7 — 天气

- 按目的地与日期范围查天气（温度、降水、风力），写入「天气与穿衣」章节。

### Step 8 — 成文

- 按下方标准章节写 Markdown；所有价格/评分/门票标注来源与核实日期。
- 章节：1 先看结论（可行性速览+路线图） 2 每日详细行程 3 决策点（A/B+建议，已定的标 ✅） 4 预约购票清单（含来源） 5 衔接可行性验证表 6 天气与穿衣 7 住宿汇总（携程实测价+日期） 8 费用预算（人均） 9 行前准备清单 10 风险与备选 11 每日用餐安排表 12 祝语。

### Step 9 — 导出 PDF

- 用自带脚本（优先 Codex 运行时 Python，含 pdfplumber）：

```bash
python scripts/build_pdf.py input.md output.pdf --title "标题"
```

- 脚本完成 Markdown→HTML（scripts/md_to_html.py）→ Edge headless 打印 → 页数质检。交付前用 `pdftoppm`（poppler）渲染 PNG 检查排版无缺陷。交付文件放客户 `outputs/` 目录。

### Step 10 — 交付与跟进

- 交付 `.md` 与 `.pdf`，PDF 用 `:codex-file-citation{path="..." purpose="output"}` 引用一次。
- 提醒客户紧急预订：内段航班、景区住宿、门票。
- 客户已在侧边栏登录过携程/大众点评时直接复用会话；不需要重新登录。

## China domestic-trip facts worth re-verifying each time

- 机场更名会改变购票/预订名称，写攻略前先确认。
- 景区票务逐步搬到小程序/公众号；金秋旺季（如喀纳斯 9.25–10.7）会约满售罄，要推动客户提前订。
- 部分公路有每日通行窗口与车辆限制（阿禾公路 9:30–15:00、≤7座），出发前 1–3 天用官方小程序确认当期政策。
- 边境村边防证免费且可线上办，电子证记得离线保存。
- 景区内餐饮人均比市区贵 ¥10–30，属正常，写进计划里。

## Scripts

- `scripts/build_pdf.py` — Markdown → A4 PDF（Edge headless）+ 页数质检；用 Codex 运行时 Python 运行。
- `scripts/md_to_html.py` — 供 build_pdf.py 调用的转换器，也可单独生成 HTML 预览。

## References（按需阅读）

- `references/verify-hotel-prices.md` — Step 5 时读：携程列表 URL 模板、登录前置、每间酒店需记录什么。
- `references/verify-restaurants.md` — Step 6 时读：大众点评/美团登录（二维码失效刷新）、城市拼音→cityId 提取、搜索 URL 模板、替代数据源。

## Constraints

- 只读价格/评价，绝不代为下单、改单、领券或付款。
- 门票/价格必须带来源与核实日期；查不到就标「待核实」，不许编造。
- 每次上网取数前重新打开侧边栏标签页，不复用已失效的标签；登录/人机验证一律请客户在侧边栏完成，AI 不代解、不绕过、不重试触发风控。
- 关键数据（房价、餐厅评分人均）至少两个平台交叉参考，并标注各平台来源与核实日期。
- 攻略用客户语言（国内默认中文），格式统一，保证能干净导出 PDF。

---
name: trip-planner
description: 'Plan scenic multi-day domestic trips (China) end-to-end and deliver a detailed, verified travel guide as Markdown + PDF. Use when the user asks for a travel itinerary/攻略 (e.g. 帮我制定北疆旅游攻略, 做个云南行程, 计划一次川西自驾). Workflow: first confirm travel dates and the scenic-spot list (from the user or researched in the browser on 小红书/马蜂窝), source long-haul transport from 12306 or airlines, plan inter-city routes with 高德地图, verify every ticket/reservation with a cited source (never fabricate), compare real hotel prices on Ctrip and Fliggy and verify restaurant ratings on Dianping (the customer must log in via the in-app browser first, ask for help when blocked by login or CAPTCHA), then export a polished PDF. Also use when the user wants 需要预约/购票的清单, 每天吃什么, 住宿推荐, or 给我个PDF.'
---

# Trip Planner

## Overview

Produce a complete, booking-ready travel guide for a scenic multi-day domestic trip: lock dates and the scenic-spot list first, verify transport (long-haul from 12306/airlines, inter-city with 高德地图), verify every ticket/reservation with a cited source (no fabrication), then verify real accommodation prices (Ctrip/Fliggy) and restaurant ratings (Dianping) — the customer must be logged in via the in-app browser first — and finally export a well-formatted Markdown + PDF guide. Only read prices/reviews; never place orders, change bookings, or pay without explicit user consent.

## 信息收集前置条件：先让客户登录 + 数据带来源

- **每次上网取数前先重新打开侧边栏页面**：应用内浏览器（侧边栏）的标签页会在轮次之间被清理，**不要复用上一轮留下的标签**；每次需要取数（查房价、查餐厅、查路线）时，先在侧边栏新建标签页并重新打开目标页面（如携程/大众点评/高德 ditu.amap.com/dir）。若标签失效报错，直接新建标签即可。
- **数据来源**：住宿在「携程 + 飞猪」两家比价；餐饮以「大众点评」登录实测为准（**美团网页版不可用，不做美团交叉验证**），必要时叠加 Trip.com/携程美食/小红书作补充参考。所有数据标注平台来源。
- 携程/飞猪（住宿实测价）和大众点评（餐厅评分、人均）都需要客户登录才能可靠取数。
- **登录前置 = 策划第 0 步，而不是行程做完后的补救**：开始任何取数/策划前，先用**应用内浏览器（侧边栏）直接打开各平台页面**（携程 hotels.ctrip.com、大众点评 www.dianping.com/<城市拼音>、高德 ditu.amap.com/dir、需要时飞猪 www.fliggy.com/jiudian/），让用户**一次性全部扫码登录**；未登录时不开始取数，更不要等攻略交付后才补一句「需要登录」。
- 大众点评 PC 端未登录基本无法搜索取数；若扫码页显示「二维码已失效」，点击「请点击刷新」再让客户扫。
- **登录/人机验证一律交给客户（硬性要求）**：遇到登录墙、短信验证码、滑块/点选验证、风控验证页（如平台风控验证页）或安全拦截时，**立即停下并请客户在侧边栏完成**；AI 不尝试自动破解、不绕过安全页、不反复刷新重试触发风控。客户完成后继续。

## Workflow

### Step 0 — 策划前先引导客户登录（硬性前置）

- **顺序要求**：这一步排在「确定时间/景点」之前。动手查路线、查房价、查餐厅或写攻略前，先完成登录准备。
- **直接打开登录页，而不是只发一句「请登录」**：用**应用内浏览器（侧边栏）新建标签页并直接打开**各平台页面，把二维码/登录入口呈现在用户面前——
  - 携程（查房价）：打开 `https://hotels.ctrip.com/`（用户右上角「登录」扫码即可）；
  - 大众点评（查餐厅）：打开 `https://www.dianping.com/<城市拼音>`（如 `wuhan`），右上角「登录」→ 扫码；二维码失效就点「请点击刷新」；
  - 飞猪（需要比价时）：打开 `https://www.fliggy.com/jiudian/`（淘宝账号体系），用户扫码登录；
  - 高德（查路线/公共交通）：打开 `https://ditu.amap.com/dir`（右上角「登录」扫码，与上面几家**一起登录**，一次搞定）。
- 打开后**停下等待**：告诉用户「登录页已打开，请逐一扫码登录，好了告诉我」；不要替用户点登录、不代解验证码、不在用户登录过程中反复刷新或切换页面。
- 客户完成后，把「携程/大众点评/高德（+飞猪）已登录」记入当前任务状态；后续 Step 3/5/6 只复用会话、重新打开标签页，不再要求重新登录。
- 若客户明确不方便登录：先确认能否用公开可查数据（搜索快照/第三方源）推进，并如实标注「待核实」，不得假装已核。

### Step 1 — 确定时间与景点清单

- 先和客户确认：**什么时候去**（季节/具体日期范围）、人数与房间数、预算档位、风景偏好。
- 景点来源：客户自己的想法优先；客户没有明确清单时，用浏览器去**小红书/马蜂窝/知乎/抖音**收集攻略，给出候选景点 + 最佳季节 + 路线逻辑，与客户确认后再定。
- 产出：确认后的日期范围 + 景点清单，作为后面所有排期的前提。
- **场景分流**：客户自带行程/景点清单 → 成文时做「可行性分析/验证」（第 1 章「先看结论·可行性速览」，逐项核对客户计划是否可行）；从零策划 → 不需要可行性分析，第 1 章直接写「行程总览 + 路线图」。

### Step 2 — 远程交通（12306 / 航司）

- 跨省/远程交通（飞机、高铁）：从 **12306** 官网/App（铁路时刻与票价）或**各航司**官网/App（航班时刻与票价）获取；可用携程/去哪儿比价，但以官方为准。
- 核对机场名称（注意更名，如 乌鲁木齐地窝堡→天山国际机场、阿勒泰→雪都机场）、航班号、起降时刻。
- 产出：已确认航班/车次表，标注购票提醒与衔接余量。

### Step 3 — 城际与区内交通（高德地图，含公共交通）

- 先在侧边栏重新打开高德网页版 ditu.amap.com/dir（或高德 MCP），再开始查路线；起终点用精确 POI（酒店/餐厅/景区名），不用城市名。
- 详细操作见 `references/route-and-transit.md`：驾车路线 + **公共交通（公交/地铁/BRT/火车混合）** + 打车参考价。
- 自驾/包车/城际移动：用高德网页版/MCP 实测每段车程（里程、用时、途经、通行窗口如阿禾公路 9:30–15:00、限 7 座）。
- **公共交通**：同一页面切「坐公交」模式，提取时长/里程/步行/票价/线路；城际火车以 12306 时刻票价为准确源；景区区间车以官方时刻表为准（注意末班车）。
- 产出：路线核对表（驾车/公交分列），逐段标注来源与实测日期。

### Step 4 — 门票与预约（必须有来源，不许瞎编）

- 每一条门票/价格/预约信息都必须注明**来源渠道**（官方小程序/公众号/官网，或 12306/航司/携程/美团/原行网等平台）与**核实日期**。
- 没有查到确切来源的信息一律不写进「已确认」列，标注「待核实」并提示客户去官方渠道确认。
- 常见核实渠道示例：白哈巴边防证「移民局12367/新疆公安微警务」（免费）；赛里木湖自驾「一部手机游赛湖」（限 3000 辆/日）；喀纳斯全域通票「喀纳斯景区」公众号/「原行网」；观鱼台现场分时预约。
- 产出：预约购票清单表——项目 | 是否需预约 | 来源渠道 | 操作步骤 | 时间节点 | 参考价 | 核实日期。

### Step 5 — 住宿（携程 + 飞猪实测价，需登录）

- 登录应在 Step 0 完成；此处只**重新打开侧边栏标签页**复用已登录会话（必要时补登飞猪），不要出现「先交付行程、后补登录」的情况。
- 读 `references/verify-hotel-prices.md`，按实际日期/人数拿当日可订含税价；**同一晚在携程和飞猪各查一次并对比价格/是否有房**；每晚至少给 首选 + 备选，注明床型、含早、可否免费取消。
- 金秋/旺季房源紧张，看到可订就提示客户尽快锁房。

### Step 6 — 就餐安排（大众点评，需登录）

- 登录应在 Step 0 完成；此处只**重新打开侧边栏标签页**复用已登录会话，不要出现「先交付行程、后补登录」的情况。
- 读 `references/verify-restaurants.md`，逐店核对评价数/人均/营业时间；以大众点评登录实测为唯一准（**美团网页版不可用，不再做美团交叉核对**），产出每日三餐表——日期 | 餐次 | 推荐店(城市/位置) | 评分参考 | 人均 | 点单建议 | 时间衔接提示，含备选行。

### Step 7 — 天气

- 按目的地与日期范围查天气（温度、降水、风力），写入「天气与穿衣」章节。

### Step 8 — 成文

- 按下方标准章节写 Markdown；所有价格/评分/门票标注来源与核实日期。
- **第 1 章按场景切换**（对应 Step 1 的场景分流）：
  - 客户自带计划/清单 → 第 1 章写「先看结论：可行性速览」，逐项给出 可行 / 需调整 / 不可行 及原因；第 5 章保留「衔接可行性验证表」。
  - 从零策划 → 第 1 章写「行程总览 + 路线图」，不做「可行性分析」句式（计划是新建的，无需“验证”）；第 5 章改为「衔接时间验证表」（核对转场时间是否赶得上即可）。
- 章节：1 先看结论（路线图；仅当客户自带计划时才写「可行性速览」） 2 每日详细行程 3 决策点（A/B+建议，已定的标 ✅） 4 预约购票清单（含来源） 5 衔接时间/可行性验证表 6 天气与穿衣 7 住宿汇总（携程/飞猪实测价+日期） 8 费用预算（人均） 9 行前准备清单 10 风险与备选 11 每日用餐安排表 12 祝语。

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
- 交付时若发现还有本可核实、却因未登录而标成「待核实」的项（说明 Step 0 未落实），先补齐登录核实再交付，而不是把「需要登录」作为事后告知。

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
- `references/verify-restaurants.md` — Step 6 时读：大众点评登录（二维码失效刷新）、城市拼音→cityId 提取、搜索 URL 模板、替代数据源。
- `references/route-and-transit.md` — Step 3 时读：高德网页版驾车+公交查询操作（选择器、模式切换、提取字段）、12306 火车、景区区间车注意点。

## Constraints

- 只读价格/评价，绝不代为下单、改单、领券或付款。
- 门票/价格必须带来源与核实日期；查不到就标「待核实」，不许编造。
- 策划开始前（Step 0）先引导客户登录携程/大众点评（需要时含飞猪），未登录不开始取数；每次上网取数前重新打开侧边栏标签页，不复用已失效的标签；登录/人机验证一律请客户在侧边栏完成，AI 不代解、不绕过、不重试触发风控。
- 关键数据必须带来源与核实日期；住宿价格在携程/飞猪比价，餐厅评分以大众点评登录实测为准（不做美团交叉验证）。
- 攻略用客户语言（国内默认中文），格式统一，保证能干净导出 PDF。

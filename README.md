# 内河航运调度中心

船东、船长和调度员共同编排航次计划、过闸排班与货物周转，按同一份运单完成从装港到卸港的全程跟踪。

这是一个前后端分离的管理平台：前端 Vue 3 + Vite + TypeScript，后端 FastAPI（Python）。
两边各自独立启动，前端 dev server 已关掉自动打开页面，启动后按终端打印的地址手工打开。

## 目录结构

```text
.
├── frontend/                 Vue 3 + Vite + TypeScript 前端
│   ├── src/views/WorkbenchView.vue|tsx  全部模块共享工作台
│   ├── src/data/modules.ts              18个业务模块配置
│   ├── src/api/              统一请求封装
│   └── vite.config.ts        dev server 配置（open: false）
├── backend/                  FastAPI（Python） 后端
│   ├── app/routers/resource.py  通用查询/导出/登记/动作接口
│   ├── app/services/<key>.py    每个模块独立领域逻辑
│   ├── app/services/base.py     共享服务骨架
│   └── app/store.py          内存数据仓库与示例数据
├── .gitignore
└── docker-compose.yml
```

## 启动

### 后端

```bash
cd backend
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./run.sh
```

健康检查：`curl http://127.0.0.1:8000/api/health`

### 前端

```bash
cd frontend
npm ci
npm run dev
```

前端默认监听 `http://127.0.0.1:5173/`，dev server 不会自动打开浏览器，
需要自己访问。`/api` 由 vite 代理到后端 `http://127.0.0.1:8000`。

## 业务模块

| 模块 | 目录 | 业务对象 | 主要字段 |
| --- | --- | --- | --- |
| 船舶登记 | `vessel` | 船舶 | 船名、船舶类型、载重吨位 |
| 船员调配 | `crew` | 船员 | 船员姓名、适任证书、在船职务 |
| 航线编排 | `route` | 航线 | 起点港、终点港、航程公里 |
| 航次计划 | `voyage` | 航次 | 航次编号、计划开航、预计到达 |
| 过闸排班 | `lock_booking` | 过闸申请 | 船闸名称、申请通过时间、排队序号 |
| 货物运单 | `cargo_manifest` | 运单 | 货物品名、托运重量、装货港 |
| 配载方案 | `load_plan` | 配载计划 | 装载顺序、舱位分配、稳性校验 |
| 燃油补给 | `fuel_supply` | 加油记录 | 油品标号、加油数量、补给港口 |
| 港口泊位 | `port_berth` | 泊位 | 泊位编号、靠泊能力、当前占用 |
| 水位监测 | `water_gauge` | 水位记录 | 监测站点、当前水位、警戒水位 |
| 气象预警 | `weather_alert` | 预警通知 | 预警类型、影响航段、预警等级 |
| 货损记录 | `cargo_damage` | 货损报告 | 货损品名、损毁程度、发现时间 |
| 船舶维保 | `maintenance` | 维保记录 | 维保项目、维保周期、上次维保日 |
| 规费结算 | `toll_fee` | 规费账单 | 费用类型、计费标准、应缴金额 |
| 航迹追踪 | `ais_track` | 位置报告 | 经度、纬度、航速节 |
| 航行事件 | `incident_log` | 事件日志 | 事件类型、发生航段、涉事船舶 |
| 卸货交接 | `discharge` | 卸货单 | 卸货港口、收货单位、实卸重量 |
| 禁限航管理 | `season_ban` | 禁限航令 | 禁航河段、禁航原因、开始时间 |

## 约定

- 全部模块共享`frontend/src/views/WorkbenchView.vue|tsx`和一套资源路由。
- 每个模块仍保留独立`backend/app/services/<模块>.py`；纯前端保留
  `frontend/src/domain/<模块>.ts`，负责各模块的业务逻辑。
- 列表接口统一返回 `{ items, total, page, size }`，动作接口统一返回 `{ ok, message }`。
- 状态流转只允许在 `app/services` 里改，路由层不做业务判断。


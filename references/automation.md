# 自动化接入说明

这个 skill 采用 **Agent 主导、脚本辅助** 的方式。

## 原则

- `SKILL.md` + `references/` 才是这个 skill 的主体
- `scripts/` 只是可选辅助，不是 skill 的核心
- `scripts/` 只负责稳定的数据获取或骨架生成
- 不把核心分析、综合建议、最终投资判断硬编码进脚本

## 当前脚本职责

### 1. 获取原始数据

```bash
python3 skills/investment-report/scripts/fetch_yahoo_data.py --symbols ^HSI ^GDAXI ^IXIC
```

输出：
- 每个标的的原始历史行情
- 元信息
- 新闻列表

### 2. 生成统一骨架

```bash
python3 skills/investment-report/scripts/generate_report.py --symbols ^HSI ^GDAXI ^IXIC
```

输出：
- 与当前 `report-template.md` 一致的报告骨架
- 不做分析、不做判断、不直接生成最终结论
- 由 Agent 结合数据和规则填充最终内容

### 3. 快速起草空白模板

```bash
python3 skills/investment-report/scripts/report_scaffold.py
```

输出：
- 适合手工补充或快速试写的空白模板

## 推荐工作流

1. Agent 读取 `SKILL.md`、`report-template.md`、`runbook.md`
2. Agent 运行 `fetch_yahoo_data.py` 获取原始数据
3. Agent 自行完成：
   - 指标计算
   - 新闻筛选、信源分级、时间窗口筛选、去重
   - 默认基于摘要做中文转述
   - 把英文标题与英文摘要改写成自然中文财经表述
   - 仅对关键新闻下钻抓全文
   - 明确操作建议与仓位建议
   - 异常提醒、置信度、观察清单
   - 全局策略建议
4. Agent 按模板输出最终报告

## 说明

- `generate_report.py` / `report_scaffold.py` 只是骨架，不代表最终分析已完成
- 最终报告应以 `SKILL.md` 和 `runbook.md` 为准
- 如果后面要支持指定日期、邮件发送，也应保持同样分工：脚本负责准备，Agent 负责判断与输出

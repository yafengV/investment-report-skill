#!/usr/bin/env python3
import argparse
from datetime import datetime

DEFAULT_SYMBOLS = [
    ("上证综合指数", "000001.SS"),
    ("创业板指", "399006.SZ"),
    ("道琼斯工业平均指数", "^DJI"),
    ("纳斯达克综合指数", "^IXIC"),
    ("恒生指数", "^HSI"),
    ("德国DAX指数", "^GDAXI"),
    ("日经225指数", "^N225"),
]


def main():
    p = argparse.ArgumentParser(description="Generate report skeleton only; analysis must be done by Agent via SKILL.md")
    p.add_argument("--report-date", help="report date in Asia/Shanghai, default today")
    p.add_argument("--data-time", help="UTC timestamp string, default now")
    p.add_argument("--symbols", nargs="*", help="symbols to include")
    args = p.parse_args()

    lookup = {code: label for label, code in DEFAULT_SYMBOLS}
    symbols = args.symbols or [code for _, code in DEFAULT_SYMBOLS]
    report_date = args.report_date or datetime.now().strftime("%Y-%m-%d")
    data_time = args.data_time or datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    print(f"投资报告（{report_date}）")
    print(f"报告日期（Asia/Shanghai）：{report_date}")
    print(f"数据时间（UTC）：{data_time}")
    print("价格口径：以“最近收盘日/最近可得收盘价”为基准（若为盘中则会标注；本次按各指数最近收盘日口径解读）")
    print("数据源：由 Agent 基于 skill 流程整合原始数据并完成分析")
    print("覆盖标的：" + "，".join(f"{lookup.get(s, s)}（{s}）" for s in symbols))
    print()
    print("今日结论先行：")
    print("- 市场主判断：")
    print("- 仓位建议：")
    print("- 核心风险：")
    print()

    for symbol in symbols:
        label = lookup.get(symbol, symbol)
        print(f"{label}（{symbol}）")
        print()
        print("前一交易日 / 最新行情概览（最近收盘日：YYYY-MM-DD）")
        print()
        print("最新/收盘：")
        print("昨收：")
        print("涨跌幅：")
        print("近1月波动（年化，近似）：")
        print("近1月最大回撤：")
        print("近1月高/低：")
        print("距离近1月高点/低点：")
        print("技术指标：MA20 / MA60 / RSI / MACD")
        print()
        print("Top3 关联度新闻")
        print()
        for i in range(1, 4):
            print(f"<新闻标题 {i}>")
            print()
            print("时间：")
            print("新闻摘要：")
            print("来源/链接：")
            print("信源等级：")
            print("新闻标签：")
            print("市场与情绪影响：")
            print("策略含义：")
            print()
        print("操作建议：")
        print("仓位建议：")
        print("理由：")
        print("关注：")
        print("风险提示：")
        print("异常提醒：")
        print("置信度：")
        print("备注：")
        print("观察清单：")
        print()

    print("综合交易策略建议")
    print()
    print("当前主线：")
    print("仓位方向：")
    print("核心风险：")
    print("全局异常提醒：")
    print("未来观察点：")
    print()
    print("免责声明：以上内容仅供参考，不构成投资建议，投资有风险，决策需结合自身风险承受能力并谨慎评估。")


if __name__ == "__main__":
    main()

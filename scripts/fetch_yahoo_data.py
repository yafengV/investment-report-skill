#!/usr/bin/env python3
import argparse
import json
import re
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import yfinance as yf

DEFAULT_SYMBOLS = [
    ("上证综合指数", "000001.SS"),
    ("创业板指", "399006.SZ"),
    ("道琼斯工业平均指数", "^DJI"),
    ("纳斯达克综合指数", "^IXIC"),
    ("恒生指数", "^HSI"),
    ("德国DAX指数", "^GDAXI"),
    ("日经225指数", "^N225"),
]


def to_float(x):
    try:
        return float(x)
    except Exception:
        return None


def clean_text(text):
    text = str(text or "—")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or "—"


def normalize_yahoo_news(news_items):
    out = []
    for item in news_items or []:
        content = item.get("content", item) if isinstance(item, dict) else {}
        provider = content.get("provider") or {}
        canonical = content.get("canonicalUrl") or {}
        out.append({
            "title": clean_text(content.get("title") or item.get("title") or "未命名新闻"),
            "summary": clean_text(content.get("summary") or content.get("description") or item.get("summary") or "—"),
            "published_at": content.get("pubDate") or item.get("pubDate") or item.get("published_at") or "—",
            "url": canonical.get("url") or item.get("link") or item.get("url") or "—",
            "source": clean_text(provider.get("displayName") or item.get("publisher") or item.get("source") or "Yahoo Finance"),
        })
    return out


def fetch_symbol(symbol, label):
    t = yf.Ticker(symbol)
    hist = t.history(period="1mo", interval="1d", auto_adjust=False)
    history = []
    if len(hist):
        hist = hist.reset_index()
        for _, row in hist.iterrows():
            dt = row.iloc[0]
            history.append({
                "date": dt.strftime("%Y-%m-%d") if hasattr(dt, "strftime") else str(dt)[:10],
                "open": to_float(row.get("Open")),
                "high": to_float(row.get("High")),
                "low": to_float(row.get("Low")),
                "close": to_float(row.get("Close")),
                "volume": to_float(row.get("Volume")),
            })
    meta = {"longName": label}
    try:
        info = t.info or {}
        meta = {
            "currency": info.get("currency"),
            "exchangeName": info.get("exchange") or info.get("exchangeName"),
            "longName": info.get("longName") or info.get("shortName") or label,
            "market": info.get("market"),
            "timezone": info.get("exchangeTimezoneName") or info.get("timeZoneFullName"),
        }
    except Exception:
        pass
    try:
        news = normalize_yahoo_news(t.news)
    except Exception:
        news = []
    return {
        "symbol": symbol,
        "label": label,
        "meta": meta,
        "history": history,
        "news": news,
    }


def main():
    p = argparse.ArgumentParser(description="Fetch raw Yahoo Finance data for investment-report skill")
    p.add_argument("--symbols", nargs="*", help="symbols to fetch")
    p.add_argument("--output", help="write JSON to file; default stdout")
    args = p.parse_args()

    lookup = {code: label for label, code in DEFAULT_SYMBOLS}
    symbols = args.symbols or [code for _, code in DEFAULT_SYMBOLS]
    items = [fetch_symbol(symbol, lookup.get(symbol, symbol)) for symbol in symbols]
    payload = {"source": "Yahoo Finance（yfinance 直连）", "symbols": items}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text)
    else:
        print(text)


if __name__ == "__main__":
    main()

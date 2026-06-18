#!/usr/bin/env python3
"""
ThemePulse data builder
-----------------------
Pulls real prices from Yahoo Finance and writes themes.json with
equal-weight theme returns over d1 / w1 / m1 / ytd plus per-stock returns.

Run locally:   python scripts/build_themes.py
In CI:         see .github/workflows/themepulse.yml
"""
import json, sys, datetime as dt
import pandas as pd
import yfinance as yf

# id, name, kind(main|tomo), description, [ (ETF, note) ], [tickers]
THEMES = [
 ("genomics","Genomics / Biotech","main","Gene editing, sequencing and precision medicine.",
   [("ARKG","ARK Genomic"),("IDNA","iShares Genomics"),("GNOM","Global X Genomics")],
   ["CRSP","NTLA","BEAM","EXAS","ILMN","PACB","TWST","DNA","RXRX","TEM"]),
 ("space-leo","Space / LEO Infrastructure","tomo","Low-earth-orbit satellite infrastructure and launch.",
   [("ARKX","ARK Space"),("UFO","Procure Space")],
   ["RKLB","ASTS","PL","RDW","LUNR","SPCE"]),
 ("semi-equip","Semiconductor Equipment / EUV","main","Lithography and chip fabrication equipment.",
   [("SOXX","iShares Semi"),("SMH","VanEck Semi")],
   ["ASML","AMAT","LRCX","KLAC","TER","ONTO","ACLS"]),
 ("neoclouds","Neoclouds / AI Cloud Infrastructure","tomo","GPU-dense next-gen cloud providers.",
   [("DTCR","Global X Data Center"),("WGMI","Valkyrie Miners")],
   ["CRWV","NBIS","APLD","IREN","CIFR","WULF"]),
 ("memory","Memory / AI Storage Supercycle","main","DRAM/HBM and NAND memory supercycle.",
   [("SOXX","iShares Semi"),("SMH","VanEck Semi")],
   ["MU","WDC","STX","SNDK","005930.KS","000660.KS"]),
 ("rare-earth","Rare Earth / Critical Minerals","main","Rare-earth elements and critical minerals.",
   [("REMX","VanEck Rare Earth")],
   ["MP","LYSCF","TMC","UAMY","REEMF"]),
 ("uranium","Uranium / Nuclear","main","Uranium mining and nuclear power.",
   [("URA","Global X Uranium"),("URNM","Sprott Uranium"),("NLR","VanEck Nuclear")],
   ["CCJ","UEC","DNN","NXE","LEU","OKLO","SMR"]),
 ("custom-silicon","AI Custom Silicon / Inference Chips","tomo","ASIC and inference accelerators.",
   [("SOXX","iShares Semi"),("SMH","VanEck Semi")],
   ["AVGO","MRVL","ARM","CRDO","ALAB","GFS"]),
 ("spacex","SpaceX IPO Ecosystem","tomo","SpaceX / Starlink IPO ecosystem.",
   [("ARKX","ARK Space"),("UFO","Procure Space")],
   ["RKLB","ASTS","PL","RDW","LUNR"]),
 ("space-defense","Space / Defense","main","Space and defense primes.",
   [("ITA","iShares Aerospace"),("PPA","Invesco Defense"),("XAR","SPDR Aerospace")],
   ["LMT","RTX","NOC","LHX","KTOS","AVAV"]),
 ("dc-power","AI Datacenter Power","main","Datacenter power, cooling and electrical infra.",
   [("GRID","First Trust Grid"),("PAVE","Global X Infrastructure")],
   ["VRT","ETN","GEV","POWL","NVT","CEG","TLN"]),
 ("photonics","Photonics / Silicon Photonics CPO","tomo","Silicon photonics and co-packaged optics.",
   [("SOXX","iShares Semi")],
   ["COHR","LITE","AAOI","POET","CRDO","MRVL"]),
 ("semis","Semiconductors","main","Broad semiconductor sector.",
   [("SMH","VanEck Semi"),("SOXX","iShares Semi"),("XSD","SPDR Semi")],
   ["NVDA","AMD","AVGO","TSM","QCOM","INTC","MU","ARM"]),
 ("edge-ai","Edge AI / On-Device","tomo","On-device / edge AI.",
   [("AIQ","Global X AI"),("BOTZ","Global X Robotics & AI")],
   ["QCOM","AAPL","ARM","SYNA","AMBA","LFUS"]),
 ("quantum","Quantum Computing","tomo","Quantum computing.",
   [("QTUM","Defiance Quantum")],
   ["IONQ","RGTI","QBTS","QUBT","ARQQ"]),
 ("ev-battery","EV / Lithium / Battery","main","Electric vehicles, lithium and batteries.",
   [("LIT","Global X Lithium"),("DRIV","Global X Autonomous EV"),("BATT","Amplify Battery")],
   ["TSLA","ALB","LAC","QS","ENVX","PSNY"]),
 ("reshoring","Reshoring / Onshoring","main","Reshoring of manufacturing.",
   [("PAVE","Global X Infrastructure"),("XLI","Industrial Select")],
   ["NUE","STLD","CAT","ETN","ROK","EMR"]),
 ("defense-tech","Defense Tech / Autonomous Weapons","tomo","Autonomous defense and defense software.",
   [("ITA","iShares Aerospace"),("SHLD","Global X Defense Tech")],
   ["PLTR","KTOS","AVAV","RCAT","ONDS","BBAI"]),
 ("robotics","Robotics / Automation","main","Robotics and industrial automation.",
   [("BOTZ","Global X Robotics & AI"),("ROBO","ROBO Global"),("ARKQ","ARK Autonomous")],
   ["ISRG","ABB","ROK","TER","SYM","ZBRA"]),
 ("anthropic","Anthropic IPO Exposure","tomo","Indirect public exposure to Anthropic.",
   [("QQQ","Invesco QQQ")],
   ["GOOG","AMZN"]),
 ("800vdc","800VDC Power Infrastructure","tomo","800V DC power distribution infrastructure.",
   [("GRID","First Trust Grid"),("PAVE","Global X Infrastructure")],
   ["VRT","NVT","ETN","MOD","GEV"]),
 ("solar","Clean Energy / Solar","main","Clean energy and solar.",
   [("TAN","Invesco Solar"),("ICLN","iShares Clean Energy"),("QCLN","First Trust Clean")],
   ["FSLR","ENPH","SEDG","RUN","NXT","ARRY"]),
 ("humanoid","Humanoid Robotics","tomo","Humanoid robots and components.",
   [("BOTZ","Global X Robotics & AI"),("ROBO","ROBO Global")],
   ["TSLA","NVDA","ABB","SERV","ZBRA","FANUY"]),
 ("copper","Copper Supply Deficit","main","Copper supply deficit.",
   [("COPX","Global X Copper Miners"),("CPER","US Copper")],
   ["FCX","SCCO","TECK","ERO","IVPAF"]),
 ("cyber","Cybersecurity","main","Cybersecurity.",
   [("CIBR","First Trust Cyber"),("HACK","Amplify Cyber"),("BUG","Global X Cyber")],
   ["CRWD","PANW","ZS","FTNT","S","NET","OKTA"]),
 ("saas","Software as A Service (SaaS)","main","Cloud software / SaaS.",
   [("IGV","iShares Software"),("WCLD","WisdomTree Cloud"),("SKYY","First Trust Cloud")],
   ["CRM","NOW","WDAY","SNOW","DDOG","TEAM","HUBS"]),
]

# ============================================================
# WATCHLIST ADDITIONS (from TradingView watchlist)
# Existing tickers above are left untouched. These are added on top.
# TradingView symbols normalised to Yahoo Finance format.
# ============================================================
ADD_TO = {                       # add into existing themes (deduped)
    "semis":        ["CDNS", "SNPS", "MRVL"],
    "dc-power":     ["ANET", "EME", "STRL"],
    "ev-battery":   ["AMPX"],
    "genomics":     ["VKTX", "AMGN"],
    "space-defense":["HWM"],
}
NEW_THEMES = [                   # new themes for watchlist names with no home
 ("precious-metals","Precious Metals","main","Gold, silver and platinum exposure.",
   [("GLD","SPDR Gold"),("SLV","iShares Silver")],
   ["GLD","SLV","GC=F","SI=F","PL=F","SGLN.L","EGLN.L","IGLN.L","4GLD.DE"]),
 ("crypto","Crypto / Digital Assets","tomo","Major digital assets.",
   [],
   ["BTC-USD","ETH-USD","SOL-USD","RENDER-USD"]),
 ("bonds-cash","Bonds & Cash","main","Short-duration bonds and cash equivalents.",
   [("SGOV","iShares 0-3M Treasury")],
   ["SGOV","IEAA.L"]),
 ("energy-storage","Energy Storage / Fuel Cells","tomo","Fuel cells and grid-scale storage.",
   [],
   ["BE","EOSE"]),
 ("watchlist-other","Watchlist — Other","main","Watchlist holdings without a dedicated theme.",
   [],
   ["XOM","EWY","GRBK","CAAP","CAH"]),
]
# Symbols on the watchlist that have no clean Yahoo Finance equivalent and are skipped:
#   CBOE:EUV, GETTEX:XZGE, GETTEX:CBUE, XETR:8PSG, LSE:XLES,
#   EURONEXT:CSBGU7, SIX:CBGOLD.USD, AMEX:NASA

_themes = [list(t) for t in THEMES]
_by_id = {t[0]: t for t in _themes}
for _tid, _adds in ADD_TO.items():
    if _tid in _by_id:
        _tk = _by_id[_tid][5]
        for _s in _adds:
            if _s not in _tk:
                _tk.append(_s)
_themes.extend(list(t) for t in NEW_THEMES)
THEMES = _themes


def pct(a, b):
    if a is None or b is None or b == 0: return None
    return round((a / b - 1) * 100, 2)

def main():
    tickers = sorted({t for _,_,_,_,_,tk in THEMES for t in tk})
    print(f"Downloading {len(tickers)} tickers...", file=sys.stderr)
    data = yf.download(tickers, period="1y", interval="1d",
                       auto_adjust=True, progress=False, threads=True)
    close = data["Close"] if isinstance(data.columns, pd.MultiIndex) else data
    close = close.dropna(how="all")

    year = close.index[-1].year
    ytd_anchor = close[close.index >= f"{year}-01-01"].index[0]

    def ret(sym, period):
        if sym not in close.columns: return None
        s = close[sym].dropna()
        if len(s) < 2: return None
        last = s.iloc[-1]
        if period == "d1":  base = s.iloc[-2]
        elif period == "w1": base = s.iloc[-6] if len(s) > 6 else s.iloc[0]
        elif period == "m1": base = s.iloc[-22] if len(s) > 22 else s.iloc[0]
        elif period == "ytd":
            ys = s[s.index >= ytd_anchor]
            base = ys.iloc[0] if len(ys) else s.iloc[0]
        return pct(last, base)

    out_themes = []
    for tid, name, kind, desc, etfs, tks in THEMES:
        stocks = []
        for sym in tks:
            r = {p: ret(sym, p) for p in ("d1","w1","m1","ytd")}
            if r["d1"] is not None or r["ytd"] is not None:
                stocks.append({"sym": sym, **r})
        agg = {}
        for p in ("d1","w1","m1","ytd"):
            vals = [s[p] for s in stocks if s[p] is not None]
            agg[p] = round(sum(vals)/len(vals), 1) if vals else 0.0
        out_themes.append({
            "id": tid, "name": name, "kind": kind, "desc": desc,
            "count": len(stocks),
            "ret": agg,
            "etfs": [{"sym": s, "note": n} for s, n in etfs],
            "stocks": stocks,
        })

    payload = {
        "asof": close.index[-1].strftime("%Y-%m-%d"),
        "generated": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "note": "Equal-weight theme returns from Yahoo Finance adjusted close.",
        "themes": out_themes,
    }
    with open("themes.json", "w") as f:
        json.dump(payload, f, indent=1)
    print(f"Wrote themes.json — asof {payload['asof']}, {len(out_themes)} themes", file=sys.stderr)

if __name__ == "__main__":
    main()

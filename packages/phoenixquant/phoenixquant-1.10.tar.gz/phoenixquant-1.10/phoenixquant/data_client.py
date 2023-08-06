import io
import os
import sys
import json
import shelve
import requests
import pandas as pd
from time import sleep
from tempfile import gettempdir
from urllib import parse, request
from datetime import datetime
from functools import partial


class DataClient:
    """
    支持类型：
    期货合约：SHFE.rb2110
    现货合约：SSWE.ALH
    期权合约：CFFEX.IO2003-C-3900，CZCE.TA004P4550
    交易所组合：CZCE.SPD AP709&CF801，CZCE.IPS SF709&SM709，DCE.SP pp1709&pp1805
    主力合约：SHFE.rb@MAIN，指数合约：SHFE.rb@INDEX
    中证指数：CSI.000300
    深圳股票：SZSE.000001，上海股票：SSE.600000
    指数：SSE.000016 上证50指数，SSE.000300 沪深300指数 SSE.000905 中证500指数
    ETF：SSE.510050 上交所上证50etf SSE.510300 上交所沪深300etf SZSE.159919 深交所沪深300etf
    ETF期权：SSE.10002513，SSE.10002504，SZSE.90000097
    """

    md_url = "https://service-an8w6tgn-1253762454.sh.apigw.tencentcs.com"
    quant_url = "https://service-gh5ap9yb-1253762454.sh.apigw.tencentcs.com"

    def __init__(self, token="", debug=False, use_cache=False):
        self.debug = debug
        self.token = os.environ["DC_TOKEN"] if "DC_TOKEN" in os.environ else token

        # Data API
        self.get_bars = partial(self.history, data_type="bar", freq="MS", use_cache=use_cache)
        self.get_ticks = partial(self.history, data_type="tick", freq="12H", use_cache=use_cache)
        self.get_dailys = partial(self.history, data_type="daily", freq="AS", use_cache=use_cache)

        # Quant API
        self.concept_list = partial(self.quantdata, method="concept_list")
        self.concept = partial(self.quantdata, method="concept")
        self.concept_names = partial(self.quantdata, method="concept_names")
        self.shenwan_industry = partial(self.quantdata, method="shenwan_industry")
        self.shenwan_instrument_industry = partial(self.quantdata, method="shenwan_instrument_industry")
        self.zx_industry = partial(self.quantdata, method="zx_industry")
        self.zx_instrument_industry = partial(self.quantdata, method="zx_instrument_industry")
        self.get_industry = partial(self.quantdata, method="get_industry")
        self.get_instrument_industry = partial(self.quantdata, method="get_instrument_industry")
        self.get_industry_mapping = partial(self.quantdata, method="get_industry_mapping")
        self.industry_code = partial(self.quantdata, method="industry_code")
        self.IndustryCode = partial(self.quantdata, method="IndustryCode")
        self.sector_code = partial(self.quantdata, method="sector_code")
        self.SectorCode = partial(self.quantdata, method="SectorCode")
        self.get_trading_dates = partial(self.quantdata, method="get_trading_dates")
        self.get_next_trading_date = partial(self.quantdata, method="get_next_trading_date")
        self.get_previous_trading_date = partial(self.quantdata, method="get_previous_trading_date")
        self.get_latest_trading_date = partial(self.quantdata, method="get_latest_trading_date")
        self.trading_date_offset = partial(self.quantdata, method="trading_date_offset")
        self.is_trading_date = partial(self.quantdata, method="is_trading_date")
        self.has_night_trading = partial(self.quantdata, method="has_night_trading")
        self.id_convert = partial(self.quantdata, method="id_convert")
        self.instruments = partial(self.quantdata, method="instruments")
        self.all_instruments = partial(self.quantdata, method="all_instruments")
        self.sector = partial(self.quantdata, method="sector")
        self.industry = partial(self.quantdata, method="industry")
        self.get_future_contracts = partial(self.quantdata, method="get_future_contracts")

    def quantdata(self, method, **rest):
        post_data = {"method": method, **rest}
        res = requests.post(self.quant_url, headers={"token": self.token}, json=post_data)
        data = pd.read_json(res.content.decode("utf-8"), orient="split")
        return data

    def status_check(self):
        while True:
            try:
                with request.urlopen(self.md_url + "/status") as response:
                    json_data = json.loads(response.read())
                    if json_data.get("status", None) == "ok":
                        break
                    else:
                        raise "database is pending..."
            except Exception as e:
                print(e, "retrying...")
                sleep(1)

    def history(self, symbol, start_date, end_date, data_type, freq, use_cache):
        date_split = pd.date_range(start_date, end_date, freq=freq)
        date_split = [start_date, *date_split, end_date]
        data = pd.DataFrame()
        self.status_check()
        for index, _ in enumerate(date_split):
            if index + 1 != len(date_split):
                args = {
                    "symbol": symbol,
                    "data_type": data_type,
                    "start_date": datetime.strftime(date_split[index], "%Y%m%d%H%M%S"),
                    "end_date": datetime.strftime(date_split[index + 1], "%Y%m%d%H%M%S"),
                }
                key = "_".join(sorted(args.values(), reverse=True))
                cache_file = os.path.join(gettempdir(), key)
                cache_client = shelve.open(cache_file, writeback=True)
                try:
                    if use_cache:
                        if key in cache_client:
                            data = data.append(cache_client[key])
                            continue
                    df = pd.read_json(
                        self.md_url + "/md?" + parse.urlencode({"token": self.token, **args}), orient="split",
                    ).set_index("datetime")
                    data = data.append(df)
                    # save to cache
                    cache_client[key] = df
                    if self.debug:
                        print("下载完成", date_split[index], "~", date_split[index + 1])
                except:
                    pass

        return data.drop_duplicates()


if __name__ == "__main__":
    client = DataClient("your token!", debug=True, use_cache=True)
    result = client.instruments(order_book_ids=["10001941", "10001943"])
    print(result)
    # 日线
    # dailys = client.get_dailys(
    #     "CFFEX.IF@INDEX",
    #     start_date=datetime(2018, 1, 1),
    #     end_date=datetime(2021, 6, 4)
    # )
    # print(dailys)
    # # 分钟
    # bars = client.get_bars(
    #     "SHFE.rb@INDEX",
    #     start_date=datetime(2020, 4, 6),
    #     end_date=datetime(2021, 6, 4)
    # )
    # print(bars)

import io
import os
import sys
import json
import types
import shelve
import requests
import pandas as pd
from time import sleep
from tempfile import gettempdir
from http.client import responses
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
        today = datetime.now().strftime('%Y-%m-%d')
        
        self.debug = debug
        self.token = os.environ["DC_TOKEN"] if "DC_TOKEN" in os.environ else token

        # Data API
        self.get_bars = partial(self.history, data_type="bar", freq="MS", use_cache=use_cache)
        self.get_ticks = partial(self.history, data_type="tick", freq="12H", use_cache=use_cache)
        self.get_dailys = partial(self.history, data_type="daily", freq="AS", use_cache=use_cache)

        # Quant API
        self.concept_list = partial(self.quantdata, method="concept_list", date=today)
        self.concept = partial(self.quantdata, method="concept", date=today)
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
        self.all_instruments = partial(self.quantdata, method="all_instruments", type="CS", market="cn")
        self.sector = partial(self.quantdata, method="sector")
        self.industry = partial(self.quantdata, method="industry")
        self.get_future_contracts = partial(self.quantdata, method="get_future_contracts")

        # future
        self.futures = types.SimpleNamespace()
        self.futures.get_commission_margin = partial(self.quantdata, method="futures.get_commission_margin")
        self.futures.get_contracts = partial(self.quantdata, method="futures.get_contracts")
        self.futures.get_dominant = partial(self.quantdata, method="futures.get_dominant")
        self.futures.get_member_rank = partial(self.quantdata, method="futures.get_member_rank")
        self.futures.get_warehouse_stocks = partial(self.quantdata, method="futures.get_warehouse_stocks")
        self.futures.get_contract_multiplier = partial(self.quantdata, method="futures.get_contract_multiplier")

        self.jy_instrument_industry = partial(self.quantdata, method="jy_instrument_industry")

        self.econ = types.SimpleNamespace()
        self.econ.get_factors = partial(self.quantdata, method="econ.get_factors")
        self.econ.get_money_supply = partial(self.quantdata, method="econ.get_money_supply")
        self.econ.get_reserve_ratio = partial(self.quantdata, method="econ.get_reserve_ratio")

        self.get_main_shareholder = partial(self.quantdata, method="get_main_shareholder")
        self.get_current_news = partial(self.quantdata, method="get_current_news")
        self.get_trading_hours = partial(self.quantdata, method="get_trading_hours")
        self.get_private_placement = partial(self.quantdata, method="get_private_placement")
        self.get_share_transformation = partial(self.quantdata, method="get_share_transformation")

        self.get_update_status = partial(self.quantdata, method="get_update_status")
        self.info = partial(self.quantdata, method="info")
        self.get_basic_info = partial(self.quantdata, method="get_basic_info")

        self.convertible = types.SimpleNamespace()
        self.convertible.all_instruments = partial(self.quantdata, method="convertible.all_instruments")
        self.convertible.get_call_info = partial(self.quantdata, method="convertible.get_call_info")
        self.convertible.get_cash_flow = partial(self.quantdata, method="convertible.get_cash_flow")
        self.convertible.get_conversion_info = partial(self.quantdata, method="convertible.get_conversion_info")
        self.convertible.get_conversion_price = partial(self.quantdata, method="convertible.get_conversion_price")
        self.convertible.get_credit_rating = partial(self.quantdata, method="convertible.get_credit_rating")
        self.convertible.get_indicators = partial(self.quantdata, method="convertible.get_indicators")
        self.convertible.get_industry = partial(self.quantdata, method="convertible.get_industry")
        self.convertible.get_instrument_industry = partial(self.quantdata, method="convertible.get_instrument_industry")
        self.convertible.get_latest_rating = partial(self.quantdata, method="convertible.get_latest_rating")
        self.convertible.get_put_info = partial(self.quantdata, method="convertible.get_put_info")
        self.convertible.instruments = partial(self.quantdata, method="convertible.instruments")
        self.convertible.is_suspended = partial(self.quantdata, method="convertible.is_suspended")
        self.convertible.rating = partial(self.quantdata, method="convertible.rating")

        self.get_dominant_future = partial(self.quantdata, method="get_dominant_future")
        self.future_commission_margin = partial(self.quantdata, method="future_commission_margin")
        self.get_future_member_rank = partial(self.quantdata, method="get_future_member_rank")
        self.current_stock_connect_quota = partial(self.quantdata, method="current_stock_connect_quota")
        self.get_stock_connect_quota = partial(self.quantdata, method="get_stock_connect_quota")
        self.is_st_stock = partial(self.quantdata, method="is_st_stock")
        self._is_st_stock = partial(self.quantdata, method="_is_st_stock")
        self.is_suspended = partial(self.quantdata, method="is_suspended")
        self.get_stock_connect = partial(self.quantdata, method="get_stock_connect")
        self.get_securities_margin = partial(self.quantdata, method="get_securities_margin")
        self.get_margin_stocks = partial(self.quantdata, method="get_margin_stocks")
        self.get_shares = partial(self.quantdata, method="get_shares")
        self.get_allotment = partial(self.quantdata, method="get_allotment")
        self.current_snapshot = partial(self.quantdata, method="current_snapshot")
        self.current_minute = partial(self.quantdata, method="current_minute")
        self.get_live_ticks = partial(self.quantdata, method="get_live_ticks")
        self.get_price = partial(self.quantdata, method="get_price", frequency="1d", adjust_type="pre")
        self.get_all_factor_names = partial(self.quantdata, method="get_all_factor_names")
        self.get_factor = partial(self.quantdata, method="get_factor")
        self.get_factor_return = partial(self.quantdata, method="get_factor_return")
        self.get_factor_exposure = partial(self.quantdata, method="get_factor_exposure")
        self.get_style_factor_exposure = partial(self.quantdata, method="get_style_factor_exposure")
        self.get_descriptor_exposure = partial(self.quantdata, method="get_descriptor_exposure")
        self.get_stock_beta = partial(self.quantdata, method="get_stock_beta")
        self.get_factor_covariance = partial(self.quantdata, method="get_factor_covariance")
        self.get_specific_return = partial(self.quantdata, method="get_specific_return")
        self.get_specific_risk = partial(self.quantdata, method="get_specific_risk")
        self.get_index_factor_exposure = partial(self.quantdata, method="get_index_factor_exposure")
        self.Financials = partial(self.quantdata, method="Financials")
        self.financials = partial(self.quantdata, method="financials")
        self.get_financials = partial(self.quantdata, method="get_financials")
        self.PitFinancials = partial(self.quantdata, method="PitFinancials")
        self.pit_financials = partial(self.quantdata, method="pit_financials")
        self.get_pit_financials = partial(self.quantdata, method="get_pit_financials")
        self.get_pit_financials_ex = partial(self.quantdata, method="get_pit_financials_ex")
        self.get_fundamentals = partial(self.quantdata, method="get_fundamentals")
        self.deprecated_fundamental_data = partial(self.quantdata, method="deprecated_fundamental_data")
        self.current_performance = partial(self.quantdata, method="current_performance")
        self.performance_forecast = partial(self.quantdata, method="performance_forecast")
        self.Fundamentals = partial(self.quantdata, method="Fundamentals")
        self.fundamentals = partial(self.quantdata, method="fundamentals")
        self.query = partial(self.quantdata, method="query")
        self.get_capital_flow = partial(self.quantdata, method="get_capital_flow")
        self.get_open_auction_info = partial(self.quantdata, method="get_open_auction_info")
        self.index_components = partial(self.quantdata, method="index_components")
        self.index_weights = partial(self.quantdata, method="index_weights")
        self.index_indicator = partial(self.quantdata, method="index_indicator")
        self.get_ksh_auction_info = partial(self.quantdata, method="get_ksh_auction_info")
        self.get_split = partial(self.quantdata, method="get_split")
        self.get_dividend = partial(self.quantdata, method="get_dividend")
        self.get_dividend_info = partial(self.quantdata, method="get_dividend_info")
        self.get_ex_factor = partial(self.quantdata, method="get_ex_factor")
        self.get_turnover_rate = partial(self.quantdata, method="get_turnover_rate")
        self.get_price_change_rate = partial(self.quantdata, method="get_price_change_rate")
        self.get_yield_curve = partial(self.quantdata, method="get_yield_curve")
        self.get_block_trade = partial(self.quantdata, method="get_block_trade")
        self.get_exchange_rate = partial(self.quantdata, method="get_exchange_rate")
        self.get_temporary_code = partial(self.quantdata, method="get_temporary_code")


        self.options = types.SimpleNamespace()
        self.options.get_contract_property = partial(self.quantdata, method="options.get_contract_property")
        self.options.get_contracts = partial(self.quantdata, method="options.get_contracts")
        self.options.get_greeks = partial(self.quantdata, method="options.get_greeks")

        self.fenji = types.SimpleNamespace()
        self.fenji.get = partial(self.quantdata, method="fenji.get")
        self.fenji.get_a_by_interest_rule = partial(self.quantdata, method="fenji.get_a_by_interest_rule")
        self.fenji.get_a_by_yield = partial(self.quantdata, method="fenji.get_a_by_yield")
        self.fenji.get_all = partial(self.quantdata, method="fenji.get_all")

        self.ecommerce = partial(self.quantdata, method="ecommerce")

        self.xueqiu = types.SimpleNamespace()
        self.xueqiu.history = partial(self.quantdata, method="xueqiu.history")
        self.xueqiu.top_stocks = partial(self.quantdata, method="xueqiu.top_stocks")

    def quantdata(self, method, **rest):
        post_data = {"method": method, **rest}
        res = requests.post(self.quant_url, headers={"token": self.token}, json=post_data)
        if res.status_code == 200:
            json_data = res.content.decode("utf-8")
            try:
                return pd.read_json(json_data, orient="split")
            except Exception as e:
                print(e)
        else:
            print("ERROR:", responses[res.status_code])
        return pd.DataFrame()


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
                    cache_client.sync()
                    if self.debug:
                        print("下载完成", date_split[index], "~", date_split[index + 1])
                except:
                    pass

        return data.drop_duplicates()


if __name__ == "__main__":
    client = DataClient("your token!", debug=True, use_cache=True)
    result = client.all_instruments(type="CS", market='cn')
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

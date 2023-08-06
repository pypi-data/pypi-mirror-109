import datetime
import inspect
import json

import certifi  # type: ignore
from binance.client import Client  # type: ignore
import pandas as pd  # type: ignore
import urllib3  # type: ignore

urllib3.disable_warnings()


class Binance:
    def __init__(self, public_key, secret_key):
        self.client = Client(public_key, secret_key)

        self.http = self._pool_manager(urllib3)

        self.prefix_url = "https://api.binance.com/api/v3"
        self.bases_unstable = set()
        self.coins = {
            "fiat": {
                "AUD",
                "BRL",
                "EUR",
                "GBP",
                "NGN",
                "RUB",
                "TRY",
                "UAH",
                "ZAR",
            },
            "stable": {
                "BIDR",
                "BUSD",
                "BVND",
                "DAI",
                "IDRT",
                "PAX",
                "TUSD",
                "USDC",
                "USDT",
                "VAI",
            },
        }
        self.quotes_unstable = set()
        self.spot_assets = set()
        self.symbols_crypto = []

    def _dates_validate(self, date_start, date_end):
        date_format = "%d %b, %Y"
        date_type = datetime.date
        date_start_strp = datetime.datetime.strptime(date_start, date_format)
        date_end_strp = datetime.datetime.strptime(date_end, date_format)

        if (
            date_start is not None
            and date_end is not None
            and isinstance(date_start_strp, date_type) is True
            and isinstance(date_end_strp, date_type) is True
        ):
            start = datetime.datetime.strptime(date_start, date_format)
            end = datetime.datetime.strptime(date_end, date_format)
            if start < end:
                return True
            else:
                return False
        else:
            return False

    def _pool_manager(self, urllib3):
        cert_reqs = "CERT_REQUIRED"
        ca_certs = certifi.where()
        retries = urllib3.Retry(3, redirect=2)
        timeout = 10.0

        return urllib3.PoolManager(
            cert_reqs=cert_reqs, ca_certs=ca_certs, retries=retries, timeout=timeout
        )

    def _symbol_df_get(self, bars):
        binance_candle_columns = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "ct",
            "qav",
            "not",
            "tbbav",
            "tbqav",
            "i",
        ]
        btc_df = pd.DataFrame(bars, columns=binance_candle_columns)

        btc_df["time"] = pd.to_datetime(btc_df["date"], unit="ms").tolist()

        return pd.DataFrame(
            {
                "time": btc_df["time"].tolist(),
                "high": btc_df["high"].astype(float).tolist(),
                "low": btc_df["close"].astype(float).tolist(),
                "close": btc_df["close"].astype(float).tolist(),
                "volume": pd.to_numeric(btc_df["volume"], errors="coerce")
                .astype(int)
                .tolist(),
            }
        )

    def symbol_interval_get(self, signal, interval, date_start, date_end):
        function_name = inspect.currentframe().f_code.co_name

        try:
            if self._dates_validate(date_start, date_end) is True:
                bars = self.client.get_historical_klines(
                    signal["symbol"], interval, date_start, date_end
                )

                return self._symbol_df_get(bars)
            else:
                raise Exception("{} int_1 ".format(function_name))
        except Exception as err:
            raise Exception("{} main".format(function_name)).with_traceback(
                err.__traceback__
            )

    def symbol_history_get(self, signal, interval, unit="day", samples=101):
        bars = self.client.get_historical_klines(
            signal["symbol"], interval, "{} {} ago UTC".format(samples, unit)
        )

        return self._symbol_df_get(bars)

    def symbols_get(self):
        function_name = inspect.currentframe().f_code.co_name
        symbols = []

        try:
            response = self.http.request(
                "GET", "{}/exchangeInfo".format(self.prefix_url)
            )

            if response.status == 200:
                data_response = json.loads(response.data.decode("utf-8"))

                for product in data_response["symbols"]:
                    symbol = {
                        "baseAsset": product["baseAsset"],  # BTC
                        "quoteAsset": product["quoteAsset"],  # USDT
                        "symbol": product["symbol"],  # BTCUSDT
                        "sdema": False,
                        "suggested": False,
                        "indicator_summary": "",
                    }
                    if (
                        (product["status"] == "TRADING")
                        and ("SPOT" in product["permissions"])
                        and ("LEVERAGED" not in product["permissions"])
                    ):
                        if (
                            product["baseAsset"] not in self.coins["fiat"]
                            and product["quoteAsset"] not in self.coins["fiat"]
                        ):
                            self.symbols_crypto.append(symbol)

                        if (
                            product["baseAsset"] not in self.coins["fiat"]
                            and product["baseAsset"] not in self.coins["stable"]
                        ):
                            self.bases_unstable.add(product["baseAsset"])

                        if (product["quoteAsset"] not in self.coins["fiat"]) and (
                            product["quoteAsset"] not in self.coins["stable"]
                        ):
                            self.quotes_unstable.add(product["quoteAsset"])

                        if (
                            product["baseAsset"] not in self.coins["fiat"]
                            and product["baseAsset"] not in self.coins["stable"]
                            and product["quoteAsset"] not in self.coins["fiat"]
                            and product["quoteAsset"] in self.coins["stable"]
                        ):
                            symbols.append(symbol)
                            self.spot_assets.add(product["baseAsset"])
                return symbols
            else:
                raise Exception("{} int_1 HTTP != 200".format(function_name))
        except Exception as err:
            raise Exception("{} main ".format(function_name)).with_traceback(
                err.__traceback__
            )

    def symbols_get_quote_given(self, quote_symbol):
        function_name = inspect.currentframe().f_code.co_name
        symbols = set()

        try:
            response = self.http.request(
                "GET", "{}/exchangeInfo".format(self.prefix_url)
            )

            if response.status == 200:
                data_response = json.loads(response.data.decode("utf-8"))

                for product in data_response["symbols"]:
                    if (
                        (product["status"] == "TRADING")
                        and ("SPOT" in product["permissions"])
                        and ("LEVERAGED" not in product["permissions"])
                    ):
                        if product["quoteAsset"] == quote_symbol:
                            symbols.add(product["baseAsset"])
                return symbols
            else:
                raise Exception("{} int_1 HTTP != 200".format(function_name))
        except Exception as err:
            raise Exception("{} main ".format(function_name)).with_traceback(
                err.__traceback__
            )

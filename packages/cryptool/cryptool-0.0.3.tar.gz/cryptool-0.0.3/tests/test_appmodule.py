from cryptool.exchanges.binance import Binance

env_exchange_public_key = 'x'
env_exchange_secret_key = 'x'

binance = Binance(env_exchange_public_key, env_exchange_secret_key)

def test_binance_symbol_history_get():
    samples_number = 361
    timeframe = {'interval': '1h', 'unit': 'hour', 'samples': samples_number}
    product = {'symbol': 'ETHUSDC'}

    stock = binance.symbol_history_get(product, timeframe['interval'], unit=timeframe['unit'], samples=timeframe['samples'])
    assert len(stock) == samples_number

def test_binance_symbol_interval_get():
    product = {'symbol': 'ETHUSDC'}

    stock = binance.symbol_interval_get(product, '1d', date_start='7 Jun, 2021', date_end='10 Jun, 2021')
    assert len(stock) == 4

def test_binance_symbols_get():
    assert len(binance.symbols_get()) > 0

def test_binance_symbols_get_quote_given():
    assert len(binance.symbols_get_quote_given('BTC')) > 0
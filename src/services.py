from src.workers import NestWorker, FastAPIWorker
from src.config import TICKER, INTERVAL, PORT_EMITTER_PRICE, PORT_EMITTER_SINGAL


class EmitterPrice(NestWorker):
    folder = 'emitter_price'
    
    def prepare(self):
        self.create_dockerfile()
        self.save_env({
            'PORT': self.port,
        })
        self.save_config({
            'type': 'price',
            'tokens': [ TICKER ],
            'intervals': [ INTERVAL ],
        })

class TempEmitterPrice(FastAPIWorker):
    folder = 'temp_emitter_price'
    
    def prepare(self):
        self.create_dockerfile()
        self.save_env({
            'PORT': self.port,
        })
        self.save_config({})


class EmitterSignal(NestWorker):
    folder = 'emitter_signal'
    
    def prepare(self):
        self.create_dockerfile()
        self.save_env({
            'PORT': self.port,
        })
        self.save_config({
            'type': 'signal',
            'identifier': 'manual',
            'tokens': [ TICKER ],
            # 'chance': 0 
        })


class TradingBot(NestWorker):
    folder = 'trading_bot'
    
    def prepare(self):
        self.create_dockerfile()
        self.save_env({
            'PORT': self.port,
            'BINANCE_USE_TEST': 'False',
            'BINANCE_API_KEY': '',
            'BINANCE_API_SECRET': '',
        })
        self.save_config({
            'minimum_amounts': {
                'BTC': '0.001',
                'USDT': '10.0'
            },
            'prices': { TICKER: PORT_EMITTER_PRICE },
            'signals' : {
                'manual': {
                    'port': PORT_EMITTER_SINGAL,
                    'tokens': [TICKER]
                }
            }
        })


class ModelBasic(FastAPIWorker):
    folder = 'model_basic'
    
    def prepare(self):
        self.create_dockerfile()
        self.save_env({
            'PORT': self.port,
        })
        self.save_config({})


class BackTester(FastAPIWorker):
    folder = 'backtester'
    
    def prepare(self):
        self.create_dockerfile()
        self.save_env({
            'PORT': self.port,
        })
        self.save_config({})
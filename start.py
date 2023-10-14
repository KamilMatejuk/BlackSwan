import sys
from src.composer import DockerComposer
from src.config import PORT_EMITTER_PRICE, PORT_EMITTER_SINGAL, PORT_TRADING_BOT, PORT_BACKTESTER
from src.services import EmitterPrice, EmitterSignal, TradingBot


if __name__ == '__main__':
    dc = DockerComposer([
        EmitterPrice(PORT_EMITTER_PRICE),
        EmitterSignal(PORT_EMITTER_SINGAL),
        TradingBot(PORT_TRADING_BOT),
        # Backtester(PORT_BACKTESTER),
    ], len(sys.argv) > 1 and sys.argv[1] == "--no-cache")
    dc.prepare()
    dc.start()
    
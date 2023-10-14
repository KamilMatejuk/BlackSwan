import sys
from src.composer import DockerComposer
from src.config import PORT_EMITTER_PRICE, PORT_EMITTER_SINGAL, PORT_TRADING_BOT, PORT_BACKTESTER
from src.services import EmitterPrice, EmitterSignal, TradingBot
from src.services import TempEmitterPrice


if __name__ == '__main__':
    dc = DockerComposer([
        TempEmitterPrice(PORT_EMITTER_PRICE),
    ], len(sys.argv) > 1 and sys.argv[1] == "--no-cache")
    dc.prepare()
    dc.start()
    
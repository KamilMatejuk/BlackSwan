import sys
from src.composer import DockerComposer
from src.config import PORT_EMITTER_PRICE
from src.config import PORT_EMITTER_SINGAL
from src.config import PORT_TRADING_BOT
from src.config import PORT_BACKTESTER
from src.config import PORT_LEARNER
from src.config import PORT_MODEL
from src.services import EmitterPrice
from src.services import EmitterSignal
from src.services import TradingBot
from src.services import TempEmitterPrice
from src.services import ModelBasic
from src.services import ModelRL
from src.services import BackTester
from src.services import Learner


if __name__ == '__main__':
    dc = DockerComposer([
        TempEmitterPrice(PORT_EMITTER_PRICE),
        ModelRL(PORT_MODEL),
        Learner(PORT_LEARNER),
    ], len(sys.argv) > 1 and sys.argv[1] == "--no-cache")
    dc.prepare()
    dc.start()
    
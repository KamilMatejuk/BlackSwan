import os
import json
import yaml
from textwrap import dedent


TICKER='BTCUSDT'
INTERVAL='1s'

PORT_EMITTER_PRICE=50001
PORT_EMITTER_SINGAL=50002
PORT_TRADING_BOT=50003


class Worker:
    
    def __init__(self, port):
        self.port = port

    def save_env(self, data: dict):
        assert self.folder is not None
        with open(os.path.join(self.folder, '.env.local'), 'w+') as f:
            for key, value in data.items():
                f.write(f'{key}={value}\n')

    def save_config(self, data: dict):
        assert self.folder is not None
        with open(os.path.join(self.folder, 'config.json'), 'w+') as f:
            json.dump(data, f, indent=4)
    
    def prepare(self):
        raise NotImplementedError("TODO: create Dockerfile, config.json and .env.local")

            
class Nest(Worker):

    def create_dockerfile(self):
        assert self.folder is not None
        with open(os.path.join(self.folder, 'Dockerfile'), 'w+') as f:
            f.write(dedent('''
            FROM node:20

            # tini - for passing SIGINT interrupts
            ENV TINI_VERSION v0.19.0
            ENV TINI_SUBREAPER true
            ADD https://github.com/krallin/tini/releases/download/$TINI_VERSION/tini /tini
            RUN chmod +x /tini
            ENTRYPOINT ["/tini", "--"]

            # dependencies
            COPY package*.json .
            RUN npm install

            # source
            COPY src/ src/
            COPY config.json .
            COPY tsconfig.build.json .
            COPY tsconfig.json .
            COPY nest-cli.json .
            COPY *setups.json .
            COPY .env.local .
            RUN npm run build

            CMD [ "node", "dist/main.js"]
            '''))


class EmitterPrice(Nest):
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


class EmitterSignal(Nest):
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


class TradingBot(Nest):
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


class DockerComposer:
    def __init__(self, services: list[Worker]):
        self.services = services
        
    def prepare(self):
        for service in self.services:
            service.prepare()
        compose = { 'version': '3', 'services': {} }
        for service in self.services:
            compose['services'][service.folder] = {
                'container_name': service.folder,
                'network_mode': 'host',
                'build': { 'context': f'./{service.folder}' },
            }
        with open('docker-compose.yml', 'w+') as f:
            yaml.dump(compose, f)

    def start(self):
        for service in self.services:
            os.system(f'docker rm -f {service.folder} 2>/dev/null >/dev/null')
        os.system('docker compose build')
        os.system('docker compose up --remove-orphans')


if __name__ == '__main__':
    dc = DockerComposer([
        EmitterPrice(PORT_EMITTER_PRICE),
        EmitterSignal(PORT_EMITTER_SINGAL),
        TradingBot(PORT_TRADING_BOT),
    ])
    dc.prepare()
    dc.start()
    
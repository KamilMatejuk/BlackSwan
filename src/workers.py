import os
import json
from textwrap import dedent


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

            
class NestWorker(Worker):

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

            CMD [ "node", "dist/main.js" ]
            '''))


class FastAPIWorker(Worker):
    
    def create_dockerfile(self):
        assert self.folder is not None
        with open(os.path.join(self.folder, 'Dockerfile'), 'w+') as f:
            f.write(dedent(f'''
            FROM python:3.10

            # dependencies
            COPY requirements.txt .
            RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt

            # source
            COPY src/ src/
            COPY main.py .
            COPY config.json .
            COPY .env.local .

            CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{self.port}"]
            '''))

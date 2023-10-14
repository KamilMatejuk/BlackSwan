import os
import yaml
from src.workers import Worker


class DockerComposer:
    def __init__(self, services: list[Worker], use_cache: bool):
        self.services = services
        self.use_cache = use_cache
        
    def prepare(self):
        for service in self.services:
            service.prepare()
        compose = { 'version': '3', 'services': {} }
        for service in self.services:
            compose['services'][service.folder] = {
                'container_name': service.folder,
                'network_mode': 'host',
                'build': { 'context': f'./{service.folder}' },
                'volumes': [ f'./{service.folder}/data:/data' ],
            }
        with open('docker-compose.yml', 'w+') as f:
            yaml.dump(compose, f)

    def start(self):
        for service in self.services:
            os.system(f'docker rm -f {service.folder} 2>/dev/null >/dev/null')
        os.system('docker compose build ' + ('--no-cache' if self.use_cache else ''))
        os.system('docker compose up --remove-orphans')

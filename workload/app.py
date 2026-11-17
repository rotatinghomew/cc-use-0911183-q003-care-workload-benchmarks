from pathlib import Path
import json

from .ledger import *
from .comparison import *
from .settlement import *


class Application:
    def __init__(self, store):
        self.store = store

    def seed(self):
        directory = Path(__file__).resolve().parent.parent / 'fixtures'
        for path in sorted(directory.glob('*.json')):
            if not self.store.all(path.stem):
                self.store.put_many(path.stem, json.loads(path.read_text(encoding='utf-8')))

    def demo(self):
        return {'services': service_overview(self.store), 'detail': service_detail(self.store, 's1'), 'invoice': draft_invoice(self.store, 'east', '2026-10')}

    def check(self):
        value = self.demo()
        return {'status': 'ok', 'summary': value}

    def call(self, method, route, payload):
        if method == 'GET' and route == 'summary':
            return self.demo()
        if method == 'GET' and route == 'service':
            return service_detail(self.store, payload['id'])
        if method == 'POST' and route == 'service':
            return {'revision': save_service(self.store, payload)}
        if method == 'POST' and route == 'confirm':
            return confirm_invoice(self.store, payload['team'], payload['month'])
        raise KeyError('接口不存在')

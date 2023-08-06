
import urllib
import urllib.request
import json

# default api base
API = 'http://api.y-space.pw/'

def _get(api, *args):
    url = api + "/".join(args)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        p = response.read()
    return json.loads(p)
    
class Exoplanets():
    def __init__(self, api=API):
        self.api = api

    def rand(self, n):
        return _get(self.api, 'exoplanets', 'rand', n)

    def list(self):
        return _get(self.api, 'exoplanets', 'list')
        
    def id(self, pl_name):
        return _get(self.api, 'exoplanets', 'id', pl_name)

    def hostname(self, hs_name):
        return _get(self.api, 'exoplanets', 'hostname', hs_name)

    def stats(self):
        return _get(self.api, 'exoplanets', 'stats')

class Messier():
    def __init__(self, api=API):
        self.api = api

    def rand(self, n):
        return _get(self.api, 'messier', 'rand', n)

    def list(self):
        return _get(self.api, 'messier', 'list')
        
    def id(self, pl_name):
        return _get(self.api, 'messier', 'id', pl_name)

class ysapi():
    def __init__(self, api=API):
        self.api = api
        self.exoplanates = Exoplanets(self.api)
        self.messier     = Messier(self.api)


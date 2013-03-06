import json
import os.path

class Config(object):
    
    @classmethod
    def from_json_file(cls, path):
        return Config(
            json.load(
                open(path)
            )
        )
        
    def __init__(self, entries):
        self._incremented_version = False
        self._version = 0
        self._entries = entries
            
    def __getitem__(self, key):
        parts = key.split('.')
        entry = self._entries
        for p in parts:
            entry = entry.get(p)
            if not entry:
                raise KeyError, key
        return entry
        
    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError, e:
            return default
        
        
    def has_version(self):
        return self.get('global.cache_bust.enabled', False) \
                    and self.get('global.cache_bust.versioning.method') == 'file'
        
    def get_version(self):
        if self._incremented_version:
            return self._version
            
        if not self.has_version():
            return None
        
        path = self.get('global.cache_bust.versioning.filename', './version')
        
        if os.path.exists(path):
            version = open(path, 'r').read()
            try:
                version = int(version)
            except ValueError:
                version = 0
        else:
            version = 0
        
        version += 1
        open(path, 'w').write(str(version))
        self._version = version
        self._incremented_version = True
        
        return self._version
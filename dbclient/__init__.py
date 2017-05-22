# -*- coding:utf-8 -*-
"""
======================
@author Vincent
@config file
init for database
======================
"""
import six
import os
class DictObj(object):
    def __init__(self, maps):
        self.maps = maps
    def __setattr__(self, name, value):
        if name == 'maps':
            object.__setattr__(self, name, value)
            return
        self.maps[name] = value
    def __getattr__(self, name):
        v = self.maps[name]
        if isinstance(v, (dict)):
            return DictObj(v)
        if isinstance(v, (list)):
            r = []
            for i in v:
                r.append(DictObj(i))
            return r
        else:
            return self.maps[name]
    def __getitem__(self, name):
        return self.maps[name]
class SetDBset():
    def __init__(self):
        self._setdbset()
    def _read_config(self, value):
        if not value:
            return {}
        import json
        def underline_dict(d):
            if not isinstance(d, dict):
                return d
            return dict((k.replace('-', '_'), underline_dict(v)) for k, v in six.iteritems(d))
        result = underline_dict(json.load(value))
        return result
    def _setdbset(self):
        path = os.path.split(os.path.realpath(__file__))[0]
        dbconfig_path = os.path.join(path,"dbconfig.json")
        fp = open(dbconfig_path, 'r')
        self.db_config = self._read_config(fp)['db']
        self.db = DictObj(self.db_config)
class DBClient(SetDBset):
    def __init__(self):
        SetDBset.__init__(self)
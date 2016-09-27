#encoding: utf-8

from sqlalchemy import text, create_engine

class Const(type):
    warning = 'This class is immutable.'
    def __setattr__(self, k, v):
        raise AttributeError(self.warning)
    
DataBaseType = Const("DataBaseType", (), {
    "POSTGRESQL": 0,
    "MYSQL": 1,
    "SQLITE": 2
})

DB_URLS = [
    'postgresql+psycopg2://{username}:{password}@{host}/{dbname}',
    'mysql+mysqldb://{username}:{password}@{host}/{dbname}',
    'sqlite:////{dbpath}'
]
     
class Record(object):
    
    def __init__(self, keys=[], vals=[]):
        self._keys = keys
        self._vals = vals
        self._cols = len(keys)
        
        assert len(self._keys) == len(self._vals)
    
    def __getitem__(self, x):    
        if isinstance(x, str):
            try:
                x = self._keys.index(x)
            except ValueError:
                return None
            
        if isinstance(x, int) and x < self._cols:
            return self._vals[x]
        
        return None
    
    def get(self, key):
        return self[key]

    def as_dict(self):
        items = zip(self._keys, self._vals)
        return dict(items)

class RecordCollection(object):
    '''
    代码精妙之处就在这了
    '''
    def __init__(self, records):
        self._gen_records = records
        self._all_records = []
        self.pending = True
    
    def __getitem__(self, key):
        '''
        key为int或slice类型
        '''
        is_int = isinstance(key, int)
        if is_int:  #如果为int, 则将其转为slice类型
            key = slice(key, key+1)
            
        is_slice = isinstance(key, slice)
        if not is_slice:
            raise TypeError("key is a wrong type. supported type is int or slice")
        
        while len(self) < key.stop or key.stop is None:
            try:
                next(self)
            except StopIteration:
                break
            
        rst = self._all_records[key]
        
        if is_int:  #如果传入的key为int, 则返回一个Record
            return rst[0]
        
        return rst  #如果传入的key为slice, 则返回一个Record的数组
            
    def __iter__(self):
        idx = 0
        while True:
            if idx < len(self):
                yield self[idx]
            else:
                yield next(self)
            idx += 1
    
    def next(self):
        return self.__next__()
    
    def __next__(self):
        try:
            record = next(self._gen_records)
            self._all_records.append(record)
            return record
        except StopIteration:
            self.pending = False
            raise StopIteration("no pending record")
    
    def __len__(self):
        return len(self._all_records)
    
    def all(self, as_dict=False):
        if as_dict:
            return [r.as_dict() for r in self]        
        return list(self)
    
class Database(object):
    
    def __init__(self, dbtype, **kwargs):
        
        if 0 < dbtype < len():
            raise TypeError("%s is not supported yet."%str(dbtype))
        
        _db_url = DB_URLS[dbtype].format(**kwargs)
        self._conn = create_engine(_db_url).connect()
    
    def close(self):
        self._conn.close()
    
    def query(self, tablenames=[], cols=[], where=None, where_vals={}, fetchall=False):
        
        if not tablenames:
            return None
        
        if isinstance(tablenames, str):
            tablenames = [tablenames]
        
        if not cols:
            cols = ["*"]
        
        if where:
            query_sql = "select %s from %s where %s"%(",".join(cols), ",".join(tablenames), where)
        else:
            query_sql = "select %s from %s"%(",".join(cols), ",".join(tablenames))
        
        cursor = self._conn.execute(text(query_sql), **where_vals)
        
        records = (Record(cursor.keys(), row) for row in cursor)
        
        rst = RecordCollection(records)
         
        if fetchall:
            return rst.all()
         
        return rst

if __name__ == "__main__":
    db = Database(DataBaseType.POSTGRESQL, dbname="ces", username="postgres", password="", host="127.0.0.1")
    rst = db.query("student", where="name like :pre", where_vals={"pre": "abc%"})
    for item in rst:
        print item.as_dict()
    
    
    

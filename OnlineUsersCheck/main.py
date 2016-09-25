#coding:utf-8
import string
import random
import time
from redis import StrictRedis

from Queue import Queue
from threading import Thread

conn = StrictRedis.from_url("redis://127.0.0.1")

def init_users():
    '''
    生成大约1000个用户
    '''
    x = string.ascii_uppercase
    y = string.ascii_lowercase
    names = set([random.choice(x)+"_"+random.choice(y)+random.choice(y) for _ in range(1000)])
    conn.sadd("users", *names)
    
def init_friends():
    '''
    为每个人分配10到100个好友
    '''
    users = Queue()
    map(lambda username: users.put(username), conn.smembers("users"))
    
    def worker():
        while True:
            username = users.get()  
            nums = random.randint(10, 100)
            friends = conn.srandmember("users", nums)
            conn.sadd(username, *friends)
            users.task_done()
            
    for _ in range(10):
        t = Thread(target=worker)
        t.daemon = True
        t.start()
        
    users.join()

def query_online_friends(username):
    '''
    查询当前在线的好友，尽量以事务的方式执行
    这样可以减少数据在客户端/服务器端之间的传输
    '''
    p = conn.pipeline()
    p.zunionstore("tmp.users.accessed", ["users.accessed"])
    p.zremrangebyscore("tmp.users.accessed", 0, time.time()-3)
    p.zinterstore("tmp.online.friends", ["tmp.users.accessed", username])
    p.zrange("tmp.online.friends", 0, -1)
    p.delete("tmp.users.accessed")
    p.delete("tmp.online.friends")
    rst = p.execute()    
    return rst[-3]
    
if __name__=="__main__":
    while True:
        online_friends = query_online_friends("V_tz")
        print len(online_friends), online_friends
        time.sleep(2)
    

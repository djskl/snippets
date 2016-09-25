from psycopg2 import connect
from threading import Thread
from Queue import Queue
import json
import random
import string
import uuid

conn = connect(database="ces", user="postgres", password="", host="127.0.0.1")

q = Queue()
for _ in range(100000):
    name = "".join([random.choice(string.lowercase) for _ in range(5)])
    q.put(json.dumps([name, "20160923 12:34:12", random.randint(0,1), random.randint(1,1000)/10.0, str(uuid.uuid4())]))
    
def worker():
    cursor = conn.cursor()
    while True:
        args = json.loads(q.get())
        cursor.execute("insert into student values(%s, %s, %s, %s, %s)", args)
        q.task_done()
        
for _ in range(20):
    t = Thread(target=worker)
    t.setDaemon(True)
    t.start()

q.join()

conn.commit()
conn.close()

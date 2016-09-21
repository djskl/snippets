import requests
import random
import time
from threading import Thread
from redis import StrictRedis

conn = StrictRedis()

users = conn.execute_command("smembers V_tz")

def worker():
    while True:
        username = random.choice(users)
        requests.get("http://127.0.0.1/"+username)
        time.sleep(random.randint(1, 5))
        
for _ in range(20):
    Thread(target=worker).start()
    
if __name__ == "__main__":
    username = random.choice(users)
    requests.get("http://127.0.0.1/"+username)
from redis import StrictRedis
import time

def application(env, sr):
    
    username = env["PATH_INFO"]
    
    if username.startswith("/"):
        username = username[1:]
    
    if username.endswith("/"):
        username = username[:-1]
    
    conn = StrictRedis()
    
    exists = conn.sismember("users", username)
    if not exists:
        sr("404 NOT FOUND", [("Content-Type", "text/html")])
        return ""
    
    conn.zadd("users.accessed", time.time(), username)
    
    print time.time(), username
    
    sr("200 OK", [("Content-Type", "text/html")])
    return ""
    
    
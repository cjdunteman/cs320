from flask import Flask, request, Response
import json, time

app = Flask(__name__)

fruits = ["apple", "banana", "kiwi", "cantaloupe", "berries", "orange"]

# key: client IP addr
# val: last time request served (in seconds since 1970)
last_req = {}

def rate_limit(fn):
    def wrapper():
        # policy: one request every 2 seconds, per IP address
        client_ip = request.remote_addr
        next_allowed = last_req.get(client_ip, 0) + 2
        now = time.time()
        
        should_allow = now >= next_allowed
        if not should_allow:
            return Response("backoff!!", status=429, 
                            headers={"Retry-After": next_allowed-now})
        last_req[client_ip] = now
        return fn()
    wrapper.__name__ = fn.__name__
    return wrapper

@app.route("/fruit")
@rate_limit
def fruit():
    idx = int(request.args.get("idx", 0))
    if idx >= len(fruits):
        return ""
    return fruits[idx]

if __name__ == "__main__":
    app.run("0.0.0.0")
# from flask import Flask, Response

# app = Flask(__name__)

# html = """<html><head><title>Too Many Requests</title></head><body><h1>Too Many</h1><p>I only allow 50 requests per hour. Try again soon.</p></body></html>"""

# @app.route("/")
# def home():
#     # Flask automatically sets status code, headers
#     r = Response(html, status=429, headers={"Retry-After":3, "Hello": "World"})
#     return r

# # Checking if module or program
# if __name__ == "__main__":
#     app.run("0.0.0.0")


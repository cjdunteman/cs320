# from flask import Flask, request, Response
# import json

# app = Flask(__name__)

# def my_jsonify(data):
#     resp_body = json.dumps(data)
#     r = Response(resp_body, headers={"Content-Type": "application/json"})
#     return r

# @app.route("/math.json")
# def home():
#     x = float(request.args.get("x", 0))
#     y = float(request.args.get("y", 0))
#     results = {"add": x+y, "sub": x-y, "mult": x*y}
#     return my_jsonify(results)

# if __name__ == "__main__":
#     app.run("0.0.0.0")
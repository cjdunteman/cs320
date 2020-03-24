# project: p3
# submitter: cdunteman
# partner: none

import pandas as pd
from flask import Flask, request, jsonify, render_template
from IPython.display import display, HTML
import re

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
# https://stackoverflow.com/questions/43263356/prevent-flask-jsonify-from-sorting-the-data/43263483

df = pd.read_csv("main.csv")

count = 1
countA = 0
countB = 0

@app.route('/')
def home():
    global count
    count += 1
    if (count <= 10):
        if (count % 2 == 0):
            with open("indexA.html") as f:
                html = f.read()
        else:
            with open("indexB.html") as f:
                html = f.read()
    else:
        if (countA > countB):
            with open("indexA.html") as f:
                html = f.read()
        else:
            with open("indexB.html") as f:
                html = f.read()
    return html

def whatever():
    print('heeljoiejf')

@app.route('/browse.html')
def browse():
    return df.to_html()

@app.route('/api.html')
def api():
    with open("api.html") as f:
        html = f.read()
    return html

@app.route('/donate.html')
def donate():
    if request.args.get('from') == 'A':
        global countA
        countA += 1
    else:
        global countB
        countB += 1
    with open("donate.html") as f:
        html = f.read()
    return html

@app.route('/stats.json')
def stats():
    data_dict = df.to_dict()
    name = request.args.get('name')
    team = request.args.get('team')
    min_avg = request.args.get('min_avg')
    
    # Search by player name
    if name != None:
        for index, row in df.iterrows():
            if name == row.Player:
                return jsonify(row.to_dict())
    # Search by team
    elif team != None:
        row_list = []
        for index, row in df.iterrows():
            if team == row.Team:
                row_list.append(row.to_dict())        
        return jsonify(row_list)
    # Search by min batting avg
    elif min_avg != None:
        row_list = []
        for index, row in df.iterrows():
            if float(min_avg) <= row.AVG:
                row_list.append(row.to_dict())
        return jsonify(row_list)
    # Full data
    else:
        return df.to_json(orient='records')

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email):
        with open("emails.txt", "a") as f:
            f.write(email + "\n")
        return jsonify("thanks")
    return jsonify("No, you did not enter a valid email address. Enter a valid email or you will get a virus!")

if __name__ == '__main__':
    app.run(host="0.0.0.0") # don't change this line!

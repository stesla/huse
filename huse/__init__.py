import re

import logging
logger = logging.getLogger(__name__)

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("huse-form.html")
    text = request.form['text']
    codes = re.findall(r'[|{]\d{3}|[|{]=\w', text)
    values = dict()
    for code in codes:
        values[code] = values.get(code, 0) + 1
    values_sorted = sorted(values.items(), key=lambda a: a[1], reverse=True)
    return render_template("huse-result.html", values=values_sorted)

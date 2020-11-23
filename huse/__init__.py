import re

import logging
logger = logging.getLogger(__name__)

from flask import Flask, render_template, request
app = Flask(__name__)

from .markup import *

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("huse-form.html")
    text = request.form['text'].strip()
    codes = re.findall(ANSI_CODE, text)
    values = dict()
    for code in codes:
        values[code] = values.get(code, 0) + 1
    values_sorted = [(colorFromCode(code), code, count)
            for code, count in sorted(values.items(), key=lambda a: a[1], reverse=True)]
    mucode = ' '.join(code + re.sub(r'[|{]', '', code)
            for _, code, count in values_sorted)
    html = ''.join(t.to_html() for t in parse(text))
    return render_template("huse-result.html", values=values_sorted, mucode=mucode, html=html)

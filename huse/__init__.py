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
    codes = re.findall(r'[|{]\d{3}|[|{]=[a-z]', text)
    values = dict()
    for code in codes:
        values[code] = values.get(code, 0) + 1
    values_sorted = sorted(values.items(), key=lambda a: a[1], reverse=True)
    values_sorted = [(colorFromCode(code), code, count) for code, count in values_sorted]
    mucode = ' '.join(code + re.sub(r'[|{]', '', code) for _, code, count in values_sorted)
    return render_template("huse-result.html", values=values_sorted, mucode=mucode)

grayscale = dict(a='#000000',b='#080808',c='#121212',d='#1c1c1c',e='#262626',
                 f='#303030',g='#3a3a3a',h='#444444',i='#4e4e4e',j='#585858',
                 k='#626262',l='#6c6c6c',m='#767676',n='#808080',o='#8a8a8a',
                 p='#9e9e9e',q='#9e9e9e',r='#a8a8a8',s='#b2b2b2',t='#bcbcbc',
                 u='#c6c6c6',v='#d0d0d0',w='#dadada',x='#e4e4e4',y='#eeeeee',
                 z='#ffffff')

rgbDigit = {'0':'00','1':'5f','2':'87','3':'af','4':'d7','5':'ff'}

def colorFromCode(code):
    m = re.match(r'[|{](\d{3})', code)
    if m is not None:
        return '#' + ''.join(rgbDigit[digit] for digit in m.group(1))

    m = re.match(r'[|{]=([a-z])', code)
    if m is not None:
        return grayscale[m.group(1)]

    raise ValueError(f'"{code}" is not a valid code')

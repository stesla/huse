import re
import html

ANSI_CODE = r'([|{]\d{3}|[|{]=[a-z])'

GRAYSCALE = dict(a='#000000',b='#080808',c='#121212',d='#1c1c1c',e='#262626',
                 f='#303030',g='#3a3a3a',h='#444444',i='#4e4e4e',j='#585858',
                 k='#626262',l='#6c6c6c',m='#767676',n='#808080',o='#8a8a8a',
                 p='#9e9e9e',q='#9e9e9e',r='#a8a8a8',s='#b2b2b2',t='#bcbcbc',
                 u='#c6c6c6',v='#d0d0d0',w='#dadada',x='#e4e4e4',y='#eeeeee',
                 z='#ffffff')

RGB_DIGIT = {'0':'00','1':'5f','2':'87','3':'af','4':'d7','5':'ff'}

def colorFromCode(code):
    m = re.match(r'[|{](\d{3})', code)
    if m is not None:
        return '#' + ''.join(RGB_DIGIT[digit] for digit in m.group(1))

    m = re.match(r'[|{]=([a-z])', code)
    if m is not None:
        return GRAYSCALE[m.group(1)]

    raise ValueError(f'"{code}" is not a valid code')

def parse(string):
    string = re.sub(r'\|_', ' ', string)
    string = re.sub(r'\|/', '\n', string)
    t = re.split(ANSI_CODE, string)
    if t[0] == "":
        initial = []
    else:
        initial = [Text(t[0])]
    rest = [ColoredText(t[i], t[i+1]) for i in range(1,len(t),2)]
    return initial + rest

class Text:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'Text("{self.text}")'

    def __eq__(self, obj):
        if isinstance(obj, Text):
            return obj.text == self.text
        return False

    def to_html(self):
        return html.escape(self.text)

class ColoredText(Text):
    def __init__(self, code, text):
        Text.__init__(self, text)
        self.code = code

    def __repr__(self):
        return f'ColoredText("{self.code}", "{self.text}")'

    def __eq__(self, obj):
        if isinstance(obj, ColoredText):
            return obj.text == self.text and obj.code == self.code
        return False

    def to_html(self):
        text = Text.to_html(self)
        color = colorFromCode(self.code)
        return f'<span style="color: {color}">{text}</span>'

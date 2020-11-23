from huse.markup import *

def test_parse_empty():
    assert parse('') == []

def test_parse_plain():
    assert parse('foo bar baz') == [Text('foo bar baz')]

def test_parse_one_code():
    assert parse('foo |=wbar') == [Text('foo '), ColoredText('|=w', 'bar')]

def test_parse_more_codes():
    assert parse('foo |123bar |=qbaz') == [
            Text('foo '), 
            ColoredText('|123', 'bar '),
            ColoredText('|=q', 'baz')]

def test_parse_initial_code():
    assert parse('|123foo') == [ColoredText('|123', 'foo')]

def test_parse_space():
    assert parse('foo|_bar') == [Text('foo bar')]

def test_parse_newline():
    assert parse('foo|/bar') == [Text('foo\nbar')]

def test_plain_markup():
    assert Text('text').to_html() == 'text'

def test_rgb_markup():
    assert ColoredText('|555', 'bar').to_html() == '<span style="color: #ffffff">bar</span>'

def test_escapes():
    assert Text('<>').to_html() == '&lt;&gt;'

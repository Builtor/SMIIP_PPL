# -*-:coding:utf-8-*-

import os

from pyquery import PyQuery as pq
from lxml import etree
from bs4 import BeautifulSoup

def get_html_from_big_text(file_object):
    html_con = ''
    for one_line in file_object:
        # one_line = save_test.re_h.sub('', one_line)
        if '<!DOCTYPE html>' not in one_line:
            html_con += one_line
        else:
            yield html_con
            html_con = ''
            html_con += one_line
    yield html_con


def beau_filter(f_in, f_out):
    for one_html in get_html_from_big_text(f_in):
        soup = BeautifulSoup(one_html)
        # print soup.get_text()
        for con in soup.find_all('div'):
            if is_chinese(con.string):
                line_data = con.string + '\n'
                print line_data
                f_out.write(line_data.encode('utf-8'))


def is_chinese(con_string):
    count = 0
    # print con_string
    if con_string is None:
        return False

    for chars in con_string:
        num = ord(chars)
        # a:97 z:122 A:65 Z:90
        if num > 65 and num < 122:
            count += 1
    res = True
    if len(con_string) < 1:
        res = False
    orbit = 1.0 * count / len(con_string)
    if orbit > 0.3:
        res = False
    return res


if __name__ == '__main__':
    with open('../htmltest.txt') as f:
        # beau_filter(f, open('res_tokenize/bs.txt', 'w'))
        for one_html in get_html_from_big_text(f):
            if len(one_html) > 10:
                d = pq(one_html)
                print d('div').text()


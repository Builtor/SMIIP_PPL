#! /usr/bin/python
#  encoding=utf-8

import sys
import jieba
import re
from pyltp import Segmentor

reload(sys)
sys.setdefaultencoding('utf-8')

debugInfo = True
UNKSYMBOL = u'<UNK>'

## 阿拉伯数字转中文, 比如1204转一千二百零四
def digit2Cn(text):
    if not isinstance(text, basestring):
        try:
            text = text.group()
        except Exception as e:
            text = ""
    text = str(int(text))
    cnstr = ""
    end = len(text)
    unit = [u'', u'十', u'百', u'千']
    number = [u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九']

    def allzero(ns):
        flag = True
        for n in range(0, len(ns)):
            if ns[n] != '0':
                flag = False
        return flag

    if allzero(text):
        if len(text) == 1:
            return number[0]
        else:
            return ""

    for i in range(0, len(text)):
        toadd = ""
        if end - i > 0:
            substr = text[i+1:end]
            if not (i == 0 and end - i == 2 and text[i] == '1'):
                toadd += number[int(text[i])]
            if text[i] != '0':
                toadd += unit[end - i - 1]
            if allzero(substr):
                cnstr += toadd
                break
            elif text[i] == '0' and i + 1 < len(text) and text[i + 1] == '0':
                continue
        else:
            toadd += number[int(text[i])]
        cnstr += toadd
    return cnstr

## 数字转中文, 2017转二零一七
def num2Cn(text):
    number = [u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九']
    numstr = ""
    if not isinstance(text, basestring):
        try:
            text = text.group()
        except Exception as e:
            text = ""
    for i in range(0, len(text)):
        numstr += number[int(text[i])]
    return numstr

## 多位数字带小数点的转中文
# 有bug 输入49510000 输出 四千九百五十一万零; 9E -> 九亿零万零 fixed by lhb
def ldigit2Cn(text):
    # 没有小数点默认大于十亿就不处理了
    if len(text) > 10:
        return u''
    unit = ['点', '万', '亿']
    cnstr = ""
    # 用小数点分割后，分别对点前后的数字进行处理
    if '.' in text:
        dotIndex = text.index('.')
        cnstr += ldigit2Cn(text[0:dotIndex]) + unit[0] + num2Cn(text[dotIndex + 1:len(text)])
    else:
        strlen = len(text)
        # 千万
        if strlen <= 8:
            if text[-8:] == '00000000':
                return ''
            # 万
            if strlen <= 4:
                cnstr += digit2Cn(text)
            else:
                # 将万 前 后分开， 并给前面的先处理
                subcnstr = digit2Cn(text[0:strlen - 4])
                # 如果前面不为0，都处理，否则只处理后四位
                if subcnstr != "":
                    last_four = text[-4:]
                    if last_four == '0000':
                        cnstr += digit2Cn(text[0:strlen - 4]) + unit[1]
                    else:
                        cnstr += digit2Cn(text[0:strlen - 4]) + unit[1] + digit2Cn(text[-4:])
                else:
                    cnstr += digit2Cn(text[-4:])
        else:
            # 亿之前 和 之后，之后用递归
            cnstr += ldigit2Cn(text[0:strlen - 8]) + unit[2] + ldigit2Cn(text[-8:])
    return cnstr

# 如果有多个匹配结果，会一直调用？？每次匹配正则的字符串就进行替换一次
def ip2cn(match_str):
    # 将整个匹配到的str分割后给到sgm
    sgm = match_str.group(0).split(u'.')
    if len(sgm) != 4:
        return ""
    else:
        return u'点'.join((num2Cn(i) for i in sgm))

# 输入类似2017/7/7
def date(match_obj):
    # match_obj里面有所有数据集str，对str做正则，返回前三个
    year, month, day = re.split(ur'[^\d]', match_obj.group())[:3]
    return num2Cn(year) + u'年' + digit2Cn(month) + u'月' + digit2Cn(day) + u'日'

#先处理中文 2017年12月30日，后处理2017/3/3
def date2cn(text):
    assert isinstance(text, unicode)
    # \d等价于 [0-9] 2017.3.3 2017-3-3 2017/3/3
    date_ptn = ur'[1-9][\d]{3}[\-\/\.](1[012]|[0]?[1-9])[\-\/\.]([12][0-9]|3[01]|[0]?[1-9])'
    #
    text = re.sub(ur'[1-9][0-9]{3}[年]', lambda t: re.sub(ur'[\d]+', num2Cn, t.group()), text)
    #
    text = re.sub(ur'(1[012]|[0]?[1-9])[月][份]?', lambda t : re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    #
    text = re.sub(ur'([12][0-9]|3[01]|[0]?[1-9])[日号]', lambda t: re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    #
    text = re.sub(date_ptn, date, text)
    return text

def timeFormator(match_obj):
    t = match_obj.group().split(':')[:3]
    if len(t) == 2:
        return digit2Cn(t[0]) + u'点' + digit2Cn(t[1]) + u'分'
    return digit2Cn(t[0]) + u'点' + digit2Cn(t[1]) + u'分' + digit2Cn(t[2]) + u'秒'


# 输入格式 21:12
# 先处理中文，21点13分，后处理纯数字
def time2cn(text):
    assert isinstance(text, unicode)
    time_ptn = ur'(1[0-9]|[2][0-4]|0?[0-9])(\:([1-5][0-9]|0?[0-9]))+'
    text = re.sub(ur'(1[0-9]|[2][0-4]|0?[0-9])[时点][钟整]?', lambda t: re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    text = re.sub(ur'([1-5][0-9]|0?[0-9])[分][钟整]?', lambda t: re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    text = re.sub(ur'([1-5][0-9]|0?[0-9])[秒][钟整]?', lambda t: re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    text = re.sub(time_ptn, timeFormator, text)
    return text


num_set = {u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八',
           u'九', u'十', u'百', u'千', u'万', u'亿', u'个', u'点', u'分', u'秒'}
def filter_pure_num(text):
    pure = True
    for word in text:
        if word not in num_set:
            pure = False
    if pure:
        return ''
    else:
        return text


# 传入的应该是一个txt中的所有内容
def textFormator(text):
    # 过滤非法字符
    # XML标准规定的无效字节为：
    # 0x00 – 0x08
    # 0x0b – 0x0c
    # 0x0e – 0x1f
    text = re.sub(ur'[\x05-\x08\x0b-\x1f\x7f]', u'', text)
    # 全角Latin
    # 全角模式：输入一个字符占用2个字符，  半角模式：输入一个字符占用1个字符。
    # 全角模式输出的字符和半角不同，但是汉字的话2个模式都是占用2个字符
    # 看了半天应该是全角转半角。。
    text = re.sub(ur'[\uFF01-\uFF5E]+', lambda t: ''.join(map(lambda c: unichr(ord(c)-0xfee0), t.group())), text)
    IP = ur'([0-9]{1,3}\.){3}[0-9]{1,3}'
    url = ur'&nbsp|(http[s]?\:|www\.|[\w\d\.]+\@)?.+\.(org|com|cn|php|htm[l]?|net)[^\u4e00-\u9fff]*'
    path = ur'([a-zA-Z]\:)?(\\[\d\w\-\+\=\.\~ ]+)+|(\/[\d\w\-\+\=\.\~ ]+)+\
                |ftp\:((\\[\d\w\-\+\.\=\~ ]*)+|(\/[\d\w\-\+\.\=\~ ]*)+)'
    percent = ur'[\d]+([\.][\d]+)?\%'
    # 1 转IP
    text = re.sub(IP, ip2cn, text)
    # 2 转日期
    text = date2cn(text)
    # 3 转时间
    text = time2cn(text)
    # 4 除去网址，绝对路径等  \u3000中文(全角)空格
    text = re.sub('|'.join((url, path, ur'[、《》\u3000]')), u'', text)
    # 5 转百分数
    text = re.sub(percent, lambda t: u'百分之' + ldigit2Cn(t.group(0)[0:-1]), text)
    # 6 转小数
    text = re.sub(ur'\d+(\.\d+)?', lambda t: ldigit2Cn(t.group(0)), text)
    # 7 将标点符号转换行
    text = re.sub(ur'[\(\)\[\]【】（）\{\}「」,\.\?，。？;\!！；“”"]', u'\n', text)
    # # 7.1 将标点符号转换行
    # text = re.sub(ur'[\(\)\[\]【】（）\{\}「」,;；“”"]', u'', text)
    # # 7.2 将标点符号转换行
    # text = re.sub(ur'[\.\?，。？\!！]', u'\n', text)
    # 8 \u4e00-\u9fff 中文
    # 模板：对每一行，因为他的字符串是一整个变量来的， strip默认移除头尾空格
    # 如果找到中文且长度大于1返回本身，否则返回空字符串，除去英文等字母
    # 为什么会过滤掉 四千九百五十一万零?
    # 传入的lambda参数类型是march obj
    text = re.sub(ur'[^\n]*\n', lambda t: t.group() if len(t.group().strip()) > 1 and not re.search(ur'[^\u4e00-\u9fff\n]', t.group().strip()) else '', text)
    return text


def processing(text_path, out_path, buffsize=100000):
    out = open(out_path, 'w')
    with open(text_path) as readf:
        # 返回一个生成器，来循环操作文件的每一行。
        rfgen = readf.xreadlines()
        while True:
            buff = ""
            done = False
            for i in xrange(buffsize):
                try:
                    buff += rfgen.next()
                except StopIteration as e:
                    done = True
                    break
            buff = textFormator(buff.decode('utf-8'))
            out.write(buff.encode('utf-8'))
            if done:
                break
    out.close()


def jieba_tokenize(userdict_path, text_path, out_path, buffsize=100000, useUNK=True, jiebaThreads=5):
    #jieba.enable_parallel(jiebaThreads)
    #jieba.set_dictionary('dict.txt.small')
    with file(userdict_path) as rf:
        words_set = set(rf.read().decode('utf-8').splitlines())
    words_set.add(u'\n')
    out = file(out_path, 'w')
    with open(text_path) as readf:
        rfgen = readf.xreadlines()
        while True:
            done = False
            buff = ""
            for i in xrange(buffsize):
                try:
                    buff += rfgen.next()
                except StopIteration as e:
                    done = True
                    break
            buff = buff.decode('utf-8')
            # token ....
            allwords = jieba.lcut(buff, HMM=False)
            if useUNK:
                for i, w in enumerate(allwords):
                    if w not in words_set:
                        allwords[i] = ' '.join(map(lambda x: x if x in words_set else UNKSYMBOL, w))
            buff = u' '.join(allwords)
            buff = re.sub(ur' \n ', u'\n', buff)
            out.write(buff.encode('utf-8'))
            if done:
                break
    out.close()

def ltp_tokenize(userdict_path, text_path, out_path, model_path, buffsize=100000, useUNK=True):
    segmentor = Segmentor()
    segmentor.load(model_path)

    with file(userdict_path) as rf:
        words_set = set(rf.read().decode('utf-8').splitlines())
    words_set.add(u'\n')
    out = file(out_path, 'w')
    with open(text_path) as readf:
        rfgen = readf.xreadlines()
        while True:
            done = False
            buff = ""
            for i in xrange(buffsize):
                try:
                    buff += rfgen.next()
                except StopIteration as e:
                    done = True
                    break
            buff = buff.decode('utf-8')
            # token ....
            allwords = segmentor.segment(buff)
            if useUNK:
                for i, w in enumerate(allwords):
                    if w not in words_set:
                        allwords[i] = ' '.join(map(lambda x: x if x in words_set else UNKSYMBOL, w))
            buff = u' '.join(allwords)
            buff = re.sub(ur' \n ', u'\n', buff)
            # print buff
            out.write(buff.encode('utf-8'))
            if done:
                break
    out.close()

# text_path = sys.argv[1]
# out_path = sys.argv[2]

# text_path = 'part.txt'
# out_path = '5.txt'
# processing(text_path, out_path)
# print "Done! Thank you!"

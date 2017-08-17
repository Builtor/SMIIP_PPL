# -*- coding: utf-8 -*-
from pyltp import Segmentor
import jieba
import re
import thulac
import pynlpir
UNKSYMBOL = u'<UNK>'


def get_words_set(words_set_path):
    words_set = open(words_set_path)
    # splitlines() 按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表
    # 将每个词都作为set的一个元素
    words_set = set(words_set.read().decode('utf-8').splitlines())
    words_set_without_num = set(map(lambda x: x.split(' ')[0], words_set))
    words_set_without_num.add(u'\n')
    return words_set_without_num


def ltp_tokenize2(words_set, sentence, useUNK=True, jiebaThreads=5):
    #jieba.enable_parallel(jiebaThreads)
    #jieba.set_dictionary('dict.txt.small')

    # token ....
    #一个buff的词语用于分词，第i个不在词典里，
    allwords = jieba.lcut(sentence, HMM=False)
    if useUNK:
        for i, w in enumerate(allwords):
            # w是数据集的每一句话？每一个词看起来比较像
            if w not in words_set:
                # 如果词不在词典里，那就对每一个字都单独做判断
                #以sep作为分隔符，将seq所有的元素合并成一个新的字符串
                allwords[i] = ' '.join(map(lambda x: x if x in words_set else UNKSYMBOL, w))
    buff = u' '.join(allwords)
    buff = re.sub(ur' \n ', u'\n', buff)
    return buff


segmentor = Segmentor()
def load_ltp_model(path):
    segmentor.load(path)


def ltp_tokenize(words_set, sentence, useUNK=True):
    allwords = list(segmentor.segment(sentence.encode('utf-8')))
    allwords = map(lambda x: x.decode('utf-8'), allwords)
    if useUNK:
        for i, w in enumerate(allwords):
            # w是数据集的每一句话？每一个词看起来比较像
            # print w
            if w not in words_set:
                # 如果词不在词典里，那就对每一个字都单独做判断
                #以sep作为分隔符，将seq所有的元素合并成一个新的字符串
                allwords[i] = ' '.join(map(lambda x: x if x in words_set else UNKSYMBOL, w))
    buff = u' '.join(allwords)
    buff = re.sub(ur' \n ', u'\n', buff)
    return buff


def jieba_tokenize2(words_set, sentence, useUNK=True):
    #一个buff的词语用于分词，第i个不在词典里，
    allwords = jieba.lcut(sentence, HMM=False)
    if useUNK:
        for i, w in enumerate(allwords):
            # w是数据集的每一句话？每一个词看起来比较像
            if w not in words_set:
                # 如果词不在词典里，那就对每一个字都单独做判断
                #以sep作为分隔符，将seq所有的元素合并成一个新的字符串
                allwords[i] = ' '.join(map(lambda x: x if x in words_set else UNKSYMBOL, w))
    buff = u' '.join(allwords)
    buff = re.sub(ur' \n ', u'\n', buff)
    return buff.lstrip()
    # out_file.write(buff.encode('utf-8'))

thu_cls = thulac.thulac(seg_only=True)
def thulac_tokenize(words_set, sentence, useUNK=True):
    res = thu_cls.cut(sentence, text=False)
    all_words = map(lambda x: x[0].decode('utf-8'), res)
    if useUNK:
        for i, w in enumerate(all_words):
            if w not in words_set:
                all_words[i] = ' '.join(map(lambda x: x if x in words_set else UNKSYMBOL, w))
    buff = u' '.join(all_words)
    buff = re.sub(ur' \n ', u'\n', buff)
    return buff


# pynlpir.open()
def nlpir_tokenize(words_set, sentence, useUNK=True):
    allwords = pynlpir.segment(sentence, pos_tagging=False)
    if useUNK:
        for i, w in enumerate(allwords):
            # w是数据集的每一句话？每一个词看起来比较像
            if w not in words_set:
                # 如果词不在词典里，那就对每一个字都单独做判断
                #以sep作为分隔符，将seq所有的元素合并成一个新的字符串
                allwords[i] = ' '.join(map(lambda x: x if x in words_set else UNKSYMBOL, w))
    buff = u' '.join(allwords)
    buff = re.sub(ur' \n ', u'\n', buff)
    return buff

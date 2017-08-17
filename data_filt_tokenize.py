# encoding=utf-8
import data_filter
import all_tokenize as at
import os

words_set = at.get_words_set('words/words.txt')
if not os.path.exists('res_tokenize_hudong'):
    os.mkdir('res_tokenize_hudong')


def jieba_tk():
    jieba_res = open('res_tokenize/jieba_res_v1.txt', 'w')


def ltp_tk():
    ltp_res = open('res_tokenize/ltp_res_v1.txt', 'w')


def thulac_tk():
    thulac_res = open('res_tokenize/thulac_res_v1.txt', 'w')


def nlpir_tk():
    nlpir_res = open('res_tokenize/nlpir_res_v1.txt', 'w')

if __name__ == '__main__':
    # 没有文件创造文件
    jieba_res = open('res_tokenize_hudong/jieba_res_v1.txt', 'w')

    at.load_ltp_model('cws.model')
    ltp_res = open('res_tokenize_hudong/ltp_res_v1.txt', 'w')

    thulac_res = open('res_tokenize_hudong/thulac_res_v1.txt', 'w')

    nlpir_res = open('res_tokenize_hudong/nlpir_res_v1.txt', 'w')

    pre_path = '/home/intern2017/huangyj/data/baike_data/part-r-000'
    text_path = '/home/intern2017/huangyj/data/hu_data/hudong_train.txt'

    with open(text_path) as f:
        rfgen = f.xreadlines()
        for pyin in rfgen:
            # 处理完标签后的数据，未分词，pyin是str类型，用decode utf8解码，可encode变回去str
            buff = data_filter.textFormator(pyin.decode('utf-8'))
            buff = buff.replace(' ', '').strip()
            buff = data_filter.filter_pure_num(buff)
            if len(buff) < 2:
                # print buff
                continue
            ltp_res.write(at.ltp_tokenize(words_set, buff, True))
            # nlpir_res.write(at.nlpir_tokenize(words_set, buff, True))
            thulac_res.write(at.thulac_tokenize(words_set, buff, True))
            jieba_res.write(at.jieba_tokenize2(words_set, buff, False))
    print 'done'

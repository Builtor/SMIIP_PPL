# encoding=utf-8
import data_filter
import all_tokenize as at
import os

words_set = at.get_words_set('words/words.txt')
if not os.path.exists('res_tokenize'):
    os.mkdir('res_tokenize')

def jieba_tk():
    jieba_res = open('res_tokenize/jieba_res_v1.txt', 'w')


def ltp_tk():
    ltp_res = open('res_tokenize/ltp_res_v1.txt', 'w')


def thulac_tk():
    thulac_res = open('res_tokenize/thulac_res_v1.txt', 'w')


def nlpir_tk():
    nlpir_res = open('res_tokenize/nlpir_res_v1.txt', 'w')

if __name__ == '__main__':
    jieba_res = open('res_tokenize/jieba_res_v1.txt', 'w')
    ltp_res = open('res_tokenize/ltp_res_v1.txt', 'w')
    thulac_res = open('res_tokenize/thulac_res_v1.txt', 'w')
    nlpir_res = open('res_tokenize/nlpir_res_v1.txt', 'w')
    for i in range(1, 32):
        pre_path = '/home/intern2017/huangyj/data/baike_data/part-r-000'

        if i <= 9:
            text_path = pre_path + '0' + str(i)
        else:
            text_path = pre_path + str(i)
        # processing(text_path, out_path)

        with open("../htmltest.txt") as f:
            rfgen = f.xreadlines()
            for pyin in rfgen:
                # 处理完标签后的数据，未分词，pyin是str类型，用decode utf8解码，可encode变回去str
                buff = data_filter.textFormator(pyin.decode('utf-8'))
                # buff = buff.replace('\n', '')
                buff = buff.replace(' ', '').strip()
                buff = data_filter.filter_pure_num(buff)
                if len(buff) < 2:
                    # print buff
                    continue
                # todo:分词，将不同的分词方法保存在不同的路径下
                ltp_res.write(at.ltp_tokenize(words_set, buff, True))
                # nlpir_res.write(at.nlpir_tokenize(words_set, buff, True))
                thulac_res.write(at.thulac_tokenize(words_set, buff, True))
                jieba_res.write(at.jieba_tokenize2(words_set, buff, False))
        print 'done'
        break

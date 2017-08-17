# encoding=utf-8
import data_filter
import all_tokenize as at
import os

words_set = at.get_words_set('words/words.txt')
if not os.path.exists('res_tokenize_mul'):
    os.mkdir('res_tokenize_mul')


def mul_pro(text_in, text_out_num):
    reload(at)



if __name__ == '__main__':
    at.load_ltp_model('../cws.model')
    num = '16'
    text_out_num = num
    jieba_res = open('res_tokenize_mul/jieba_res_'+ text_out_num + '.txt', 'w')
    ltp_res = open('res_tokenize_mul/ltp_res_'+ text_out_num + '.txt', 'w')
    thulac_res = open('res_tokenize_mul/thulac_res_'+ text_out_num + '.txt', 'w')
    nlpir_res = open('res_tokenize_mul/nlpir_res_'+ text_out_num + '.txt', 'w')

    pre_path = '/home/intern2017/huangyj/data/baike_data/part-r-000'
    pre_path = 'local_test/part-r-000'

    with open(pre_path + num) as f:
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
            jieba_res.write(at.jieba_tokenize2(words_set, buff, True))
    print 'done', text_out_num

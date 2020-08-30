#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 30/9/2016 8:41 PM
# @Author  : GUO Ganggang
# @email   : ganggangguo@csu.edu.cn
# @Site    :
# @File    : obtain_train_data.py
# @Software: PyCharm

import graphlab as gl
import codecs
from itertools import islice
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TopicModel:
    def trainModel(self, trained_file, train_field, model_saved_name, num_topics, num_iterations, method='auto',
                   beta=0.01, delimiter="\t"):
        train_data = gl.SFrame.read_csv(trained_file, delimiter, header=True)
        print train_data
        train_bag = gl.text_analytics.count_words(train_data[train_field])
        train_model = gl.topic_model.create(train_bag, num_topics=num_topics, num_iterations=num_iterations, beta=beta,
                                            method=method, verbose=True)
        train_model.save(model_saved_name)
        return train_model
    # def predict(self,train_model,test_file,test_field,test_result_field,test_output_file,delimiter = " "):
    #     test_data = gl.SFrame.read_csv(test_file,delimiter = delimiter,header = True)
    #     test_bag = gl.text_analytics.count_words(test_data[test_field])
    #     test_data[test_result_field] = train_model.predict(test_bag)
    #     test_data.save(test_output_file)


def dealwithData(inFilePath,outFilePath):
    with codecs.open(outFilePath, "w", "utf-8") as output_file:
        output_file.write('uid' + '\t' + 'text' + '\n')
        with codecs.open(inFilePath, "rb", "utf-8") as inHandle:
            for line in inHandle:
                temp = line.strip().split(' ')
                uid = temp[0]
                text = " ".join(temp[1:])
                output_file.write(uid + '\t' + text + '\n')

def showLDAtopicSep(input_file,output_file):
    weibo_model = gl.load_model(input_file)
    topics_words = weibo_model.get_topics(num_words=200, output_type='topic_words')
    print topics_words
    topics_words.save(output_file)


def prediction_weibo_LDA(prediction_model_filePath,data_filepath,output_filepath):

    weibo_LDA_model = gl.load_model(prediction_model_filePath)

    weibo_train_data = gl.SFrame.read_csv(data_filepath, delimiter=",", header=True)
    weibo_model_bag = gl.text_analytics.count_words(weibo_train_data['text'])

    weibo_train_data ['weibo_topic'] = weibo_LDA_model.predict(weibo_model_bag)
    weibo_train_data['weibo_topic_probability'] = weibo_LDA_model.predict(weibo_model_bag, output_type='probability')

    weibo_train_data.remove_column('text')
    weibo_train_data.save(output_filepath)



# 按uid 对每位用户的每条微博的主题进行统计,并根据各个主题出现次数多少，输出前5个

def static_LDATopic_merge(inFilePath_1,inFilePath_2,output_path,first_k):
    topic_num = {}
    with codecs.open(inFilePath_1, "rb", "utf-8") as inputfile:
        num = 0
        for line in islice(inputfile.readlines(), 1, None):
            temp = line.strip()
            topic_num[str(num)] = temp
            num += 1

    with codecs.open(output_path, "w", "utf-8") as output_handler:
        # output_handler.write('topics' + ',' + 'numbers' + '\n')
        static_num = {}
        with codecs.open(inFilePath_2, "rb", "utf-8") as input_file:
            for line in islice(input_file.readlines(), 1, None):
                temp_sec = line.strip().split(',')
                static_num[temp_sec[0]] = static_num.get(temp_sec[0], 0) + 1
        lda_sort = sorted(static_num.iteritems(), key=lambda d: d[1], reverse=True)

        if first_k > len(lda_sort):
            first_k = len(lda_sort)

        for j in range(first_k):
            print lda_sort[j][0], lda_sort[j][1]
            output_handler.write(str(lda_sort[j][0])+ ',' + str(lda_sort[j][1]) + ',' + topic_num[str(lda_sort[j][0])] + '\n')





def static_LDATopic(inFilePath_1,inFilePath_2,output_path):

    with codecs.open(output_path, "w", "utf-8") as output_handler:
        # output_handler.write('topics' + ',' + 'numbers' + '\n')
        with codecs.open(inFilePath_1, "rb", "utf-8") as inputfile:
            for line in islice(inputfile.readlines(), 1, None):
                temp_fir = line.strip().split(',')
                static_num = {}
                with codecs.open(inFilePath_2, "rb", "utf-8") as input_file:
                    for line in islice(input_file.readlines(), 1, None):
                        temp_sec = line.strip().split(',')
                        if temp_sec[0] == temp_fir[0]:
                            static_num[temp_sec[1]] = static_num.get(temp_sec[1], 0) + 1
                lda_sort = sorted(static_num.iteritems(), key=lambda d: d[1], reverse=True)

                # print len(lda_sort)
                if len(lda_sort) >= 3:
                    length_list = 3
                else:
                    print len(lda_sort)
                    length_list = len(lda_sort)
                topics_first_3 = []
                for j in range(length_list):
                    # print lda_sort[j][0], lda_sort[j][1]
                    topics_first_3.append(lda_sort[j][0])
                topics_first_3_str = ','.join(topics_first_3)
                output_handler.write(str(temp_fir[0])+ ','+ topics_first_3_str + '\n')



def merge_lda_topics(inFilePath_1,inFilePath_2,outFilePath):
    topic_words = {}
    flag = 0
    with codecs.open(inFilePath_1, "rb", "utf-8") as input_file:
        for line in islice(input_file.readlines(), 1, None):
            temp = line.strip().split('\t')
            words = ','.join(temp)
            # print words
            topic_words[str(flag)] = words
            flag += 1
    with open(outFilePath, 'w') as output_file:
        with codecs.open(inFilePath_2, "rb", "utf-8") as input_file:
            for line in islice(input_file.readlines(), 1, None):
                temp = line.strip().split(',')
                print str(temp[0])
                print topic_words[str(temp[0])]

                output_file.write(str(temp[0]) +','+ topic_words[str(temp[0])] + '\n')





if __name__ == "__main__":
    # dealwithData(inFilePath, outFilePath)
    # filePath = 'D:\\pingan_stock\\pingan_stock_undervalueed\\'
    filePath = 'D:\\pingan_stock\\pingan_stock_undervalueed\\0407\\'
    train_file = filePath + 'stock_weibo_seg_clean_3words.csv'
    train_field = 'text'
    model_saved_name = filePath + 'stock_weibo_LDA_model'
    topic_model = TopicModel()
    train_model = topic_model.trainModel(train_file,train_field,model_saved_name,num_topics = 200,num_iterations = 1000)
    print train_model.get_topics()


    # filePath = 'D:\\incomeLevelPrediction\\db_file\\'
    input_file = filePath + 'stock_weibo_LDA_model'
    output_file = filePath + 'stock_weibo_LDA_model_200topics.csv'

    showLDAtopicSep(input_file,output_file)

    prediction_model_filePath =filePath + 'stock_weibo_LDA_model'
    data_filepath =filePath + 'pingan_stock_weibo_seg_clean_3words.csv'
    output_filepath = filePath + 'pingan_stock_weibo_seg_clean_3words_LDA.csv'
    prediction_weibo_LDA(prediction_model_filePath, data_filepath, output_filepath)

    first_k = 10
    input_file_1 = filePath + 'stock_weibo_LDA_model_200topics.csv'
    input_file_2 = filePath + 'pingan_stock_weibo_seg_clean_3words_LDA.csv'
    output_file = filePath + 'pingan_stock_weibo_seg_clean_3words_LDA_static_10first_topics.csv'
    static_LDATopic_merge(input_file_1, input_file_2, output_file,first_k)


    # filePath = 'D:\\pingan_stock\\pingan_stock_undervalueed\\0330\\3words\\'
    # input_file_1 = filePath + '601318_satisfied_conditions_large_change_and_highest_volume.csv'
    # input_file_2 = filePath + 'eastmoney_guba_post_pingan_hs_seg_clean_3words_dividedText_LDA.csv'
    # output_file = filePath + 'bbs_LDA_topics_static_first3.csv'
    # static_LDATopic(input_file_1, input_file_2, output_file)

    # input_file_1 = filePath + 'stock_news\\financial_news_LDA_model_topics.csv'
    # input_file_2 = filePath + 'stock_news\\guangda_news_seg_clean_3words_LDA_static.csv'
    # output_file = filePath + 'stock_news\\guangda_news_LDA_topics_static_first30.csv'
    # merge_lda_topics(input_file_1,input_file_2,output_file)



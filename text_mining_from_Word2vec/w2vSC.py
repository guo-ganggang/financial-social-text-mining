#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os.path
import sys
import multiprocessing
from gensim import utils
import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import codecs
import time
import re
from itertools import islice


def baseDate_static(ipath,inFilePath_1,inFilePath_2,outFilePath):

    model = gensim.models.Word2Vec.load_word2vec_format(ipath, binary=False)
    with open(outFilePath, 'w') as output_file:
        features = []
        for f in range(200):
            features.append('f_bbs_'+str(f))
        title = ','.join(features)
        output_file.write('date' + ',' + title + ',' + 'number' + '\n')
        with codecs.open(inFilePath_1, "rb", "utf-8") as inputfile_1:
            first_first_date = '2010-01-01 00:00'
            first_date = time.strptime(first_first_date, "%Y-%m-%d %H:%M")
            first_date_stam = time.mktime(first_date)
            # flag = 0
            for line_1 in islice(inputfile_1.readlines(), 1, None):
                temp_1 = line_1.strip().split(',')
                temp_temp = temp_1[0] + ' 15:00'
                print temp_1[0]
                end_date = time.strptime(temp_temp, "%d/%m/%Y %H:%M")
                # print end_date
                end_date_stam = time.mktime(end_date)
                sumNum = 0
                inint_list = []
                for i in range(200):
                    inint_list.append(0.0)
                with codecs.open(inFilePath_2, "rb", "utf-8") as inputfile_2:
                    for line_2 in inputfile_2.readlines():
                        temp_2 = line_2.strip().split('\t')
                        # print temp_2[0]
                        # everyLineDate = re.sub(u'﻿','',temp_2[0])
                        everyLineDate = temp_2[0]
                        # everyLineDate = temp_2[0][1:]
                        # print everyLineDate
                        if everyLineDate == '0000-00-00 00:00':
                            continue
                        # print everyLineDate
                        dateFormat = time.strptime(everyLineDate, "%Y-%m-%d %H:%M")
                        Timestamp = time.mktime(dateFormat)
                        if (first_date_stam <= Timestamp < end_date_stam):
                            sumNum += 1
                            # print everyLineDate
                            temp_3 = temp_2[1].strip().split(' ')
                            for j in range(len(temp_3)):
                                char = utils.to_unicode(temp_3[j])
                                # if u'\u4e00' <= char <= u'\u9fff':
                                    # print temp_3[j]
                                try:
                                    temp_list = model[char]
                                except KeyError:
                                    continue
                                else:
                                    print "Unexpected error:", sys.exc_info()[0]
                                inint_list = list(map(lambda x: x[0] + x[1], zip(inint_list,temp_list)))
                                # print inint_list
                                # else:
                                #     continue
                        else:
                            continue
                     #
                # if sumNum == 0:
                #     flag += 1
                #     print temp_1[0]
                final_list = ','.join(str(v) for v in inint_list)
                output_file.write(temp_1[0] + ',' + final_list+ ',' + str(sumNum) + '\n')
                first_date_stam = end_date_stam
            # print flag




if __name__ == '__main__':
    # program = os.path.basename(sys.argv[0])
    # logger = logging.getLogger(program)
    #
    # logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    # logging.root.setLevel(level=logging.INFO)
    # logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments

    # inp = 'D:\\pingan_stock\\financial_bbs\\eastmoney_guba_post_seg_clean_3words.csv'
    # outp1 = 'D:\\pingan_stock\\financial_bbs\\word2vec\\sg0_s200_w3_m2_3words.bin'
    # outp2 = 'D:\\pingan_stock\\financial_bbs\\word2vec\\sg0_s200_w3_m2_3words.vector'

    # model = Word2Vec(LineSentence(inp), size=200,window=5,min_count=100,
    #         workers=multiprocessing.cpu_count(), hs=1, negative=0)

    # model = Word2Vec(LineSentence(inp),sg = 0, size=200,window=3,min_count=2,
    #         workers=multiprocessing.cpu_count(), hs=1, negative=3,sample = 1e-4)

    # trim unneeded model memory = use(much) less RAM
    #model.init_sims(replace=True)
    # model.save_word2vec_format(outp2, binary=False)
    # model.save(outp1)

    filePath = 'D:\\pingan_stock\\financial_bbs\\'
    ipath = filePath + 'word2vec\\sg0_s200_w3_m2_3words.vector'
    inFilePath_1 = filePath + 'mergeData_classification_601318.csv'
    inFilePath_2 = filePath + 'eastmoney_guba_post_pingan_hs_seg_clean_1words.csv'
    outFilePath = filePath + '601318_pingan_financialBBS_feature.csv'
    baseDate_static(ipath, inFilePath_1, inFilePath_2, outFilePath)
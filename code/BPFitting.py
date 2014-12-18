# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 00:15:09 2014

@author: fuz
"""

import csv
    
def loadCSV(fi):
    reader = csv.reader(file(fi),delimiter='\t',skipinitialspace=True)
    records = [record for record in reader]
    return records[1:]
    

def loadBorrowHistory(fi):
    bhist = {}
    for semester,uid,bid,date,_ in loadCSV(fi):
        uid = int(uid)
        if bhist.has_key(uid):
            bhist[uid].append([int(semester),int(bid),date])
        else:
            bhist[uid] = [[int(semester),int(bid),date]]
    return bhist
    
def loadLibraryHistory(fi):
    lhist = {}
    for semester,uid,date,time,_ in loadCSV(fi):
        uid = int(uid)
        if lhist.has_key(uid):
            lhist[uid].append([int(semester),date,time])
        else:
            lhist[uid] = [[int(semester),date,time]]
    return lhist

def loadConsumeHistory(fi):
    chist = {}
    for semester,uid,loc,date,time,amount in loadCSV(fi):
        uid = int(uid)
        if chist.has_key(uid):
            chist[uid].append([int(semester),date,time,float(amount),loc])
        else:
            chist[uid] = [[int(semester),date,time,float(amount),loc]]
    return chist
    
def loadGrade(fi):
    grade = {}
    for semester,uid,rank,_ in loadCSV(fi):
        uid = int(uid)
        if grade.has_key(uid):
            grade[uid].update({int(semester):int(rank)})
        else:
            grade[uid] = {int(semester):int(rank)}
    return grade
    


def loadTrainingData(data_dir):
    bhist = loadBorrowHistory(data_dir+'/借书.txt')
    lhist = loadLibraryHistory(data_dir+'/图书馆门禁.txt')
    chist = loadConsumeHistory(data_dir+'/消费.txt')
    grade = loadGrade(data_dir+'/成绩.txt')

    print len(bhist),len(lhist),len(chist),len(grade)

    students = set({}).union(bhist,lhist,chist,grade)
    urecords = {}
    def _getitem_func(key):
        def _func(dic):
            if dic.has_key(key):
                return dic[key]
            else:
                return None
        return _func
    for uid in students:
        urecords[uid] = map(_getitem_func(uid),[bhist,lhist,chist,grade])
    return urecords


def reduceData(data):
    rdata = []
    def _len(d):
        if d is None:
            return 0
        return len(d)
        
    for u,[bhist,lhist,chist,grade] in data.items():
        rrecord = [_len(bhist),_len(lhist),_len(chist),grade[1],grade[2]]
        rdata.append((rrecord,grade[3]))
    
    _max = map(float,map(max, [[x[i] for x,y in rdata] for i in range(5)]))
    rdata = [[divide(x,_max).tolist(),float(y)/538] for x,y in rdata]
    return rdata
        

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import *

def annFitting(rdata):
    dataset = SupervisedDataSet(5,1)
    for x,y in rdata:
        dataset.addSample(x,y)
    
    net = buildNetwork(5,20,1)
    trainer = BackpropTrainer(net,dataset,
                              verbose=True,
                              learningrate=0.1)    
    return net,trainer
    
def loadTestingData(data_dir):
    bhist = loadBorrowHistory(data_dir+'/借书.txt')
    lhist = loadLibraryHistory(data_dir+'/图书馆门禁.txt')
    chist = loadConsumeHistory(data_dir+'/消费.txt')
    grade = loadGrade(data_dir+'/成绩.txt')

    print len(bhist),len(lhist),len(chist),len(grade)

    students = set({}).union(bhist,lhist,chist,grade)
    urecords = {}
    def _getitem_func(key):
        def _func(dic):
            if dic.has_key(key):
                return dic[key]
            else:
                return None
        return _func
    for uid in students:
        urecords[uid] = map(_getitem_func(uid),[bhist,lhist,chist,grade])
    return urecords
    

def reduceTestingData(data):
    rdata = []
    def _len(d):
        if d is None:
            return 0
        return len(d)
        
    for u,[bhist,lhist,chist,grade] in data.items():
        rrecord = [_len(bhist),_len(lhist),_len(chist),grade[1],grade[2]]
        rdata.append((rrecord,u))
    
    _max = map(float,map(max, [[x[i] for x,u in rdata] for i in range(5)]))
    rdata = [[divide(x,_max).tolist(),u] for x,u in rdata]
    return rdata

data = loadTrainingData('../data/成绩排名预测/训练/')
rdata = reduceData(data)
net,trainer = annFitting(rdata)
trainer.trainEpochs(200)

tdata = loadTestingData('../data/成绩排名预测/测试/')
trdata = reduceTestingData(tdata)
test = []
for x,u in trdata:
    test.append([net.activate(x),u])
test = sorted(test)
















# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 00:21:56 2014

@author: fuz
"""

import csv

def loadfile(fi):
	reader = csv.reader(open(fi,'r'))
	fd = file("output.csv",'w+')
	fd.write("id,rank\n")
	rank_list = {}
	for uid,rank in reader:
		try:
			rank_list[int(uid)] = int(rank)
		except ValueError as e:
			print e.message
	t = sorted(rank_list.items())
	print t
	for uid,rank in t:
		fd.write(str(uid)+","+str(rank)+"\n")
	fd.close()

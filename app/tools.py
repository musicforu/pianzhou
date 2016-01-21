#!/usr/bin/env python
#﻿-*- coding: utf-8 -*-

import os

#获取目录中所有图片名称的列表形式
def photos_list(dir):
	photos2tuple_list=[]	
	photos2list=os.listdir(dir)
	for i in photos2list:
		i=i.decode('utf-8')
		photos2tuple_list.append((i[:-4],i[:-4]))
	return photos2tuple_list
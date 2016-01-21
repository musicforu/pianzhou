#!/usr/bin/env python
#﻿-*- coding: utf-8 -*-

import os

#获取目录中所有图片名称的列表形式
def photos_list(dir):
	photos2list=os.listdir(dir)
	photos2tuple_list=[(i[:-4],i[:-4]) for i in photos2list]
	return photos2tuple_list
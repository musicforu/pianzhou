#!/usr/bin/env python
#﻿-*- coding: utf-8 -*-

from flask import request
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,SelectField
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import Required,Length,Email,Regexp
from ..tools import photos_list

photos_dir='app/static/photos'

class NameForm(Form):
	name=StringField('您的用户名是?',validators=[Required()])
	submit=SubmitField('提交')

class EditProfileForm(Form):
	name=StringField('真实姓名',validators=[Length(0,64)])
	location=StringField('居住地',validators=[Length(0,64)])
	about_me=TextAreaField('个人介绍')
	photos=photos_list(photos_dir)
	photo=SelectField('选择您的头像',choices=photos)
	submit=SubmitField('提交')

class EditProfileAdminForm(Form):
	email=StringField('邮箱地址',validators=[Required(),Length(0,64),Email()])
	username=StringField('用户名',validators=[
		Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名必须只包含字母，数字，点或下划线')])
	confirmed=BooleanField('确认')
	role=SelectField('角色',coerce=int)
	name=StringField('真实名字',validators=[Length(0,64)])
	location=StringField('居住地',validators=[Length(0,64)])
	about_me=TextAreaField('个人介绍')
	submit=SubmitField('提交')

	def __init__(self,user,*args,**kwargs):
		super(EditProfileAdminForm,self).__init__(*args,**kwargs)
		self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
		self.user=user

	def validate_email(self,field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已经被注册.')

	def validate_username(self,field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已经被使用.')

class PostForm(Form):
	body=PageDownField("您现在想说些什么吗？",validators=[Required()])
	submit=SubmitField("发表")


class CommentForm(Form):
	body=StringField('',validators=[Required()])
	submit=SubmitField('发表')


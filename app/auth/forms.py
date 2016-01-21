#!/usr/bin/env python
#﻿-*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User
from ..tools import photos_list

photos_dir='app/static/photos'

class LoginForm(Form):
	email=StringField(u'邮箱地址',validators=[Required(),Length(1,64),Email()])
	password=PasswordField(u'密码',validators=[Required()])
	remember_me=BooleanField(u'保持登陆')
	submit=SubmitField(u'登陆')

class RegistrationForm(Form):
	email=StringField(u'邮箱地址',validators=[Required(),Length(1,64),Email()])
	username=StringField(u'用户名',validators=[
		Required(),Length(1,64),Regexp('^[a-zA-Z][a-zA-Z0-9_.]*$',0,u'用户名必须只包含字母，数字，点或下划线')])
	password=PasswordField(u'密码',validators=[Required(),EqualTo('password2',message=u'两次密码必须一致.')])
	password2=PasswordField(u'确认密码',validators=[Required()])
	photos=photos_list(photos_dir)
	photo=SelectField(u'选择您的头像',choices=photos)	
	submit=SubmitField(u'注册')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'邮箱地址已被注册.')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'用户名已存在.')

class ChangePasswordForm(Form):
	old_password=PasswordField(u'旧密码',validators=[Required()])
	password=PasswordField(u'新密码',validators=[
		Required(),EqualTo('password2',message=u'两个密码必须一致')])
	password2=PasswordField(u'确认新密码',validators=[Required()])
	submit=SubmitField(u'更新密码')

class PasswordResetRequestForm(Form):
	email=StringField(u'邮箱地址',validators=[Required(),Length(1,64),Email()])
	submit=SubmitField(u'重置密码')

class PasswordResetForm(Form):
	email=StringField(u'邮箱地址',validators=[Required(),Length(1,64),Email()])
	password=PasswordField(u'新密码',validators=[Required(),EqualTo('password2',message=u'两个密码必须一致.')])
	password2=PasswordField(u'确认新密码',validators=[Required()])
	submit=SubmitField(u'重置密码')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError(u'未知的邮箱地址.')





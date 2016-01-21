#!/usr/bin/env python
#﻿-*- coding: utf-8 -*-

from flask import render_template,redirect,request,url_for,flash
from flask.ext.login import login_user,login_required,logout_user,current_user
from . import auth
from ..models import User,Role,Post
from .forms import LoginForm,RegistrationForm,ChangePasswordForm,PasswordResetRequestForm,PasswordResetForm
from ..send_email import send_email
from .. import db
from threading import Thread
from werkzeug.utils import secure_filename
import os

upload_path='app/static/photos'
@auth.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash(u'用户名或密码错误.')
	return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash(u'您已经登出.')
	return redirect(url_for('main.index'))

@auth.route('/register',methods=['POST','GET'])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		avatar_name=form.photo.data+'.jpg'
		avatar_path='photos/'+avatar_name	
		user=User(email=form.email.data,
				username=form.username.data,
				password=form.password.data,
				avatar=avatar_path)
		db.session.add(user)
		db.session.commit()				
		token=user.generate_confirmation_token()
		send_email([user.email],u'验证您的账户',
			'confirm',user=user,token=token)		
		flash(u'一封确认邮件已经发到您的邮箱.')
		return redirect(url_for('main.index'))
	photos=os.listdir('app/static/photos')
	return render_template('auth/register.html',form=form,photos=photos)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash(u'您已经确认过账户, 谢谢!')
	else:
		flash(u'验证链接是错误的或者已经过期.')
	return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed and request.endpoint[:5]!='auth.' and request.endpoint!='static':
			return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/email/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token=current_user.generate_confirmation_token()
	send_email([current_user.email],'boat',
			'confirm',user=current_user,token=token)
	flash(u'一封确认邮件已经发到您的邮箱.')
	return redirect(url_for('main.index'))

@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
	form=ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password=form.password.data
			db.session.add(current_user)
			db.session.commit()
			flash(u'您的密码已经更新!')
			return redirect(url_for('main.index'))
		else:
			flash(u'密码错误.')
	return render_template('auth/change_password.html',form=form)

@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form =PasswordResetRequestForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user:
			token=user.generate_reset_token()
			send_email([user.email],u'重置您的密码',
				'reset_password',user=user,token=token,
				next=request.args.get('next'))
		flash(u'一封指引您重置密码的邮件已经发到您的邮箱.')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def password_reset(token):
	#if not current_user.is_anonymous:
		#return redirect(url_for('main.index'))
	form=PasswordResetForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user is None:
			return redirect(url_for('main.index'))
		if user.reset_password(token,form.password.data):
			flash(u'您的密码已经更新.')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html',form=form)








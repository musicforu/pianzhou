#!/usr/bin/env python
#﻿-*- coding: utf-8 -*-

import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY='hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN=True
	FLASKY_ADMIN='Superman'
	DEBUG=True
	FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'
	FLASKY_MAIL_SENDER='Flasky Admin <flasky@666.com>'
	FLASKY_ADMIN='[Flasky]'
	FLASKY_POSTS_PER_PAGE=20
	FLASKY_FOLLOWERS_PER_PAGE = 50
	FLASKY_COMMENTS_PER_PAGE =50
	SQLALCHEMY_RECORD_QUERIES = True
	FLASKY_SLOW_DB_QUERY_TIME=0.5
	MAIL_SERVER='smtp.qq.com'
	MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
	MAIL_PORT=25
	SQLALCHEMY_DATABASE_URI='postgres://ehvfwslnxkxmxh:3s_8uTwvXaBdug-yinVFlDdRkl@ec2-54-83-52-144.compute-1.amazonaws.com:5432/dbvamn4raq0k91'

	@staticmethod
	def init_app(app):
		pass

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'postgres://ehvfwslnxkxmxh:3s_8uTwvXaBdug-yinVFlDdRkl@ec2-54-83-52-144.compute-1.amazonaws.com:5432/dbvamn4raq0k91'
	@classmethod
	def init_app(cls, app):
		Config.init_app(app)

class HerokuConfig(ProductionConfig):	
	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)
		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.WARNING)
		app.logger.addHandler(file_handler)

config={
	'production':Config,
	'default':Config,
	'development':Config,
	'heroku':HerokuConfig
}
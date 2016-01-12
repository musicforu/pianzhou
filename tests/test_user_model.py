#!/usr/bin/env python
#﻿-*- coding: utf-8 -*-

import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission, Follow

class UserModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		Role.insert_roles()
		
	def test_password_setter(self):
		u=User(password='cat')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u=User(password='cat')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):
		u=User(password='cat')
		self.assertTrue(u.verify_password('cat'))
		self.assertFalse(u.verify_password('dog'))

	def test_password_salts_are_random(self):
		u=User(password='cat')
		u2=User(password='cat')
		self.assertTrue(u.password_hash!=u2.password_hash)

	def test_valid_reset_token(self):
		u=User(password='cat')
		db.session.add(u)
		db.session.commit()
		token=u.generate_reset_token()
		self.assertTrue(u.reset_password(token,'dog'))
		self.assertTrue(u.verify_password('dog'))

	def test_invalid_reset_token(self):
		u1=User(password='cat')
		u2=User(password='dog')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		token=u1.generate_reset_token()
		self.assertFalse(u2.reset_password(token,'horse'))
		self.assertTrue(u2.verify_password('dog'))
		
	def test_roles_and_permissions(self):
		Role.insert_roles()
		u=User(email='john@example.com',password='cat')
		self.assertTrue(u.can(Permission.WRITE_ARTICLES))
		self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

	def test_anonymous_user(self):
		u=AnonymousUser()
		self.assertFalse(u.can(Permission.FOLLOW))

	




#! python
# -*- coding: utf-8 -*-

from flask import g
from models import User
from wtforms import fields, validators
from flask.ext.wtf import Form

MIN_PASSWORD_LENGTH = 4
MIN_USERNMAE_LENGTH = 4


class LoginForm(Form):
    mail = fields.TextField('Email', validators=[validators.required(message='Email is required'), validators.Email(message='Email ist not valid')])
    password = fields.PasswordField(validators=[validators.required(message='Password is required')])
    remember_me = fields.BooleanField('remember_me', default=False)
    def validate_mail(self, field):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Email not found in database')
        if not user.check_password(self.password.data):
            raise validators.ValidationError('Password is invalid')
    def get_user(self):
        return User.query.filter_by(mail=self.mail.data).one()


class SettingsForm(Form):
    name = fields.TextField('Nickname')
    def validate_name(self, field):
        if not len(self.name.data) >= MIN_USERNMAE_LENGTH:
            raise validators.ValidationError('new name must be at least {0} characters long'.format(MIN_USERNMAE_LENGTH))


class RegisterForm(Form):
    name = fields.TextField('Nickname', [validators.required()])
    mail = fields.TextField('Email', [validators.required(), validators.Email()])
    password = fields.PasswordField('Password', [validators.required()])
    confirm = fields.PasswordField('Repeat Password', [
        validators.required(),
        validators.EqualTo('password', message='Passwords must match')
        ])
    def validate_mail(self, field):
        user = User.query.filter_by(mail=self.mail.data).first()
        if user is not None:
            raise validators.ValidationError('Email already in use')


class PasswordResetForm(Form):
    mail = fields.TextField('Email', [validators.required(), validators.Email()])
    
    def get_user(self):
        return User.query.filter_by(mail=self.mail.data).first()


class PasswordChangeForm(Form):
    current_password = fields.PasswordField('Current Password', [validators.required()])
    new_password = fields.PasswordField('New Password', [validators.required()])
    confirm_password = fields.PasswordField('Repeat New Password', [
        validators.required(),
        validators.EqualTo('new_password', message='Passwords must match')
        ])

    def validate_new_password(self, field):
        if not len(self.new_password.data) >= MIN_PASSWORD_LENGTH:
            raise validators.ValidationError('new password must be at least {0} characters long'.format(MIN_PASSWORD_LENGTH))

    def validate_current_password(self, field):
        if not g.user.check_password(self.current_password.data):
            raise validators.ValidationError('Current Password is invalid')

class DeleteUserForm(Form):
    password = fields.PasswordField('Password', [validators.required()])
    delete_check = fields.BooleanField('delete_check', default=False)

    def validate_password(self, field):
        if not g.user.check_password(self.password.data):
            raise validators.ValidationError('Password is invalid')
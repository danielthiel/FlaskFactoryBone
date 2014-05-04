#! python
# -*- coding: utf-8 -*-


from flask import Blueprint, flash, g
from flask import session, jsonify
from flask import render_template, redirect, url_for, request, make_response
from flask.ext.login import login_user, logout_user, login_required, current_user


usermgmt = Blueprint('usermgmt', __name__)

from server import db, lm
from models import User
from forms import LoginForm, RegisterForm, SettingsForm
from forms import PasswordResetForm, PasswordChangeForm, DeleteUserForm
from utils import create_json_response



# Main Views:
@usermgmt.route('/')
def index():
    return render_template('user/index.html')


# Registration View:
@usermgmt.route('/register', methods = ['GET', 'POST'])
def register():
    # import worker
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            newuser = User(form.name.data, form.mail.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            login_user(newuser)
            # worker.create_ipblock_for_login(request, is_registration=True)
            return redirect(request.args.get('next') or url_for('index'))
        except:
            flash('Registierung fehlgeschlagen.')
    return render_template('user/register.html', form=form)



@usermgmt.route('/passwordreset', methods=['GET', 'POST'])
def password_reset():
    # import worker
    if g.user is not None and g.user.is_authenticated():
        return redirect(request.args.get('next') or url_for('index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = form.get_user()
        if user:
            flash(u'Aktuell kann kein Passwort zuruckgesetzt werden.')
            # worker.reset_password_for_user(user)
        else:
            flash(u'Diese Email konnte im System nicht gefunden werden.')
    return render_template('user/pwreset.html', form=form)


# SETTINGS / EINSTELLUNGEN:
@usermgmt.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    pw_form = PasswordChangeForm()
    set_form = SettingsForm()
    if 'pw_change' in request.form and pw_form.validate_on_submit():
        try:
            g.user.set_password(pw_form.new_password.data)
            db.session.commit()
            flash(u'Passwort wurde geändert.')
        except:
            flash(u'Passwort konnte nicht geändert werden.')
    if 'settings_change' in request.form and set_form.validate_on_submit():
        g.user.name = set_form.name.data
        db.session.commit()
        flash(u'Einstellungen wurde geändert.')
    return render_template('user/settings.html', pw_form=pw_form, set_form=set_form)


# Login Views:
@usermgmt.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user and g.user.is_authenticated():
        return redirect(request.args.get('next') or url_for('index'))
    loginform = LoginForm()
    if 'login' in request.form and loginform.validate_on_submit():
        session['remember_me'] = loginform.remember_me.data
        user = loginform.get_user()
        login_user(user)
        return redirect(request.args.get('next') or url_for('index'))
    elif request.method == 'POST':
        try:
            data = request.json
            user = User.query.filter(User.mail==data['mail']).one()
            print user
            if user and user.check_password(data['password']):
                login_user(user)
                return create_json_response({'login': True}, 200)
        except Exception, e:
            return create_json_response({'login': False}, 300)
        return create_json_response({'login': False}, 300)

    return render_template('user/login.html', form=loginform)


@usermgmt.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@usermgmt.route('/deleteuser', methods=['GET', 'POST'])
@login_required
def delete_user():
    form = DeleteUserForm()
    if form.validate_on_submit():
        if form.delete_check.data is True:
            g.user.account_activated = False
            db.session.commit()
            logout_user()
            flash(u'Benutzeraccount wurde gelöscht.')
            return redirect(url_for('index'))
        else:
            flash(u'Keine Änderungen durchgeführt.')
    return render_template('user/delete.html', form=form)
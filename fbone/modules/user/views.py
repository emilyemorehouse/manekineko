# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, send_from_directory, abort, redirect, url_for, request, flash
from flask import current_app as APP
from flask.ext.login import login_required, current_user
from fbone.extensions import login_manager
from fbone.core.oauth import OAuthSignIn
from .models import User


user = Blueprint('user', __name__, url_prefix='/user')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@user.route('/')
@login_required
def index(offset = 0):
    if not current_user.is_authenticated():
        abort(403)
    return render_template('user/index.html', user=current_user)


@user.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('user.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@user.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('frontend.index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('user.index'))


@user.route('/<int:user_id>/profile')
@login_required
def profile(user_id):
    user = User.get_by_id(user_id)
    return render_template('user/profile.html', user=user, current_user=current_user, followed=current_user.is_following(user))


@user.route('/<int:user_id>/avatar/<path:filename>')
@login_required
def avatar(user_id, filename):
    dir_path = os.path.join(APP.config['UPLOAD_FOLDER'], 'user_%s' % user_id)
    return send_from_directory(dir_path, filename, as_attachment=True)


@user.route('/follow_user/<int:user_id>')
@login_required
def follow_user(user_id):
    user = User.get_by_id(user_id)
    current_user.follow(user)
    flash(_("You are now following") +" %s"%user.name,'success')
    return render_template('user/profile.html', user=user, current_user=current_user, followed=current_user.is_following(user))

@user.route('/unfollow_user/<int:user_id>')
@login_required
def unfollow_user(user_id):
    user = User.get_by_id(user_id)
    current_user.unfollow(user)
    flash(_("You are now not following")+" %s"%user.name,'success')
    return render_template('user/profile.html', user=user, current_user=current_user, followed=current_user.is_following(user))




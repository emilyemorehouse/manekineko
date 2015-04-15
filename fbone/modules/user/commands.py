# -*- coding: utf-8 -*-
"""
    fbone.modules.user
    ~~~~~~~~~~~~~~~~~~~~~~~~

    user management commands
"""

from flask.ext.script import Command, prompt, prompt_pass
from werkzeug.datastructures import MultiDict

from .models import User


class CreateUserCommand(Command):
    """Create a user"""
    """!!!broken!!!"""

    def run(self):
        email = prompt('Email')
        password = prompt_pass('Password')
        password_confirm = prompt_pass('Confirm Password')
        data = MultiDict(dict(email=email, password=password, password_confirm=password_confirm))
        form = RegisterForm(data, csrf_enabled=False)
        if form.validate():
            user = register_user(email=email, password=password)
            print '\nUser created successfully'
            print 'User(id=%s email=%s)' % (user.id, user.email)
            return
        print '\nError creating user:'
        for errors in form.errors.values():
            print '\n'.join(errors)


class DeleteUserCommand(Command):
    """Delete a user"""

    def run(self):
        email = prompt('Email')
        user = User.first(email=email)
        if not user:
            print 'Invalid user'
            return
        User.delete(user)
        print 'User deleted successfully'


class ListUsersCommand(Command):
    """List all users"""

    def run(self):
        for u in User.all():
            print 'User(id=%s email=%s)' % (u.id, u.email)

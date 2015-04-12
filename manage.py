# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Manager module
"""

from flask.ext.script import Manager

from fbone import create_app
from fbone.extensions import db
from fbone.utils import MALE
from fbone.modules.user import User, UserDetail, ADMIN, ACTIVE

# from fbone.modules.admin.commands import ...
# from fbone.modules.api.commands import ...
# from fbone.modules.frontend.commands import ...
# from fbone.modules.settings.commands import ...
from fbone.modules.user.commands import CreateUserCommand, DeleteUserCommand, ListUsersCommand


app = create_app()
manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command('create_user', CreateUserCommand())
manager.add_command('delete_user', DeleteUserCommand())
manager.add_command('list_users', ListUsersCommand())


@manager.command
def run():
    """Run in local machine."""
    app.run(host='0.0.0.0')


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
        name=u'admin',
        nickname=u'agadorspartacus',
        email=u'admin@example.com',
        password=u'123456',
        role_code=ADMIN,
        status_code=ACTIVE,
        user_detail=UserDetail(
            gender_code=MALE,
            age=32,
            url=u'http://seminoles.com',
            location=u'Tallahassee, FL',
            bio=u'FSU Grad. Go Noles!'))
    db.session.add(admin)
    db.session.commit()


if __name__ == "__main__":
    manager.run()

# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Flask-Script Manager
"""

from flask.ext.script import Manager

from fbone import create_app
from fbone.extensions import db
from fbone.utils import MALE
from fbone.modules.user import User, ADMIN, ACTIVE

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
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
        name=u'admin',
        fullname=u'Agador Spartacus',
        email=u'admin@example.com',
        password=u'123456',
        role_code=ADMIN,
        status_code=ACTIVE,
        gender_code=MALE,
        bio=u'FSU Grad. Go Noles!')
    db.session.add(admin)
    db.session.commit()


if __name__ == "__main__":
    manager.run()

# -*- coding: utf-8 -*-
"""
    fbone.modules.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    fbone base db Model
    Convenience functions which interact with SQLAlchemy models.
"""

from sqlalchemy import Column, func, Integer
from sqlalchemy.ext.declarative import declared_attr

from fbone.extensions import db


class Base(db.Model):
    """Convenience base DB model class. Makes sure tables in MySQL are created as InnoDB.
    This is to enforce foreign key constraints (MyISAM doesn't support constraints) outside of production. Tables are
    also named to avoid collisions.
    """

    @declared_attr
    def __tablename__(self):
        return '{}'.format(self.__name__.lower())

    __abstract__ = True
    __table_args__ = dict(mysql_charset='utf8', mysql_engine='InnoDB')
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the sebase's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.
        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        rv = isinstance(model, self.__class__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__class__))
        return rv

    def _preprocess_params(self, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.
        :param kwargs: a dictionary of parameters
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, model):
        """Commits the model to the database and returns the model
        :param model: the model to save
        """
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def all(self):
        """Returns a generator containing all instances of the base model.
        """
        return self.__class__.query.all()

    def get_by_id(self, id):
        """Returns an instance of the base model with the specified id.
        Returns `None` if an instance with the specified id does not exist.
        :param id: the instance id
        """
        return self.__class__.query.get(id)

    def get_all(self, *ids):
        """Returns a list of instances of the base model with the specified
        ids.
        :param *ids: instance ids
        """
        return self.__class__.query.filter(self.__class__.id.in_(ids)).all()

    def find(self, **kwargs):
        """Returns a list of instances of the base model filtered by the
        specified key word arguments.
        :param **kwargs: filter parameters
        """
        return self.__class__.query.filter_by(**kwargs)

    def first(self, **kwargs):
        """Returns the first instance found of the base model filtered by
        the specified key word arguments.
        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        """Returns an instance of the base model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.
        :param id: the instance id
        """
        return self.__class__.query.get_or_404(id)

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the base model class.
        :param **kwargs: instance parameters
        """
        return self.__class__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        """Returns a new, saved instance of the base model class.
        :param **kwargs: instance parameters
        """
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        """Returns an updated instance of the base model class.
        :param model: the model to update
        :param **kwargs: update parameters
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        """Immediately deletes the specified model instance.
        :param model: the model instance to delete
        """
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()
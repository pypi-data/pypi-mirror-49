from .base import *

class Log(Base):
    __tablename__ = 'log'

    id = sa.Column(sa.Integer, primary_key=True)
    step = sa.Column(sa.Integer, ForeignKey('step.id'))
    message = sa.Column(sa.String)
    time = sa.Column(sa.DateTime)
    level = sa.Column(sa.Integer)
    component = sa.Column(sa.Integer)
    module = sa.Column(sa.String)
    line = sa.Column(sa.Integer)
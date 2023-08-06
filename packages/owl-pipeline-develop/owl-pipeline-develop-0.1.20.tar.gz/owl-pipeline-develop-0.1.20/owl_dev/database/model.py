from sqlalchemy import Column, DateTime, Integer, Sequence, Unicode

from owl_dev.database import DeclarativeBase


class Status(DeclarativeBase):
    __tablename__ = "status"
    id = Column(Integer, Sequence("status_id_seq"), primary_key=True)
    flow = Column(Unicode(25), nullable=False)
    task = Column(Unicode(25), nullable=False)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    last = Column(DateTime, nullable=True)
    status = Column(Unicode(25), nullable=False)

    def __repr__(self):
        return "<Status(flow='%s', task='%s', status='%s')>" % (
            self.flow,
            self.task,
            self.status,
        )


class Info(DeclarativeBase):
    __tablename__ = "info"
    id = Column(Integer, Sequence("info_id_seq"), primary_key=True)
    config = Column(Unicode, nullable=False)
    env = Column(Unicode, nullable=False)
    python = Column(Unicode, nullable=False)

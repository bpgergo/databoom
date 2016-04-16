from lxml.html.builder import COL
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, ForeignKey, \
    Integer, String, Float, SmallInteger, DateTime, Boolean, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
import logging


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        elif hasattr(o, 'isoformat'):
            return o.isoformat()
        return super(DecimalEncoder, self)._iterencode(o, markers)


class Econ(Base):
    __tablename__ = 'econ'
    id = Column(String, primary_key=True)
    parent_id = Column(String, ForeignKey('econ.id'))
    value = Column(String, nullable=False)
    def __repr__(self):
        return "id:%s, parent:%s, value:%s" % (self.id, self.parent_id, self.value)

    @property
    def json(self):
        return {"id": self.id, "parent_id": self.parent_id, "value": self.value}

class Func(Base):
    __tablename__ = 'func'
    id = Column(String, primary_key=True)
    parent_id = Column(String, ForeignKey('func.id'))
    value = Column(String, nullable=False)
    tags = Column(String)

    def __repr__(self):
        tags = None
        if self.tags:
            [tag.strip() for tag in self.tags.split(",")]
        return {"id": self.id, "parent_id": self.parent_id, "value": self.value, "tags": tags}


def json_func(self):
        result = {"id": self.id, "parent_id": self.parent_id, "value": self.value}
        if hasattr(self, "tags"):
            tags = None
            if self.tags:
                [tag.strip() for tag in self.tags.split(",")]
            result["tags"] = tags

        return result


class Org(Base):
    __tablename__ = 'org'
    id = Column(String, primary_key=True)
    parent_id = Column(String, ForeignKey('org.id'))
    value = Column(String, nullable=False)
    def __repr__(self):
        return "id:%s, parent:%s, value:%s" % (self.id, self.parent_id, self.value)


class Budget(Base):
    __tablename__ = 'budget'
    id = Column(String, primary_key=True)
    func_id = Column(String, ForeignKey('func.id'), nullable=False)
    econ_id = Column(String, ForeignKey('econ.id'), nullable=False)
    amount = Column(Numeric, nullable=False)
    org_id = Column(String, ForeignKey('org.id'), nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime)
    comm = Column(String)
    tags = Column(String)
    def __repr__(self):
        return str(json_budget(self))


def json_budget(self):
    start = None
    if self.date_start:
        start = self.date_start.isoformat()
    end = None
    if self.date_end:
        end = self.date_end.isoformat()
    tags = None
    if self.tags:
        [tag.strip() for tag in self.tags.split(",")]
    return {"id": self.id,
            "func_id": self.func_id,
            "econ_id": self.econ_id,
            "org_id": self.org_id,
            "value": str(self.amount), # '{0:.3g}'.format(self.amount),
            "date_start": start,
            "date_end": end,
            "comments": self.comm,
            "tags": tags
            }

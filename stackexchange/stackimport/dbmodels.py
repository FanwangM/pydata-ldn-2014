# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

from sqlalchemy import (
    Column, Integer, DateTime, UnicodeText, Table, ForeignKey,
    ForeignKeyConstraint)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


post_tags = Table(
    'post_tags', Base.metadata,
    Column('post_id', Integer),
    Column('forum_id', Integer),
    Column('tag_id', Integer, ForeignKey('tags.id')),
    ForeignKeyConstraint(
        ('post_id', 'forum_id'),
        ('posts.id', 'posts.forum_id'),
    ),
)


class Forum(Base):
    __tablename__ = 'forums'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(UnicodeText, index=True, unique=True)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    text = Column(UnicodeText, index=True, unique=True)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    forum_id = Column(Integer, ForeignKey('forums.id'), primary_key=True)
    post_type_id = Column(Integer, nullable=False)
    accepted_answer_id = Column(Integer)
    creation_date = Column(DateTime, nullable=False)
    score = Column(Integer, nullable=False)
    view_count = Column(Integer)
    body = Column(UnicodeText, nullable=False)
    owner_user_id = Column(Integer)
    last_editor_user_id = Column(Integer)
    last_edit_date = Column(DateTime)
    last_activity_date = Column(DateTime, nullable=False)
    title = Column(UnicodeText)
    # tags
    answer_count = Column(Integer)
    favorite_count = Column(Integer)

    forum = relationship('Forum', backref=backref('posts', order_by=id))

    tags = relationship('Tag', secondary=post_tags, backref='posts')

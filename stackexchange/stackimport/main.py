import argparse
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .dbmodels import Base
from .importer import import_forum


def connect(db_name):
    engine = create_engine('postgresql+psycopg2://simon@/{}'.format(db_name))
    Session = sessionmaker(bind=engine)
    return engine, Session()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('db_name')
    parser.add_argument('forum_name')
    parser.add_argument('file')
    parser.add_argument('--create', action='store_true', default=False)
    return parser.parse_args(sys.argv[1:])


def main():
    args = parse_args()
    engine, session = connect(args.db_name)
    if args.create:
        Base.metadata.create_all(engine)

    import_forum(session, args.forum_name, args.file)

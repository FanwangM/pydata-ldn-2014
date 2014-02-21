import argparse
import sys


def connect(db_name):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('postgresql+psycopg2://simon@/{}'.format(db_name))
    Session = sessionmaker(bind=engine)
    return engine, Session()


def parse_args():
    parser = argparse.ArgumentParser(prog='stackimport')
    parser.add_argument('db_name')
    parser.add_argument('--create', action='store_true', default=False)

    subparsers = parser.add_subparsers()
    import_group = subparsers.add_parser('import')
    import_group.add_argument('forum_name')
    import_group.add_argument('file')
    import_group.set_defaults(func=import_action)

    console_group = subparsers.add_parser('console')
    console_group.set_defaults(func=console_action)
    return parser.parse_args(sys.argv[1:])


def import_action(session, args):
    from .importer import import_forum
    import_forum(session, args.forum_name, args.file)


def console_action(session, args):
    from . import dbmodels  # noqa
    import IPython
    IPython.embed()


def main():
    args = parse_args()
    engine, session = connect(args.db_name)
    if args.create:
        from .dbmodels import Base
        Base.metadata.create_all(engine)

    args.func(session, args)

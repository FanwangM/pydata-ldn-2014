import glob
import mailbox

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Sequence, MetaData
from sqlalchemy import Integer
from sqlalchemy.exc import DataError
from sqlalchemy.dialects.postgresql import HSTORE

engine = create_engine("postgresql+psycopg2://simon@/emails")
meta_data = MetaData(bind=engine)

pydev = Table("pydev",
              meta_data,
              Column("id", Integer, Sequence("pydev_id_seq"), primary_key=True),
              Column("data", HSTORE, default={}),
             )
pylist = Table("pylist",
              meta_data,
              Column("id", Integer, Sequence("pylist_id_seq"), primary_key=True),
              Column("data", HSTORE, default={}),
             )

RESET_TABLE = True
if RESET_TABLE:
    meta_data.drop_all()
    meta_data.create_all()


def igroup(it, block_size):
    buf = []
    for i, value in enumerate(it):
        if len(buf) == block_size:
            yield buf
            buf = []
        buf.append(value)
    yield buf

def mbox_to_doc(m):
    return {k: m.get(k) for k in m.keys()}

with engine.connect() as conn:
    for filename in glob.glob("data/emails/pylist/*txt"):
        print filename
        mbox = mailbox.mbox(filename)
        ins = pylist.insert()
        for m in mbox:
            try:
                conn.execute(ins, data=mbox_to_doc(m))
            except DataError:
                print "Ignoring doc {}".format(mbox_to_doc(m))

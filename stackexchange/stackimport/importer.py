import datetime
import re
from xml.sax.saxutils import unescape

from lxml import etree

from .dbmodels import Forum, Post, Tag


DATE_ISOFORMAT = '%Y-%m-%dT%H:%M:%S.%f'
TAGS_RE = re.compile('<(.*?)>')


strptime = lambda s: datetime.datetime.strptime(
    s + '000', DATE_ISOFORMAT)
unicode_decode = lambda s: s  # .decode('utf-8')


def add_tags(session, tags_string):
    tags = []
    tags_string = unicode_decode(unescape(tags_string))
    for tag_text in TAGS_RE.findall(tags_string):
        if session.query(Tag).filter(Tag.text == tag_text).count() == 0:
            tag = Tag(text=tag_text)
            session.add(tag)
            tags.append(tag)
        else:
            tag = session.query(Tag).filter(Tag.text == tag_text).one()
            tags.append(tag)
    return tags


attr_to_column_map = {
    'Id': 'id',
    'PostTypeId': 'post_type_id',
    'AcceptedAnswerId': 'accepted_answer_id',
    'CreationDate': 'creation_date',
    'Score': 'score',
    'ViewCount': 'view_count',
    'Body': 'body',
    'OwnerUserId': 'owner_user_id',
    'LastEditorUserId': 'last_editor_user_id',
    'LastEditDate': 'last_edit_date',
    'LastActivityDate': 'last_activity_date',
    'Title': 'title',
    'Tags': 'tags',
    'AnswerCount': 'answer_count',
    'FavoriteCount': 'favorite_count',
}


def import_forum_posts(session, xml, forum):
    attr_to_type_map = {
        'Id': int,
        'PostTypeId': int,
        'AcceptedAnswerId': int,
        'CreationDate': strptime,
        'Score': int,
        'ViewCount': int,
        'Body': unicode_decode,
        'OwnerUserId': int,
        'LastEditorUserId': int,
        'LastEditDate': strptime,
        'LastActivityDate': strptime,
        'Title': unicode_decode,
        'Tags': lambda t: add_tags(session, t),
        'AnswerCount': int,
        'FavoriteCount': int,
    }

    for index, row in enumerate(xml.getroot()):
        try:
            kwargs = {attr_to_column_map[attr]: attr_to_type_map[attr](value)
                      for attr, value in row.attrib.iteritems()
                      if attr in attr_to_column_map}
        except Exception as e:
            print u'Error import row: {!s}'.format(unicode(e))
            continue
        post = Post(forum=forum, **kwargs)
        session.add(post)

        if (index + 1) % 1000 == 0:
            session.commit()

    session.commit()


def import_forum(session, forum_name, filename):
    if session.query(Forum).filter(Forum.name == forum_name).count() == 0:
        forum = Forum(name=forum_name)
        session.add(forum)
    else:
        forum = session.query(Forum).filter(Forum.name == forum_name).one()
    session.commit()

    with open(filename, 'r') as posts_file:
        xml = etree.parse(posts_file)
    import_forum_posts(session, xml, forum)
    session.commit()

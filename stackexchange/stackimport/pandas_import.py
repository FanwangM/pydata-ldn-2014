import datetime
import re

from lxml import etree
import pandas

DATE_ISOFORMAT = '%Y-%m-%dT%H:%M:%S.%f'
TAGS_RE = re.compile('<(.*?)>')


strptime = lambda s: datetime.datetime.strptime(
    s + '000', DATE_ISOFORMAT)


def import_to_pandas(filename):
    post_ids = []
    creation_dates = []
    tags = []
    titles = []
    bodies = []

    with open(filename, 'r') as posts_file:
        xml = etree.iterparse(posts_file, tag='row')

        for index, event in enumerate(xml):
            _, row = event

            if 'Tags' not in row.attrib:
                row_tags = [None]
            else:
                tags_string = row.attrib['Tags']
                row_tags = TAGS_RE.findall(tags_string)

            if 'Title' not in row.attrib:
                title = None
            else:
                title = row.attrib['Title']

            post_id = int(row.attrib['Id'])
            creation_date = strptime(row.attrib['CreationDate'])
            body = row.attrib['Body']

            row.clear()

            for tag_text in row_tags:
                post_ids.append(post_id)
                creation_dates.append(creation_date)
                tags.append(tag_text)
                titles.append(title)
                bodies.append(body)

    post_ids = pandas.Series(post_ids)
    creation_dates = pandas.Series(creation_dates)
    tags = pandas.Series(tags)
    titles = pandas.Series(titles)
    bodies = pandas.Series(bodies)
    return pandas.DataFrame(
        {
            'post_id': post_ids,
            'creation_date': creation_dates,
            'tag': tags,
            'title': titles,
            'body': bodies,
        },
    )

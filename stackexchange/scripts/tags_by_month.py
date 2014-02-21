import matplotlib.pyplot as plt
import pandas


# frame = pandas.io.sql.read_sql('''-- Popular tags by month
#    SELECT extract(YEAR FROM posts.creation_date) as post_year,
#           extract(MONTH FROM posts.creation_date) as post_month,
#           tags.text as tag,
#           count(posts.id)
#      FROM posts, tags, post_tags
#     WHERE post_tags.post_id = posts.id
#       AND post_tags.forum_id = posts.forum_id
#       AND post_tags.tag_id = tags.id
#  GROUP BY post_year,
#           post_month,
#           tag
#  ORDER BY count desc;
# ''', connection)


math_by_year_month = pandas.io.sql.read_sql('''\
   SELECT to_char(posts.creation_date, 'YYYY-MM') as creation_date,
          tags.text as tag,
          count(posts.id)
     FROM posts, tags, post_tags
    WHERE post_tags.post_id = posts.id
      AND post_tags.forum_id = posts.forum_id
      AND post_tags.tag_id = tags.id
 GROUP BY creation_date,
          tag;
''', connection)

math_by_year_month = math_by_year_month.set_index('creation_date')
math_by_year_month.index = pandas.to_datetime(math_by_year_month.index)

tags_by_count = math_by_year_month.groupby(['tag'])['count'].sum().order()
homework_by_year_month = math_by_year_month[
    math_by_year_month['tag'] == 'homework']


math_by_date = pandas.io.sql.read_sql('''\
   SELECT to_char(posts.creation_date, 'YYYY-MM-DD') as creation_date,
          tags.text as tag,
          count(posts.id)
     FROM posts, tags, post_tags
    WHERE post_tags.post_id = posts.id
      AND post_tags.forum_id = posts.forum_id
      AND post_tags.tag_id = tags.id
 GROUP BY creation_date,
          tag;
''', connection)

math_by_date = math_by_date.set_index('creation_date')
math_by_date.index = pandas.to_datetime(math_by_date.index)

tags_by_count = math_by_date.groupby(['tag'])['count'].sum().order()
homework_by_date = math_by_date[
    math_by_date['tag'] == 'homework']


shimano = pandas.io.sql.read_sql('''\
   SELECT to_char(posts.creation_date, 'YYYY') as creation_date,
          tags.text as tag,
          count(posts.id)
     FROM posts, tags, post_tags
    WHERE post_tags.post_id = posts.id
      AND post_tags.forum_id = posts.forum_id
      AND post_tags.tag_id = tags.id
      AND tags.text = 'shimano'
 GROUP BY creation_date,
          tag;
''', connection)


sram = pandas.io.sql.read_sql('''\
   SELECT to_char(posts.creation_date, 'YYYY') as creation_date,
          tags.text as tag,
          count(posts.id)
     FROM posts, tags, post_tags
    WHERE post_tags.post_id = posts.id
      AND post_tags.forum_id = posts.forum_id
      AND post_tags.tag_id = tags.id
      AND tags.text = 'sram'
 GROUP BY creation_date,
          tag;
''', connection)


shimano = shimano.set_index('creation_date')
shimano.index = pandas.to_datetime(shimano.index)
sram = sram.set_index('creation_date')
sram.index = pandas.to_datetime(sram.index)


fig1 = plt.figure()
shimano.groupby(shimano.index).size().order().plot()
sram.groupby(sram.index).size().order().plot()

fig2 = plt.figure()
homework_by_year_month.groupby(
    homework_by_year_month.index).size().order().plot()

fig3 = plt.figure()
homework_by_date.groupby(homework_by_date.index).size().order().plot()

class: center, center, inverse

# Why using database at all ?

---
layout:false

.left-column[
  ## Some basic statistics around SO
]

.right-column[
StackOverflow makes its data publicly available:

- popular tags ?
- trends in tags over time ?

Problem:

- ~ 8 millions questions, ~23 Gb xml for posts
- too large to use pandas on laptop
- multiple tables, relationships (e.g. tags)

Suggestion: store in a database, load the data we care about in pandas.
]

---
layout:false

.left-column[
## What will you learn ?
]

.right-column[
playing python, numpy, pandas and postgres to their strenghts:

- importing data from postgres into pandas

- how to use sqlalchemy to deal with Database without too much pain

- using pandasql to make some pandas data manipulation easier

- handling semi-structured data in postgres
]

---
class: left, top, inverse
# We will not talk about 'very large' data handling

---
class: left, top, inverse
# We will not talk about scalability

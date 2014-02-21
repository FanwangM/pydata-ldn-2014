class: center, middle, inverse
# Semi-structured data analysis
## Using postgresql HSTORE to look at python email lists
---
layout: false

.left-column[
 ## Semi structured data
]

.right-column[
Real-world data are often loosely-defined:

- most, but not all entries have a common set of tags/labels
- values are not always the same 'type'

Pydev archive:

- mbox format
- not every email has the same tags

One can still use postgresql:

- ACID properties, transactions
- stability
- we can still use SQLAlchemy and standard tools
]

---
layout: false

.left-column[
## HSTORE
]

.right-column[
Hstore is a postgresql extensions:

```
sudo apt-get install postgresql-9.3-contrib
sudo -u postgres psql $database
> CREATE EXTENSION hstore;
```

Hstore values are akin to python dict, accessed with the '->' operator:

``` sql
select count(data->'From') from pylist
    where data->'From' = 
    'guido at python.org (Guido van Rossum)';
## took ~ 200 ms
```

You can add indices to some keys:

``` sql
create index ix_pylist_from 
    on pylist
    using btree((data->'From'));
```

``` sql
select count(data->'From') from pylist 
    where data->'From' = 
    'guido at python.org (Guido van Rossum)';
## took ~ 2 ms
```
]
---
# HSTORE and SQLA

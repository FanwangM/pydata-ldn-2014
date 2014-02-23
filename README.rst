PyData London 2014 Databases Tutorial
=====================================


Data sources used
=================

Python Mailing Lists
--------------------

* The full ``python-list`` and ``python-dev`` mailing list archives can
  be retrieved in ``mbox`` format with the following ``bash`` snippet,
  replacing ``${LIST}`` with either ``python-list`` or ``python-dev`::

    MAILMAN_URL="http://mail.python.org/pipermail/${LIST}/"
    for FILENAME in $(wget -O - -q $MAILMAN_URL |
                             egrep -o 'href="[^"]+.txt.gz"' |
                             cut -f2 -d\" )
    do
        wget $MAILMAN_URL/$FILENAME
        gunzip $FILENAME
    done


Stack Exchange Data
-------------------

The Stack Exchange data is available as a torrent download.  The
information will be added shortly.

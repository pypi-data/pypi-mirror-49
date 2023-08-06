This is a backport of the zipfile module from Python 3.7, which contains some
improvements. Cloned from the 3.6 backport of Thomas Kluyver (https://gitlab.com/takluyver/zipfile36).

Installation::

    pip install zipfile37

Suggested usage:

.. code:: python

    if sys.version_info >= (3, 7):
        import zipfile
    else:
        import zipfile37 as zipfile

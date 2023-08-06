Description
============

Introduction
------------

Emporium provides an abstraction over file stores. It currently supports storing
files on local disk, in memory, or on S3. Most stores are implemented as a
simple wrapper around the `smart-open <https://pypi.org/project/smart-open/>`_
package.

Example
-------

The following code snippet creates a store, writes some text to a file in the
store, reads the file, and prints its contents. The file ``hello.txt`` will have
been created under folder ``data``, relative to the current working directory.

.. code-block:: python

   from emporium import create_store

   config = {
       "type": "local",
       "base_path": "data"
   }

   store = create_store(config)

   with store.write("hello.txt") as handle:
       handle.write("world!")

   with store.read("hello.txt") as handle:
       print(handle.read())

To write the file to a key in S3, change the config definition to the following:

.. code-block:: python

   config = {
        "type": "s3",
        "bucket": "my-data-bucket",
        "prefix": "data"
   }


# py_dataset   [![DOI](https://data.caltech.edu/badge/175684474.svg)](https://data.caltech.edu/badge/latestdoi/175684474)

py_dataset is a Python wrapper for the [dataset](https://github.com/caltechlibrary/dataset) 
command line tool, Go package, and  C shared library for working with 
[JSON](https://en.wikipedia.org/wiki/JSON) objects as collections. 
Collections can be stored on disc or in 
Cloud Storage.  JSON objects are stored in collections as 
plain UTF-8 text. This means the objects can be accessed with common 
Unix text processing tools as well as most programming languages.

This package wraps all [dataset](docs/dataset.html) operations such 
as initialization of collections, creation, 
reading, updating and deleting JSON objects in the collection. Some of 
its enhanced features include the ability to generate data 
[frames](docs/frame.html) as well as the ability to 
import and export JSON objects to and from CSV files and Google Sheets.

## Install

Available via pip `pip install py_dataset` or by downloading this repo and
typing `python setup.py install`. This repo includes dataset shared C libraries
compiled for Windows, Mac, and Linux and the appripriate library will be used
automatically.

## Features

[dataset](docs/dataset) supports 

- Basic storage actions ([create](docs/create.html), [read](docs/read.html), [update](docs/update.html) and [delete](docs/delete.html))
- listing of collection [keys](docs/keys.html) (including filtering and sorting)
- import/export  of [CSV](how-to/working-with-csv.html) files and [Google Sheets](how-to/working-with-gsheets.html)
- An experimental full text [search](how-to/indexing-and-search.html) interface based on [Blevesearch](https://blevesearch.com)
- The ability to reshape data by performing simple object [joins](docs/join.html)
- The ability to create data [grids](docs/grid.html) and [frames](docs/frame.html) from collections based 
  on keys lists and [dot paths](docs/dotpath.html) into the JSON objects stored

### Limitations of _dataset_

_dataset_ has many limitations, some are listed below

- it is not a multi-process, multi-user data store (it's files on "disc" without locking)
- it is not a replacement for a repository management system
- it is not a general purpose database system
- it does not supply version control on collections or objects

## Tutorial

This module provides the functionality of the _dataset_ command line tool as a Python 3.6 module.
Once installed try out the following commands to see if everything is in order (or to get familier with
_dataset_).

The "#" comments don't have to be typed in, they are there to explain the commands as your type them.
Start the tour by launching Python3 in interactive mode.

```shell
    python3
```

Then run the following Python commands.

```python
    from py_dataset import dataset
    # Almost all the commands require the collection_name as first paramter, we're storing that name in c_name for convience.
    c_name = "a_tour_of_dataset.ds"

    # Let's create our a dataset collection. We use the method called 'init' it returns True or False
    dataset.init(c_name)

    # Let's check our collection to see if it is OK
    dataset.status(c_name)

    # Let's count the records in our collection (should be zero)
    cnt = dataset.count(c_name)
    print(cnt)

    # Let's read all the keys in the collection (should be an empty list)
    keys = dataset.keys(c_name)
    print(keys)

    # Now let's add a record to our collection. To create a record we need to know
    # this collection name (e.g. c_name), the key (most be string) and have a record (i.e. a dict literal or variable)
    key = "one"
    record = {"one": 1}
    ok = dataset.create(c_name, key, record)
    # If ok is False we can check the last error message with the 'error_message' method
    if ok == False:
        print(dataset.error_message())

    # Let's count and list the keys in our collection, we should see a count of '1' and a key of 'one'
    dataset.count(c_name)
    keys = dataset.keys(c_name)
    print(keys)

    # We can read the record we stored using the 'read' method.
    new_record = dataset.read(c_name, key)
    print(new_record)

    # Let's modify new_record and update the record in our collection
    new_record["two"] = 2
    ok = dataset.update(c_name, key, new_record)
    if ok == False:
        print(dataset.error_message())

    # Let's print out the record we stored using read method
    print(dataset.read(c_name, key)

    # Finally we can remove (delete) a record from our collection
    ok = dataset.delete(c_name, key)
    if ok == False:
        print(dataset.error_message())

    # We should not have a count of Zero records
    cnt = dataset.count(c_name)
    print(cnt)
```

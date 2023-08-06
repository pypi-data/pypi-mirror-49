** WARNING : DON'T EXPECT SOMETHING USEFULL FROM THIS TOOL AT THIS STAGE !! **

# xlscrap

xlscrap is a [MIT-licensed](https://opensource.org/licenses/BSD-3-Clause) package to ease Excel files mass data extraction

See the [documentation](docs/index.md).

# Rationale

Have you ever feel the pain of extracting data from a lot of Excel files ?

* When you have hundreds or thousands file that look similar
but differ in slighty annoying details.
* When data cells coordinates can't be used because they change
* When you have to spot dozens or hundreds fields with different strategies.
* When the same field moves in different sheet position or name
* When the same field label changes
* When the data cell is on the right of the label or below the label
* When you need to check that the collected data is correct.

xlscrap helps you to scrap data out of your Excel files.

# Quickstart

```python
>>> import xlscrap
>>> s = xlscrap.Scrapper()
>>> s.field('name')
>>> s.field('age')
>>> s.field('address')
>>> s.table('pets', fields=['name', 'breed', 'age'])
>>> s.scrap('excel-files/*.xls*')
looking for 4 fields in 5 files in excel-files/*.xls*,
file 1/5, found 4/4 fields in diana.xlsx
file 2/5, found 4/4 fields in bob.xls
file 3/5, found 3/4 fields in richard.ods
file 4/5, found 0/4 fields in alien.xls
file 5/5, found 4/4 fields in maria.xlsm
>>> s.result
[
    {'name': 'Diana',
    'age': 47,
    'address': '44 rue du Louvre\n75000 Paris\nFrance'
    'pets': []},
    ...
]
```

# TODO

* set gitlab URL in setup.py
* clone gitlab/github
* complete quickstart in README
  
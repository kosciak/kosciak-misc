# Introduction #

Imports [AdTaily](http://adtaily.com/) catalogue and saves it as CSV file


# Download #

Check the [Downloads](http://code.google.com/p/kosciak-misc/downloads/list) section or checkout the source from Subversion repository using
```
svn checkout http://kosciak-misc.googlecode.com/svn/python/adtaily2csv/trunk/ adtaily2csv
```


# Usage #

Just run the script with catalogue number as an argument. For example if you want to import 'Komputery i Internet' (http://www.adtaily.com/networks/6/websites) catalogue just run
```
./adtaily2csv.py 6
```
Script will generate adtaily\_6.csv that can be imported by MS Excel or OOo Calc. When importing select UTF-8 encoding and Tab as an separator!


# Changelog #

0.2
  * fixed how CPM is calculated

0.1
  * initial release
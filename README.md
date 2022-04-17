# Postgres tests

A simple test for postgres clients performances.

# Requirements

* docker
* make

# Instructions

Run `make launch`, open the browser at the url `http://localhost:8089/`, setup the parameters for your test and launch it.

# Limitations

- the only available clients are in python and go
- only connection pools are being tested currently

# Postgres tests

Quick and dirty test for postgres clients performances.

You can find an example of the test output in the examples folder.

# Requirements

- docker
- make

# Instructions

Run `make launch`, open the browser at the url `http://localhost:8089/`, setup the parameters for your test and launch it.

# Limitations

- the only available clients are in python and go
- only raw ```SELECT *``` queries are being tested right now
- there are probably better tools to execute the tests than locust

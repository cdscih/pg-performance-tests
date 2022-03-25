.PHONY: launch populate_db launch-test

populate_db:
	docker run pg-tests_utils python populate_db.py


launch-test:
	docker run pg-tests_locust locust

launch:
	docker-compose build &&\
	 docker-compose up -d &&\
	 echo "Waiting to load db..." &&\
	 sleep 2 &&\
	 make populate_db &&\
	 make launch-test

re-launch:
	docker-compose down && make launch

.PHONY: launch populate_db launch_test_client quit

populate_db:
	docker run pg-tests_utils python populate_db.py


launch_test_client:
	docker run pg-tests_locust locust

# TODO: use a proper script to wait for db
launch:
	docker-compose build &&\
	 docker-compose up -d &&\
	 echo "Waiting to load db..." &&\
	 sleep 2 &&\
	 make populate_db &&\
	 make launch_test_client

quit:
	docker-compose down

re-launch:
	docker-compose down && make launch

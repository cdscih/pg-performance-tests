.PHONY: launch populate_db launch_test_client clean build

populate_db:
	docker run pg-tests_utils python populate_db.py


launch_test_client:
	docker run pg-tests_locust locust

clean:
	docker-compose down --remove-orp

build:
	docker-compose build

# TODO: use a proper script to wait for db
launch: clean build
	 docker-compose up -d &&\
	 echo "Waiting to load db..." &&\
	 sleep 2 &&\
	 make populate_db &&\
	 make launch_test_client

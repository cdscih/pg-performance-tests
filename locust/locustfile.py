from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    host = ""

    @task
    def py_conn_pool(self):
        self.client.get(url="http://py_pool:8000/py_pool")

    @task
    def py_std_conn(self):
        self.client.get(url="http://py_std:8001/py_std")

    @task
    def go_conn_pool(self):
        self.client.get(url="http://go_pool:8002/go_pool")

    @task
    def go_std_conn(self):
        self.client.get(url="http://go_std:8003/go_std")

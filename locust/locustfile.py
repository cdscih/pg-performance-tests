from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    host = ""

    @task
    def python_connection_pools(self):
        self.client.get(url="http://python-server:8000/py")

    @task
    def go(self):
        self.client.get(url="http://go-server:8001/go")

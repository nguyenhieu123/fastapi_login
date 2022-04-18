# import random
from locust import HttpUser, task


class test_login(HttpUser):

    @task
    def login_for_access_token(self):
        self.client.post("/login", json = {"email": "user3@example.com",
                "password": "string"})


# class sign_up(HttpUser):
#     @task  
#     def sign_up(self):
#         n = random.randint(10000, 100000)
#         email = str(n) + "@example.com"
#         self.client.post("/sign_up", json={"email": email, "user_name": "test", "password": "string"})

from controller import regius

class Index:
    def get(self, req, resp):
        data = {"welcome": "Welcome, Your Web Successfully Running !"}
        resp.text = regius.template("index.html", data=data)
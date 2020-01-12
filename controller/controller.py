
from controller import regius

class Index:
    def get(self, req, resp):
        data = {"welcome": "Welcome, Your Web Successfully Running !"}
        resp.text = regius.template("index.html", data=data)

class Name:
    def get(self, req, resp, nama):
        resp.text = "Hello " + nama

class SampleRedirect:
    def get(self, req, resp):
        regius.redirect(req, resp, "/halo/Jhon")
from wsgiref import simple_server
from config import app
if __name__ == "__main__":
    httpd = simple_server.make_server('127.0.0.1', 8001, app)
    httpd.serve_forever()

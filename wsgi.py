
# import flask app but need to call it "application" for WSGI to work
from central.main import app as application  # noqa

if  __name__ == "__main__":
    application.run()

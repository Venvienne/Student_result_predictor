from api.index import app

# WSGI entry point
application = app

if __name__ == "__main__":
    application.run()
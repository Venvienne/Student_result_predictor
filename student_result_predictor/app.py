from api.index import app

# This is the entry point that Vercel will use
# Export the Flask app directly
application = app

if __name__ == "__main__":
    app.run()

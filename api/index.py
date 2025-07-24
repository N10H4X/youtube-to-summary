from app import app

# Vercel expects the WSGI application to be named 'app'
if __name__ == "__main__":
    app.run()

import os
import sys
from waitress import serve
from server import app
from dotenv import load_dotenv

load_dotenv(override=True)


def get_env_var(key, default=None):
    return os.environ.get(key) or os.getenv(key, default)


if __name__ == "__main__":
    PORT = int(get_env_var('PORT', 5000))
    ENV = get_env_var('FLASK_ENV', 'development')
    DEBUG = get_env_var('DEBUG', 'False').lower() in ('true', '1', 't')

    print(f"Environment: {ENV}")
    print(f"Debug mode: {DEBUG}")
    print(f"Port: {PORT}")

    if ENV == 'development':
        app.run(debug=DEBUG, port=PORT)
    else:
        print("Starting production server...")
        serve(
            app,
            host='0.0.0.0',
            port=PORT,
            threads=4,
            url_scheme='http'
        )

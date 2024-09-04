from sendwa import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

application = create_app()
application.wsgi_app = ProxyFix(
    application.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == "__main__":
    application.run(debug=True)

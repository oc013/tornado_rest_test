import tornado.ioloop
import tornado.web
import json

from lib.sqlite import SQLite
from lib.model_widget import ModelWidget

# @todo possibly define these as env vars
dbname = 'tornado_rest_test.db'
table_name = 'widgets'

def db_init():
    """ Check if table for the application exists, create it if it does not """
    db = SQLite(dbname)
    model_widget = ModelWidget(db)

    if not db.tables_exist([table_name]):
        model_widget.create_table()
        model_widget.describe()

class IndexHandler(tornado.web.RequestHandler):
    """ Output index page which will have some basic instructions as well as display the widgets
        in the db """
    def get(self):
        self.render("templates/index.html", title="Tornado Rest Test", body_content="Welcome to the show!")

class ApiHandler(tornado.web.RequestHandler):
    """ Handle requests to /api """
    def post(self):
        response = {"language": self.request.headers.get("Accept-Language", "")}
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(response))

def make_app():
    """ Define routes for the application """
    return tornado.web.Application([
        # Static routes
        (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': './css'}),
        (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': './js'}),
        (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': './img'}),
        (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': './img/favicon.ico'}),

        # Dynamic routes
        (r"/", IndexHandler),
        (r"/api", ApiHandler),
    ])

def main():
    db_init()

    app = make_app()
    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()

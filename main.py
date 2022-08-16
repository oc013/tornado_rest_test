import tornado.ioloop
import tornado.web
import json

from lib.sqlite import SQLite
from lib.model_widget import ModelWidget

# @todo possibly define these as env vars
DB_NAME = "tornado_rest_test.db"
TABLE_NAME = "widgets"

class Application(tornado.web.Application):
    """ Define routes for the application and extend so db is a member for all handlers"""

    def __init__(self, db):
        """ Constructor for application """
        self.db = db
        self.model_widget = ModelWidget(db)

        self.db_init()

        routes = [
            # Static routes
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': './css'}),
            (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': './js'}),
            (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': './img'}),
            (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': './img/favicon.ico'}),

            # Dynamic routes
            (r"/", IndexHandler),
            (r"/api/?(.*)", ApiHandler),
        ]

        super().__init__(routes)

    def db_init(self):
        """ Check if table for the application exists, create it if it does not """
        if not self.db.tables_exist([TABLE_NAME]):
            self.model_widget.create_table()
            self.model_widget.describe()

            # @todo remove or move into test harness
            rowid = self.model_widget.insert("test widget 1", 5)
            rowid = self.model_widget.insert("test widget 2", 10)
            rowid = self.model_widget.insert("test widget 3", 15)

class IndexHandler(tornado.web.RequestHandler):
    """ Output index page which will have some basic instructions as well as display the widgets
        in the db
    """
    def get(self):
        self.render("templates/index.html", title="Tornado Rest Test", body_content="<h1>Widget Manager</h1>")

class ApiHandler(tornado.web.RequestHandler):
    """ Handle requests to /api """
    def post(self, path):
        self.route(path)

    def get(self, path):
        self.route(path)

    def route(self, path):
        """ Temporary to allow both gets and posts while testing """
        if path == "create":
            response = self.create()
        elif path == "read":
            response = self.read()
        elif path == "update":
            response = self.update()
        elif path == "delete":
            response = self.delete()
        else:
            raise tornado.web.HTTPError(404)

        self.set_header("Content-Type", "application/json")

        self.write(json.dumps(response))

    def create(self):
        """ Insert a record """
        if self.request.headers['Content-Type'] == 'application/json':
            args = json.loads(self.request.body)
            row_id = self.application.model_widget.insert(args['widget_name'], args['widget_parts'])
        else:
            raise tornado.web.HTTPError(400)

        return {"response": "create", "id": row_id}

    def read(self):
        """ Default behavior returns all records """
        selectAll = True

        if self.request.body and self.request.headers['Content-Type'] == 'application/json':
            args = json.loads(self.request.body)
            if args['id']:
                selectAll = False

        widget_results = self.application.model_widget.select_all() if selectAll else self.application.model_widget.select_one(args['id'])

        return widget_results

    # @todo we're assuming we're getting both fields right now
    def update(self):
        """ Update a record by ID """
        if self.request.headers['Content-Type'] == 'application/json':
            args = json.loads(self.request.body)
            row_id = self.application.model_widget.update(args['widget_id'], args['widget_name'], args['widget_parts'])
        else:
            raise tornado.web.HTTPError(400)

        return {"response": "update"}

    def delete(self):
        """ Delete a record by ID """
        if self.request.headers['Content-Type'] == 'application/json':
            args = json.loads(self.request.body)
            rows_affected = self.application.model_widget.delete(args['id'])
        else:
            raise tornado.web.HTTPError(400)

        return {"response": "delete", "rows": rows_affected}

def main():
    db = SQLite(DB_NAME)

    app = Application(db)
    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()

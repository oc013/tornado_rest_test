""" A simple API and client built and served with Tornado framework """

import json
import tornado.ioloop
import tornado.web

from lib.sqlite import SQLite
from lib.model_widget import ModelWidget

# @todo possibly define these as env vars
DB_NAME = "tornado_rest_test.db"
TABLE_NAME = "widgets"

class Application(tornado.web.Application):
    """ Define routes for the application and extend so db is a member for all handlers"""

    def __init__(self, db):
        """ Constructor for application """
        self.db_conn = db
        self.model_widget = ModelWidget(self.db_conn)

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
        if not self.db_conn.tables_exist([TABLE_NAME]):
            self.model_widget.create_table()
            self.model_widget.describe()

            # @todo remove or move into test harness
            self.model_widget.insert("test widget 1", 5)
            self.model_widget.insert("test widget 2", 10)
            self.model_widget.insert("test widget 3", 15)

class IndexHandler(tornado.web.RequestHandler):
    """ Output index page which will have some basic instructions as well as display the widgets
        in the db
    """
    def get(self):
        """ Handle get request to index page """
        self.render(
            "templates/index.html",
            title="Tornado Rest Test",
            body_content="<h1>Widget Manager</h1>"
        )

class ApiHandler(tornado.web.RequestHandler):
    """ Handle requests to /api """
    def post(self, path):
        """ Route to handle post requests to the api """
        self.route(path)

    def get(self, path):
        """ Route to handle get requests to the api """
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

            validate = self.application.model_widget.validate({
                'name': args['widget_name'],
                'parts': args['widget_parts']
            })

            if not validate["success"]:
                self.set_status(400)
                return {"error": validate["messages"]}

        else:
            raise tornado.web.HTTPError(400)

        row_id = self.application.model_widget.insert(args['widget_name'], args['widget_parts'])

        return {"response": "create", "id": row_id}

    def read(self):
        """ Default behavior returns all records """
        select_all = True

        if self.request.body and self.request.headers['Content-Type'] == 'application/json':
            args = json.loads(self.request.body)

            if args['id']:
                validate = self.application.model_widget.validate({
                    'id': args['id']
                })

                if not validate["success"]:
                    self.set_status(400)
                    return {"error": validate["messages"]}

                select_all = False

        if select_all:
            widget_results = self.application.model_widget.select_all()
        else:
            widget_results = self.application.model_widget.select_one(args['id'])

        return widget_results

    # @todo we're assuming we're getting both fields right now
    def update(self):
        """ Update a record by ID """
        if self.request.headers['Content-Type'] == 'application/json':
            args = json.loads(self.request.body)

            validate = self.application.model_widget.validate({
                'id': args['widget_id'],
                'name': args['widget_name'],
                'parts': args['widget_parts']
            })

            if not validate["success"]:
                self.set_status(400)
                return {"error": validate["messages"]}
        else:
            raise tornado.web.HTTPError(400)

        rows_affected = self.application.model_widget.update(
            args['widget_id'],
            args['widget_name'],
            args['widget_parts']
        )

        return {"response": "update", "rows": rows_affected}

    def delete(self):
        """ Delete a record by ID """
        if self.request.headers['Content-Type'] == 'application/json':
            args = json.loads(self.request.body)

            validate = self.application.model_widget.validate({
                'id': args['id']
            })

            if not validate["success"]:
                self.set_status(400)
                return {"error": validate["messages"]}
        else:
            raise tornado.web.HTTPError(400)

        rows_affected = self.application.model_widget.delete(args['id'])

        return {"response": "delete", "rows": rows_affected}

def main():
    """ Function to wrap starting up the application """
    db_conn = SQLite(DB_NAME)

    app = Application(db_conn)
    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()

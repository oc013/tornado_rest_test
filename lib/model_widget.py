from typing import TypeVar, Type

# @todo revisit this to ensure it is the proper way to type hint
SQLite = TypeVar("lib.sqlite.SQLite")

class ModelWidget():
    """ Defines CRUD operations for Widgets Model """

    def __init__(self, db: SQLite) -> None:
        """ Constructor with dependency injection """
        self.db = db

        self.fields=("id", "name", "parts", "date_created", "date_updated")

        self.validation = {
            "id": ("int", ),
            "name": ("length", 64),
            "parts": ("int", )
        }

    def validate(self, values):
        """ Perform basic validation """
        valid = True
        messages = []
        for key, value in values.items():
            if key in self.validation:
                if self.validation[key][0] == "int" and not value.isdigit():
                    valid = False
                    messages.append(f"{key} is not an integer")
                elif self.validation[key][0] == "length":
                    maxlength = self.validation[key][1]
                    if len(value) > maxlength:
                        valid = False
                        messages.append(f"{key} is longer than {maxlength}")

        return {"success": valid, "messages": messages}

    def create_table(self) -> None:
        """ Create the table schema and triggers """
        self.db.execute('''
            pragma encoding = 'UTF-8';
        ''', ())

        self.db.execute('''
            CREATE TABLE widgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                parts INTEGER,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                date_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''', ())

        self.db.execute('''
            CREATE TRIGGER widget_updated_trigger AFTER UPDATE ON widgets
            BEGIN
                UPDATE widgets SET date_updated = datetime('now') WHERE id = NEW.id;
            END;
        ''', ())

    def describe(self) -> None:
        result = self.db.select("SELECT * FROM sqlite_master", ())
        print(result)

    def insert(self, name: str, parts: int) -> int:
        """ Insert a record """
        rowid = self.db.insert("INSERT INTO widgets (name, parts) VALUES (?, ?)", (name, parts))
        return rowid

    def select_all(self) -> list:
        """ Select all records in table """
        results = self.db.select("SELECT * FROM widgets", ())

        return_results = [dict(zip(self.fields, row)) for row in results]

        return return_results

    def select_one(self, id: int) -> list:
        """ Select one record by id """
        results = self.db.select("SELECT * FROM widgets WHERE id = ?", (id,))
        return_results = dict(zip(self.fields, results[0]))
        return return_results

    # @todo handle if only name or parts number is updated
    def update(self, id: int, name: str, parts: int) -> int:
        """ Update a record by id """
        return self.db.execute("UPDATE widgets SET name = ?, parts = ? WHERE id = ?", (name, parts, id))

    def delete(self, id: int) -> int:
        """ Delete a record by id """
        return self.db.execute("DELETE from widgets WHERE id = ?", (id,))

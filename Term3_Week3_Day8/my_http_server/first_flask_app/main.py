from flask import Flask, request, jsonify, abort
app = Flask(__name__)
import psycopg2

connection = psycopg2.connect(
    database="library_api",
    user="app",
    password="Testing1",
    host="localhost"
)

cursor = connection.cursor()

cursor.execute("create table if not exists books (id serial PRIMARY KEY, title varchar);")
connection.commit()

@app.route("/books", methods=["GET"])
def book_index():
    #Return all books
    sql = "SELECT * FROM books"
    cursor.execute(sql)
    books = cursor.fetchall()
    return jsonify(books)

@app.route("/books", methods=["POST"])
def book_create():
    #Create a new book
    sql = "INSERT INTO books (title) VALUES (%s);"
    cursor.execute(sql, (request.json["title"],))
    connection.commit()

    sql = "SELECT * FROM books ORDER BY ID DESC LIMIT 1"
    cursor.execute(sql)
    book = cursor.fetchone()
    return jsonify(book)

@app.route("/books/<int:id>", methods=["GET"])
def book_show(id):
    #Return a single book
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@app.route("/books/<int:id>", methods=["PUT", "PATCH"])
def book_update(id):
    #Update a book
    sql = "UPDATE books SET title = %s WHERE id = %s;"
    cursor.execute(sql, (request.json["title"], id))
    connection.commit()

    sql = "SELECT * FROM books WHERE id = %s"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@app.route("/books/<int:id>", methods=["DELETE"])
def book_delete(id):
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    
    if book:
        sql = "DELETE FROM books WHERE id = %s;"
        cursor.execute(sql, (id,))
        connection.commit()

    return jsonify(book)
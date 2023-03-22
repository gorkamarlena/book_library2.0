from flask import render_template, request, redirect
from app import app
from app.models import Book, Author, db

@app.route("/")
def index():
    all_books = Book.query.all()
    return render_template("homepage.html", all_books=all_books)

@app.route('/add', methods=['GET'])
def add():
    return render_template("add.html")

@app.route("/add", methods =['POST'])
def add_book():
    title = request.form.get("title")
    authorName = request.form.get("authorName")
    authorLastName = request.form.get("authorLastName")
    authorName2 = request.form.get("authorName2")
    authorLastName2 = request.form.get("authorLastName2")
    b = Book(title = title)
    db.session.add(b)

    if not Author.query.filter(Author.name == authorName, Author.lastName == authorLastName).first():
        a = Author(name = authorName, lastName = authorLastName)
    else:
        a = Author.query.filter(Author.name == authorName, Author.lastName == authorLastName).first()
    b.authors.append(a)
    db.session.add(a)

    if not authorName2 == "":
        if not Author.query.filter(Author.name == authorName2, Author.lastName == authorLastName2).first():
            a2 = Author(name = authorName2, lastName = authorLastName2)
        else:
            a2 = Author.query.filter(Author.name == authorName2, Author.lastName == authorLastName2).first()
        b.authors.append(a2)
        db.session.add(a2)
    db.session.commit()
    return redirect('/')

@app.route('/delete', methods = ['GET'])
def delete():
    return render_template("delete.html")

@app.route('/delete', methods = ['POST'])
def delete_book():
    title = request.form.get("title")
    msg = None
    if Book.query.filter(Book.title == title).first():
        db.session.delete(Book.query.filter(Book.title == title).first())
        db.session.commit()
        msg = 'Book deleted!'
    else:
        msg = 'Book not found!'
    return render_template('delete.html', msg = msg)

@app.route('/find_book', methods = ['GET'])
def find():
    return render_template("update.html")

@app.route('/find_book', methods = ['POST'])
def find_book():
    id = request.form.get("id")
    b = Book.query.filter(Book.id == id).first()
    title = b.title
    authorName = b.authors.all()[0].name
    authorLastName = b.authors.all()[0].lastName
    if len(Book.query.filter(Book.title == title).first().authors.all()) > 1:
        authorName2 = b.authors.all()[1].name
        authorLastName2 = b.authors.all()[1].lastName
    else:
        authorName2 = ""
        authorLastName2 = ""
    
    return render_template('update.html', id = id, title = title, authorName = authorName, authorName2 = authorName2, authorLastName = authorLastName, authorLastName2 = authorLastName2, available = b.is_available)

@app.route("/update", methods =['POST'])
def update_book():
    id = request.form.get('id')
    title = request.form.get("title")
    authorName = request.form.get("authorName")
    authorLastName = request.form.get("authorLastName")
    authorName2 = request.form.get("authorName2")
    authorLastName2 = request.form.get("authorLastName2")
    available = request.form.get('available')
    if available:
        available = True
    else:
        available = False
    
    b = Book.query.filter(Book.id == id).first()
    b.title = title
    b.is_available = available
    db.session.add(b)
    b.authors = []
    if not Author.query.filter(Author.name == authorName, Author.lastName == authorLastName).first():
        a = Author(name = authorName, lastName = authorLastName)
    else:
        a = Author.query.filter(Author.name == authorName, Author.lastName == authorLastName).first()
    b.authors.append(a)
    db.session.add(a)
    
    if not authorName2 == "":
        if not Author.query.filter(Author.name == authorName2, Author.lastName == authorLastName2).first():
            a2 = Author(name = authorName2, lastName = authorLastName2)
        else:
            a2 = Author.query.filter(Author.name == authorName2, Author.lastName == authorLastName2).first()
        b.authors.append(a2)
        db.session.add(a2)
    db.session.commit()
    return redirect('/')
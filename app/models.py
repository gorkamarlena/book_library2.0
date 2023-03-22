from app import db

book_author = db.Table('book_author',
    db.Column('book_id', db.ForeignKey('book.id')),
    db.Column('author_id', db.ForeignKey('author.id'))
)

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = False)
    lastName = db.Column(db.String(100), unique = False)

    def __str__(self):
        return f'{self.name} {self.lastName}'

    def __repr__(self):
        return f'{self.name} {self.lastName}'
    
class Book(db.Model):
    __tablename__  = 'book'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), index = True)
    authors = db.relationship('Author', secondary = book_author, backref ='books', lazy = 'dynamic')
    is_available = db.Column(db.Boolean, default=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

class Available(db.Model):
    __tablename__ ='availability'
    id = db.Column(db.Integer, primary_key = True)
    book = db.Column(db.Integer, db.ForeignKey('book.id'))
    date_borrow = db.Column(db.String(10))
    date_return = db.Column(db.String(10))
    books = db.relationship('Book', backref = 'available')
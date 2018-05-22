from models import Base, User, Genre, Book
from flask import Flask, jsonify, request, url_for
from flask import render_template, redirect, flash
from flask import session as login_session
from flask import make_response
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, asc, exc
from sqlalchemy.pool import StaticPool
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import string
import requests

engine = create_engine(
    'sqlite:///libraryUser.db',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Homepage that shows genres and latest books added
@app.route('/library')
@app.route('/')
def index():
    books = session.query(Book).order_by(Book.id)
    genres = getGenres()
    return render_template('index.html', books=books, genres=genres)


# Show a specific genre and all associated books
@app.route('/genre/<int:genre_id>')
def showGenre(genre_id):
    genres = getGenres()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    books = session.query(Book).filter_by(genre=genre).all()
    return render_template(
        'genre.html', genre=genre, books=books, genres=genres)


# Add a new Genre
@app.route('/genre/add', methods=['GET', 'POST'])
def addGenre():
    if 'username' not in login_session:
        flash('Only logged in Users can edit the Database')
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        newGenre = Genre(
            name=request.form['name'],
            description=request.form['description'],
            user_id=login_session['user_id'])
        session.add(newGenre)
        session.commit()
        flash("%s has been added" % newGenre.name)
        return redirect(url_for('index'))
    else:
        genres = getGenres()
        return render_template('addGenre.html', genres=genres)


# Remove an Existing Genre from the library
@app.route('/genre/<int:genre_id>/delete', methods=['GET', 'POST'])
def removeGenre(genre_id):
    if 'username' not in login_session:
        flash('Only logged in Users can edit the Database')
        return redirect(url_for('showLogin'))
    delGenre = session.query(Genre).filter_by(id=genre_id).one()
    books = session.query(Book).filter_by(genre=delGenre).all()
    if login_session['user_id'] != delGenre.user_id:
        flash("Only the Genre's Creator can delete it")
        return redirect(url_for('index'))
    if books:
        flash('Cannot Delete Genres with assigned books')
        return redirect(url_for('index'))
    if request.method == 'POST':
        session.delete(delGenre)
        session.commit()
        flash("%s has been deleted" % delGenre.name)
        return redirect(url_for('index'))
    else:
        genres = getGenres()
        return render_template(
            'deleteGenre.html', genre=delGenre, genres=genres)


# Show all information for a specific Book
@app.route('/book/<int:book_id>')
def showBook(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    genres = getGenres()
    return render_template('book.html', book=book, genres=genres)


# Add a new book to the database
@app.route('/book/add', methods=['GET', 'POST'])
def addBook():
    if 'username' not in login_session:
        flash('Only logged in Users can edit the Database')
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        bookGenre = session.query(Genre).filter_by(
            name=request.form['genre']).one()
        new_book = Book(title=request.form['title'],
                        author=request.form['author'],
                        genre=bookGenre,
                        description=request.form['description'],
                        user_id=login_session['user_id'])
        session.add(new_book)
        session.commit()
        flash("%s has been added" % new_book.title)
        return redirect(url_for('index'))
    else:
        all_genres = getGenres()
        if not all_genres:
            flash("We need at least one Genre before you can add any books")
            return redirect(url_for('index'))
        return render_template('addBook.html', genres=all_genres)


# Edit an Existing Book in the database
@app.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(book_id):
    if 'username' not in login_session:
        flash('Only logged in Users can edit the Database')
        return redirect(url_for('showLogin'))
    editedBook = session.query(Book).filter_by(id=book_id).one()
    if login_session['user_id'] != editedBook.user_id:
        flash("Only a Book's Creator can edit it")
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form['title']:
            editedBook.title = request.form['title']
        if request.form['author']:
            editedBook.author = request.form['author']
        if request.form['genre']:
            bookGenre = session.query(Genre).filter_by(
                name=request.form['genre']).one()
            editedBook.genre = bookGenre
        if request.form['description']:
            editedBook.description = request.form['description']
        session.add(editedBook)
        session.commit()
        flash("%s has been updated" % editedBook.title)
        return redirect(url_for('index'))
    else:
        all_genres = getGenres()
        return render_template(
            'editBook.html', genres=all_genres, book=editedBook)


# Remove an Existing Book from the library
@app.route('/book/<int:book_id>/delete', methods=['GET', 'POST'])
def removeBook(book_id):
    if 'username' not in login_session:
        flash('Only logged in Users can edit the Database')
        return redirect(url_for('showLogin'))
    del_book = session.query(Book).filter_by(id=book_id).one()
    if login_session['user_id'] != del_book.user_id:
        flash("Only a Book's Creator can delete it")
        return redirect(url_for('index'))
    if request.method == 'POST':
        session.delete(del_book)
        session.commit()
        flash("%s has been deleted" % del_book.title)
        return redirect(url_for('index'))
    else:
        genres = getGenres()
        return render_template('deleteBook.html', book=del_book, genres=genres)


# Create state token and show login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    genres = getGenres()
    return render_template('login.html', STATE=state, genres=genres)


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('index'))
    else:
        flash("You were not logged in")
        return redirect(url_for('index'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user already exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser()
    login_session['user_id'] = user_id
    flash("you are now logged in as %s" % login_session['username'])
    return redirect(url_for('index'))


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s' % access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/'
    url += 'revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/library/JSON')
def allGenresJSON():
    genres = session.query(Genre).all()
    return jsonify(Genres=[gen.serialize for gen in genres])


@app.route('/genre/<int:genre_id>/JSON')
def genreBooksJSON(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    books = session.query(Book).filter_by(genre=genre).all()
    return jsonify(Books=[b.serialize for b in books])


@app.route('/book/<int:book_id>/JSON')
def bookJSON(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(Book=book.serialize)


def getGenres():
    return session.query(Genre).order_by(asc(Genre.name)).all()


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except exc.SQLAlchemyError:
        return None


def createUser():
    newUser = User(
        name=login_session['username'], email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    print 'New User Created!'
    return user.id


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

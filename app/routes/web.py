from flask import Blueprint, render_template, request, redirect, session, url_for
from app import db
from app.models import User, Book
from werkzeug.security import check_password_hash

bp = Blueprint('web', __name__)

@bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('web.login'))
    books = Book.query.all()
    return render_template('index.html', books=books)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            return redirect('/')
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not User.query.filter_by(username=request.form['username']).first():
            user = User(username=request.form['username'])
            user.set_password(request.form['password'])
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    return render_template('register.html')

@bp.route('/add_book', methods=['POST'])
def add_book():
    if 'user_id' not in session:
        return redirect('/login')
    title = request.form['title']
    author = request.form['author']
    db.session.add(Book(title=title, author=author))
    db.session.commit()
    return redirect('/')

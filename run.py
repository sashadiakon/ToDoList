from flask import Flask

app = Flask(__name__)


app.config['SECRET_KEY'] = 'prikol'

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))


from flask_login import LoginManager

login_manager = LoginManager(app)
login_manager.init_app(app)


from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('todos', lazy=True))


@app.route('/')
@login_required
def index():
    todos = current_user.todos
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        todo.user = current_user
        db.session.add(todo)
        db.session.commit()
        flash('Todo added successfully')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo.title = title
        todo.description = description
        db.session.commit()
        flash('Todo updated successfully')
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

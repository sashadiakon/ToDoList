from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Todo, User, Reviews
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("home.html")

@main.route('/profile', methods = ["GET", "POST"])
@login_required
def profile():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, email=current_user.email)
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return "There was an issue adding your task"
        return redirect(url_for('main.profile'))
    else:
        tasks = Todo.query.filter_by(email = current_user.email).order_by(Todo.date_created.desc()).all()
        return render_template('profile.html', current_user=current_user, tasks=tasks)


@main.route('/delete/<int:task_id>')
def delete(task_id):
    task_to_delete = Todo.query.get_or_404(task_id)
    email = Todo.query.filter_by(id = task_id).first().email
    if current_user.email == email:
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/profile')
        except:
            flash('There was a problem deleting that task')
            return redirect(url_for("main.profile"))

    else: 
        flash("You cannot delete another user task")
        return redirect(url_for("main.profile"))


@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    email = Todo.query.filter_by(id = id).first().email
    if request.method == 'POST':
        if current_user.email == email:

            task.content = request.form['content']

            try:
                db.session.commit()
                return redirect(url_for("main.profile"))
            except:
                flash('There was an issue updating your task')
                return redirect(url_for("main.profile"))
        else:
            flash("You can't update another user task")
            return redirect(url_for("main.profile"))

    else:
        print(task)
        print(email)
        return render_template('update.html', task=task)

@main.route("/reviews", methods = ["GET", "POST"])
def reviews():
    if request.method == "POST":
        if current_user.is_authenticated:
            name = request.form['name']
            msg = request.form['msg']
            print(name, msg)
            new_task = Reviews(msg = msg, name=name)
            try:
                db.session.add(new_task)
                db.session.commit()
            except:
                return "There was an issue adding your task"
            return redirect(url_for('main.reviews'))
        else: 
            flash("You must be logged in to leave a review")
            return redirect(url_for("auth.login"))
    else:
        print(dir(current_user))
        print(current_user.is_authenticated)
        reviews = Reviews.query.all()
        return render_template("reviews.html", name = current_user.name, reviews = reviews)
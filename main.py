from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from . import db
from .models import User, Workout


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/new')
@login_required
def new_workout():
    return render_template('create-workout.html')


@main.route('/new', methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form.get('pushups')
    comment = request.form.get('comment')

    workout = Workout(pushups=pushups, comment=comment, author=current_user)
    db.session.add(workout)
    db.session.commit()

    flash('Your workout has been added!')

    return redirect(url_for('main.user_workouts'))


@main.route('/all')
@login_required
def user_workouts():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    workouts = Workout.query.filter_by(author=user).paginate(page=page, per_page=3) # this is responsible for pagination
    return render_template('all-workouts.html', workouts=workouts, user=user)


@main.route('/workout/<int:workout_id>/update', methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']
        db.session.commit()
        flash('Your workout has been updated!')
        return redirect(url_for('main.user_workouts'))

    return render_template('update-workout.html', workout=workout)


@main.route('/workout/<int:workout_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.user_workouts'))

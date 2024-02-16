from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import redirect, url_for, request, flash, abort
main = Blueprint('main', __name__)
from .models import get_db_connection

@main.route('/')
def index():
    print("error====>>>>>>>")
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.email)

@main.route('/new')
@login_required
def new_workout():
    return render_template('create_workout.html', name = current_user.email)


@main.route('/new', methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form.get('pushups')
    comment = request.form.get('comment')
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO workout (push_up, comment, user_id) VALUES ('{pushups}', '{comment}','{current_user.id}') ")
            
            flash('Your new workout Added')
            
            return redirect(url_for('main.user_workouts'))
    
    
    return redirect(url_for('main.profile'))

@main.route('/all')
@login_required
def user_workouts():
    page = request.args.get('page', 1, type=int)
    per_page = 3
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            offset = (page -1) * per_page
            # cur.execute(f"SELECT * FROM workout WHERE user_id = '{current_user.id}'")
            cur.execute(f"SELECT * FROM workout WHERE user_id = %s LIMIT %s OFFSET %s",(current_user.id, per_page, offset ))
            data = cur.fetchall()
            print("data=====>", data)
            if(data and len(data) > 0):
                workouts = data
                total_workouts = get_total_workouts_count(current_user.id)
                total_pages = calculate_total_pages(total_workouts, per_page)
                # workouts = {"pushups" : workouts[1], "date_posted" : workouts[2], "comment" : workouts[4]}
                # print("workouts=====>",workouts["pushups"])
                return render_template('all_workout.html', workouts=workouts, user = "BHANU", page=page, total_pages=total_pages)
            else:
                 return render_template('create_workout.html', name = current_user.email)
             
def get_total_workouts_count(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM workout WHERE user_id = %s", (user_id,))
            total_count = cur.fetchone()[0]
    return total_count

def calculate_total_pages(total_items, per_page):
    return (total_items + per_page - 1) // per_page 


@main.route('/workout/<int:workout_id>/update', methods = ['GET','POST'])
@login_required
def update_workout(workout_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM workout WHERE id = '{workout_id}'")
            data = cur.fetchone()
            if(data):
                workout = data
                if( request.method == 'POST'):
                    pushups = request.form.get('pushups')
                    comment = request.form.get('comment')
                    cur.execute(f"UPDATE workout SET push_up = '{pushups}', comment = '{comment}' WHERE id = '{workout_id}'")
                    flash('Your workout Updated')
                    # conn.commit()
                    return redirect(url_for('main.user_workouts'))
                return render_template('update_workout.html', workout=workout, user = "BHANU")
    
@main.route('/workout/<int:workout_id>/delete', methods = ['GET','POST'])
@login_required
def delete_workout(workout_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM workout WHERE id = '{workout_id}'")
            data = cur.fetchone()
            if(data):
                cur.execute(f"DELETE FROM workout WHERE id = '{workout_id}'")
                flash('Your workout Deleted')
                # conn.commit()
                return redirect(url_for('main.user_workouts'))
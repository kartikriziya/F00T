from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os
from models import db, User, Game, Drive, Play

# Create a Flask Instance
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db with this app
db.init_app(app)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/init-db')
def init_db():
    try:
        with app.app_context():
            # Drop all existing tables
            db.drop_all()
            # Create all tables
            db.create_all()
            # Create a test user
            test_user = User(
                username="coach",
                password="password123"
            )
            db.session.add(test_user)
            db.session.commit()
            return "Database initialized and test user created successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}"








# Create a route decorator

#def index():
#    return "<h1>Hello World!</h1>"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template('components/login.html')

@app.route('/login', methods=['GET', 'POST'])
def onLogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = user.username  # Save username in session
            return redirect(url_for('game_options'))
        flash('Invalid credentials')
    return render_template('components/login.html')

@app.route('/logout')
def onLogout():
    session.pop('username', None)  # Remove the 'username' key from the session
    return redirect(url_for('onLogin'))  # Redirect to login page after logging out

@app.route('/game-options')
def game_options():
    if not session.get('username'):
        return redirect(url_for('index'))  # by default index
    else:
        games = Game.query.all()
        return render_template('components/game_options.html', games=games)

@app.route('/add-game', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        try:
            game = Game(
                game_name=request.form.get('game_name'),
                date=datetime.strptime(request.form.get('date'), '%Y-%m-%d'),
                time=request.form.get('time')
            )
            db.session.add(game)
            db.session.commit()
            flash('Game added successfully!', 'success')
            return redirect(url_for('game_options'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding game: {str(e)}', 'error')
    return render_template('components/add_game.html')

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('components/game_detail.html', game=game)

@app.route('/game/<int:game_id>/add-drive', methods=['POST'])
def add_drive(game_id):
    try:
        drive = Drive(game_id=game_id)
        db.session.add(drive)
        db.session.commit()
        flash('Drive added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding drive: {str(e)}', 'error')
    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/drive/<int:drive_id>/add-play', methods=['GET', 'POST'])
def add_play(drive_id):
    if request.method == 'POST':
        try:
            play = Play(
                drive_id=drive_id,
                quarter=request.form.get('quarter', type=int),
                down=request.form.get('down', type=int),
                distance=request.form.get('distance', type=int),
                yard_line=request.form.get('yard_line', type=int),
                play_type=request.form.get('play_type'),
                play_direction=request.form.get('play_direction'),
                result=request.form.get('result'),
                gain_loss=request.form.get('gain_loss', type=int),
                personnel=request.form.get('personnel'),
                off_form=request.form.get('off_form'),
                form_adj=request.form.get('form_adj'),
                dir_call=request.form.get('dir_call'),
                off_play=request.form.get('off_play')
            )
            db.session.add(play)
            db.session.commit()
            flash('Play added successfully!', 'success')
            return redirect(url_for('drive_detail', drive_id=drive_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding play: {str(e)}', 'error')
    return render_template('components/add_play.html', drive_id=drive_id)

@app.route('/drive/<int:drive_id>')
def drive_detail(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    return render_template('components/drive_detail.html', drive=drive)

@app.route('/game/<int:game_id>/delete', methods=['POST'])
def delete_game(game_id):
    try:
        game = Game.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()
        flash('Game deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting game: {str(e)}', 'error')
    return redirect(url_for('game_options'))

@app.route('/drive/<int:drive_id>/delete', methods=['POST'])
def delete_drive(drive_id):
    try:
        drive = Drive.query.get_or_404(drive_id)
        game_id = drive.game_id
        db.session.delete(drive)
        db.session.commit()
        flash('Drive deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting drive: {str(e)}', 'error')
    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/play/<int:play_id>/delete', methods=['POST'])
def delete_play(play_id):
    try:
        play = Play.query.get_or_404(play_id)
        drive_id = play.drive_id
        db.session.delete(play)
        db.session.commit()
        flash('Play deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting play: {str(e)}', 'error')
    return redirect(url_for('drive_detail', drive_id=drive_id))

@app.route('/play/<int:play_id>/edit', methods=['GET', 'POST'])
def edit_play(play_id):
    # Fetch the play object from the database
    play = Play.query.get_or_404(play_id)
    
    if request.method == 'POST':
        try:
            drive_id=play.drive_id
            # Update the play object with the form data
            play.quarter = request.form.get('quarter', type=int)
            play.down = request.form.get('down', type=int)
            play.distance = request.form.get('distance', type=int)
            play.yard_line = request.form.get('yard_line', type=int)
            play.play_type = request.form.get('play_type')
            play.play_direction = request.form.get('play_direction')
            play.result = request.form.get('result')
            play.gain_loss = request.form.get('gain_loss', type=int)
            play.personnel = request.form.get('personnel')
            play.off_form = request.form.get('off_form')
            play.form_adj = request.form.get('form_adj')
            play.dir_call = request.form.get('dir_call')
            play.off_play = request.form.get('off_play')

            # Commit the updated play to the database
            db.session.commit()

            flash('Play updated successfully!', 'success')
            return redirect(url_for('drive_detail', drive_id=drive_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating play: {str(e)}', 'error')

    # Render the form to edit the play
    return render_template('components/edit_play.html', play=play)



@app.route('/game/<int:game_id>/drivechart')
def drive_chart(game_id):
    game = Game.query.get_or_404(game_id)
    drives = Drive.query.filter_by(game_id=game_id).all()
    
    drives_data = []
    for drive in drives:
        plays = Play.query.filter_by(drive_id=drive.id).order_by(Play.id).all()
        drives_data.append({
            'id': drive.id,
            'result': drive.result or 'Unknown',
            'plays': plays,  # Pass the full plays list
            'play_count': len(plays)
        })
    
    return render_template('components/drive_chart.html', game=game, drives=drives_data)

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {str(e)}")
    app.run(debug=True)
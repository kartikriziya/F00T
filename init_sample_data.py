# init_sample_data.py
from app import app, db
from models import User, Game, Drive, Play
from datetime import datetime

def create_sample_data():
    with app.app_context():
        # First, clear existing data
        db.session.query(Play).delete()
        db.session.query(Drive).delete()
        db.session.query(Game).delete()
        db.session.commit()

        # Create a test game
        game = Game(
            game_name="Seahawks vs Patriots",
            date=datetime(2025, 1, 1),
            time="19:00"
        )
        db.session.add(game)
        db.session.commit()

        # Drive 1 - Touchdown Drive
        drive1 = Drive(game_id=game.id, result="TOUCHDOWN")
        db.session.add(drive1)
        db.session.commit()

        drive1_plays = [
            {
                'quarter': 1, 'down': 1, 'distance': 10, 'yard_line': 25,
                'play_type': 'Run', 'result': 'Rush', 'gain_loss': 5,
                'personnel': '11', 'off_form': 'TRIPS', 'dir_call': 'RIGHT'
            },
            {
                'quarter': 1, 'down': 2, 'distance': 5, 'yard_line': 30,
                'play_type': 'Pass', 'result': 'Complete', 'gain_loss': 15,
                'personnel': '11', 'off_form': 'ACE', 'dir_call': 'LEFT'
            },
            {
                'quarter': 1, 'down': 1, 'distance': 10, 'yard_line': 45,
                'play_type': 'Run', 'result': 'Rush', 'gain_loss': 55,
                'personnel': '21', 'off_form': 'TREY', 'dir_call': 'RIGHT',
                'off_play': 'TOUCHDOWN'
            }
        ]

        # Drive 2 - Punt Drive
        drive2 = Drive(game_id=game.id, result="PUNT")
        db.session.add(drive2)
        db.session.commit()

        drive2_plays = [
            {
                'quarter': 1, 'down': 1, 'distance': 10, 'yard_line': 20,
                'play_type': 'Run', 'result': 'Rush', 'gain_loss': 2,
                'personnel': '11', 'off_form': 'TRIPS', 'dir_call': 'LEFT'
            },
            {
                'quarter': 1, 'down': 2, 'distance': 8, 'yard_line': 22,
                'play_type': 'Pass', 'result': 'Incomplete', 'gain_loss': 0,
                'personnel': '11', 'off_form': 'ACE', 'dir_call': 'RIGHT'
            },
            {
                'quarter': 1, 'down': 3, 'distance': 8, 'yard_line': 22,
                'play_type': 'Pass', 'result': 'Sack', 'gain_loss': -5,
                'personnel': '11', 'off_form': 'TRIPS', 'dir_call': 'RIGHT'
            },
            {
                'quarter': 1, 'down': 4, 'distance': 13, 'yard_line': 17,
                'play_type': 'Punt', 'result': 'Punt', 'gain_loss': 0,
                'personnel': 'ST', 'off_form': 'PUNT', 'dir_call': 'RIGHT'
            }
        ]

        # Drive 3 - Field Goal Drive
        drive3 = Drive(game_id=game.id, result="FIELD GOAL")
        db.session.add(drive3)
        db.session.commit()

        drive3_plays = [
            {
                'quarter': 2, 'down': 1, 'distance': 10, 'yard_line': 35,
                'play_type': 'Pass', 'result': 'Complete', 'gain_loss': 25,
                'personnel': '11', 'off_form': 'TRIPS', 'dir_call': 'RIGHT'
            },
            {
                'quarter': 2, 'down': 1, 'distance': 10, 'yard_line': 60,
                'play_type': 'Run', 'result': 'Rush', 'gain_loss': 8,
                'personnel': '21', 'off_form': 'TREY', 'dir_call': 'LEFT'
            },
            {
                'quarter': 2, 'down': 2, 'distance': 2, 'yard_line': 68,
                'play_type': 'Run', 'result': 'Rush', 'gain_loss': -1,
                'personnel': '21', 'off_form': 'ACE', 'dir_call': 'RIGHT'
            },
            {
                'quarter': 2, 'down': 3, 'distance': 3, 'yard_line': 67,
                'play_type': 'Pass', 'result': 'Incomplete', 'gain_loss': 0,
                'personnel': '11', 'off_form': 'TRIPS', 'dir_call': 'LEFT'
            },
            {
                'quarter': 2, 'down': 4, 'distance': 3, 'yard_line': 67,
                'play_type': 'FG', 'result': 'Field Goal', 'gain_loss': 0,
                'personnel': 'ST', 'off_form': 'FG', 'dir_call': 'CENTER'
            }
        ]

        # Drive 4 - Turnover Drive
        drive4 = Drive(game_id=game.id, result="INTERCEPTION")
        db.session.add(drive4)
        db.session.commit()

        drive4_plays = [
            {
                'quarter': 2, 'down': 1, 'distance': 10, 'yard_line': 30,
                'play_type': 'Run', 'result': 'Rush', 'gain_loss': 4,
                'personnel': '21', 'off_form': 'TREY', 'dir_call': 'RIGHT'
            },
            {
                'quarter': 2, 'down': 2, 'distance': 6, 'yard_line': 34,
                'play_type': 'Pass', 'result': 'Interception', 'gain_loss': 0,
                'personnel': '11', 'off_form': 'TRIPS', 'dir_call': 'LEFT'
            }
        ]

        # Add plays for each drive
        for play_data in drive1_plays:
            play = Play(drive_id=drive1.id, **play_data)
            db.session.add(play)

        for play_data in drive2_plays:
            play = Play(drive_id=drive2.id, **play_data)
            db.session.add(play)

        for play_data in drive3_plays:
            play = Play(drive_id=drive3.id, **play_data)
            db.session.add(play)

        for play_data in drive4_plays:
            play = Play(drive_id=drive4.id, **play_data)
            db.session.add(play)

        db.session.commit()
        print("Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()
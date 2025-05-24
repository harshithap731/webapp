from app import create_app
from app.utils import load_users_from_csv
from app import db

app = create_app()

with app.app_context():
    db.create_all()
    load_users_from_csv('users.csv')  # Load initial users from CSV

if __name__ == '__main__':
    app.run(debug=True, port=5648)


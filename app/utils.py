import csv
from app.models import User
from app import db, bcrypt

def load_users_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not User.query.filter_by(email=row['email']).first():
                hashed_password = bcrypt.generate_password_hash(row['password']).decode('utf-8')
                user = User(username=row['username'], email=row['email'], password=hashed_password)
                db.session.add(user)
        db.session.commit()

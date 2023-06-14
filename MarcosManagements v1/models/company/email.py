from models import db, User
from datetime import datetime

class Email(db.Model):
    __tablename__ = "emails"
    id = db.Column("id",  db.Integer(), primary_key = True)
    from_id = db.Column(db.Integer())
    to_id = db.Column(db.Integer())
    from_name = db.Column(db.String(30), nullable=False)
    to_name = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(3000))
    date_time = db.Column("date_time", db.DateTime(), nullable=False, default=datetime.now())

    def save_email(from_id, to_id, content):
        from_name = User.get_user_by_id(from_id).username
        to_name = User.get_user_by_id(to_id).username

        email = Email(from_id=from_id, to_id=to_id, from_name=from_name, to_name=to_name, content=content)

        db.session.add(email)
        db.session.commit()

    def get_email_by_id(id):
        email = Email.query.filter_by(id=id).first()
        
        return email

    def get_emails(user_id):
        emails = Email.query.filter_by(to_id=user_id).all()
        
        return emails
    
    def get_emails_sent(user_id):
        emails = Email.query.filter_by(from_id=user_id).all()
        
        return emails
    
    def delete_email(id):
        try:
            Email.query.filter_by(id=id).delete()
            db.session.commit()
            return True
        except:
            return False
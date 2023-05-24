from models import db, User, Company

class Worker(db.Model):
    __tablename__ = "workers"
    id = db.Column("id",  db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id), primary_key = True)
    company_id = db.Column(db.Integer(), db.ForeignKey(Company.id), primary_key = True)
    function = db.Column(db.String(30))
    sector = db.Column(db.String(30))
    working_hours = db.Column(db.Float())
    salary = db.Column(db.Float())

    def save_worker(user_id, company_id, function, sector, working_hours, salary):
        worker = Worker(user_id=user_id, company_id=company_id, function=function, sector=sector, working_hours=working_hours, salary=salary)

        db.session.add(worker)
        db.session.commit()
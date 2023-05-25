from models import db, User, Company

class Worker(db.Model):
    __tablename__ = "workers"
    id = db.Column("id",  db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    company_id = db.Column(db.Integer(), db.ForeignKey(Company.id))
    function = db.Column(db.String(30))
    sector = db.Column(db.String(30))
    working_hours = db.Column(db.Float())
    salary = db.Column(db.Float())

    def save_worker(username, company_id, function, sector, working_hours, salary):
        user = User.query.filter_by(username=username).first()
        worker = Worker(user_id=user.id, company_id=company_id, function=function, sector=sector, working_hours=working_hours, salary=salary)

        db.session.add(worker)
        db.session.commit()
    
    def save_worker_changes(data):
        Worker.query.filter_by(id=data['id'])\
                .update(dict(function=data['function'], sector = data['sector'], 
                        working_hours = data['working_hours'], salary = data['salary']))
        
        Company.query.filter_by(id=data['id'])
        db.session.commit()

    def delete_worker(id):
        try:
            Company.query.filter_by(id=id).delete()
            Worker.query.filter_by(id=id).delete()
            db.session.commit()
            return True
        except:
            return False
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

    payments = db.relationship("Payment", backref="workers", lazy=True)

    def get_worker(id):
        return Worker.query.filter_by(id=id).join(User, User.id == Worker.user_id)\
            .add_columns(Worker.id, User.username).first()
    
    def get_worker_by_user_id(user_id, company_id):
        return Worker.query.filter_by(user_id=user_id, company_id=company_id).first()

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
            Worker.query.filter_by(id=id).delete()
            db.session.commit()
            return True
        except:
            return False
        
    def get_worker_by_company_id(company_id):
        return Worker.query.filter_by(company_id=company_id).join(User, User.id == Worker.user_id)\
            .add_columns(Worker.id, User.username, User.name, Worker.function, Worker.sector, Worker.working_hours, Worker.salary)\
            .all()

    def get_working_companies(user_id):

        return Worker.query.filter_by(user_id=user_id).join(Company, Company.id == Worker.company_id)\
            .add_columns(Company.id, Company.name).all()
from models import db, Worker, User, Company
from datetime import datetime

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column("id",  db.Integer(), primary_key = True)
    worker_id = db.Column(db.Integer(), db.ForeignKey(Worker.id))
    value = db.Column(db.Float())
    date_time = db.Column("date_time", db.DateTime(), nullable=False, default=datetime.now())
    

    def save_payment(worker_id):
        worker = Worker.get_worker(worker_id)

        payment = Payment(worker_id=worker_id, value=worker.salary)

        db.session.add(payment)
        db.session.commit()

    def get_all_payments():
        payments = Payment.query\
            .join(Worker, Worker.id == Payment.worker_id)\
            .join(User, User.id == Worker.user_id)\
            .join(Company, Company.id == Worker.company_id)\
            .add_columns(
                Company.name,
                Worker.id,
                User.username,
                Payment.value,
                Payment.date_time
            ).all()
        
        return payments
    
    def get_company_payments(company_id):
        workers = Worker.get_worker_by_company_id(company_id)
        payments = []

        for worker in workers:
            for payment in Payment.get_worker_payments(worker.id):
                payments.append(payment)

        return payments
    
    def get_worker_payments(id):
        payments = Payment.query.filter_by(worker_id=id)\
            .join(Worker, Worker.id == Payment.worker_id)\
            .join(User, User.id == Worker.user_id)\
            .add_columns(
                Worker.id,
                User.username,
                Payment.value,
                Payment.date_time
            ).all()

        return payments
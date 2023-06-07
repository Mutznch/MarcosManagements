"""from models import db, Worker

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column("id",  db.Integer(), primary_key = True)
    worker_id = db.Column(db.Integer(), db.ForeignKey(Worker.id))
    paid = db.Column(db.Booloean())

    def save_company(owner_id, name):
        company = Company(owner_id=owner_id, name=name)

        db.session.add(company)
        db.session.commit()

    def get_all_companies():
        companies = Company.query\
            .join(User, User.id == Company.owner_id)\
            .add_columns(
                User.id,
                User.username, 
                Company.name,
        ).all()
        
        return companies
    
    def get_workers(id):
        company = Company.query.filter_by(id=id).first()

        return company.workers
    
    def get_my_companies(user_id):

        user = User.query.get(user_id)

        my_companies = user.companies

        #owned_companies = 

        return my_companies """
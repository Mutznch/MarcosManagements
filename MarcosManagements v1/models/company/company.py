from models import db, User

class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column("id",  db.Integer(), primary_key = True)
    owner_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    name = db.Column(db.String(30))

    workers = db.relationship("Worker", backref="companies", lazy=True)
    devices = db.relationship("Device", backref="companies", lazy=True)

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

        return my_companies 
    
    def delete_company(id):
        try:
            Company.query.filter_by(id=id).delete()
            db.session.commit()
            return True
        except:
            return False
        
    def update_company(id, name):
        Company.query.filter_by(id=id)\
                .update(dict(name=name))
        
        Company.query.filter_by(id=id)
        db.session.commit()

    def get_company_by_id(id):
        company = Company.query.filter_by(id=id).first()
        
        return company
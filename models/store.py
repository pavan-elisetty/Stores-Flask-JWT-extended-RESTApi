from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer , primary_key = True)
    name=db.Column(db.String(80))

    items = db.relationship('ItemModel' , lazy = 'dynamic')

    def __init__(self,name):
        self.name = name

    def json(self):
        return {
            'id':self.id,
            'name':self.name ,
            'items':[item.json() for item in self.items.all()]
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

                                                                          #acting as query builder
    @classmethod
    def find_by_name(cls, name): #cls==ItemModel
        return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name=name LIMIT 1


    def save_to_db(self):
        db.session.add(self)   #this method is useful to both update and insert
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # starships = db.relationship('Starship', backref='users', lazy=True)
    # planet = db.relationship('Planet', backref='users', lazy=True)
    # favorites = db.relationship('Favorite', backref='user', lazy=True)





    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            # do not serialize the password, it's a security breach
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    # planet = db.relationship('Planet', backref='character', lazy=True)


    def __repr__(self):
        return '<Character %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return '<Planet %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate
        }

class Starship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # character_id  = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    # character = db.relationship('Character', backref='starship', lazy=True)

    def __repr__(self):
        return '<Starship %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # "character_id": self.character_id
        }

class Favorite(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'), nullable=True)

    user = db.relationship('User', backref='favorites')
    planet = db.relationship('Planet', backref='favorites')
    character = db.relationship('Character', backref='favorites')
    starship = db.relationship('Starship', backref='favorites')

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        serialized_data = {
            "id": self.id,
            "user_id": self.user_id
        }
        if self.planet_id is not None:
            serialized_data["planet_id"] = self.planet_id
        if self.character_id is not None:
            serialized_data["character_id"] = self.character_id
        if self.starship_id is not None:
            serialized_data["starship_id"] = self.starship_id

        return serialized_data
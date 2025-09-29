from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Author must have a name.")

        #  Custom check for uniqueness
        existing_author = Author.query.filter_by(name=value).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError("Author name must be unique.")

        return value

    @validates("phone_number")
    def validate_phone(self, key, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("content")
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return value

    @validates("summary")
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Summary must be a maximum of 250 characters.")
        return value

    @validates("category")
    def validate_category(self, key, value):
        if value not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return value

    @validates("title")
    def validate_title(self, key, value):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Title must be clickbait-y (contain 'Won't Believe', 'Secret', 'Top', or 'Guess').")
        return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
from flask_sqlalchemy import SQLAlchemy
from .views import app
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'app.db')}"

# Start connection with the database
db = SQLAlchemy(app)

"""
>>> from csapp.models import db
>>> from csapp.models import CheatSheetContent
>>> db.create_all()
>>> CheatSheetContent.query.all()

"""


class CheatSheetContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    h1 = db.Column(db.String(200), nullable=False)  # This title cannot be empty
    h2 = db.Column(db.String(200))
    cell1 = db.Column(db.Text)
    cell2 = db.Column(db.Text)
    syntax = db.Column(db.Text)
    example_content = db.Column(db.Text)
    example_caption = db.Column(db.Text)
    method = db.Column(db.Text)
    method_description = db.Column(db.Text)
    link = db.Column(db.Text)
    link_href = db.Column(db.Text)
    link_type = db.Column(db.String(10), default='code')

    def __init__(self, h1, h2, cell1, cell2, syntax, example_content, example_caption, method, method_description, link,
                 link_href, link_type):
        self.h1 = h1
        self.h2 = h2
        self.cell1 = cell1
        self.cell2 = cell2
        self.syntax = syntax
        self.example_content = example_content
        self.example_caption = example_caption
        self.method = method
        self.method_description = method_description
        self.link = link
        self.link_href = link_href
        self.link_type = link_type

    def __repr__(self):
        return f'CheatSheetContent {self.id}'


def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
    db.session.add(CheatSheetContent(h1="pandas.Series",
                   h2="",
                   cell1="pandas.Series.value_counts",
                   cell2="Return a Series containing counts of unique values.",
                   syntax="Series.value_counts(self, normalize=False, sort=True, ascending=False, bins=None, dropna=True)",
                   example_content="",
                   example_caption="",
                   method="",
                   method_description="",
                   link="Exercise 2.4.2: How thresholds affect performance, Credit Risk Modeling in Python (Datacamp), Chapter 2: Logistic Regression for Defaults, Section 2.4: Model discrimination and impact",
                   link_href="C:/Users/YBant/Documents/projects/my_wiki/content/datacamp/credit_risk_modeling/chapter2.html#how_thresholds_affect_performance",
                   link_type="code"))
    db.session.commit()


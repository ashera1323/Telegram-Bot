from peewee import *
import settings

db = settings.DB


class BaseModel(Model):
    class Meta:
        database = db


class Course(BaseModel):
    name = TextField()
    text = TextField(null=True)
    announcement = TextField(null=True)


class Week(BaseModel):
    name = TextField(null=True)
    order = IntegerField()
    course = ForeignKeyField(Course)
    announcement = TextField(null=True)


class Task(BaseModel):
    name = TextField()
    order = IntegerField()
    week = ForeignKeyField(Week)
    contest = TextField()
    review = TextField()


class User(BaseModel):
    date_start = DateField(null=True)
    chat_id = BigIntegerField(unique=True, null=True)
    alias = TextField(unique=True)
    task = ForeignKeyField(Task, null=True)
    access = IntegerField()
    name = TextField(null=True)
    surname = TextField(null=True)
    course = ForeignKeyField(Course)




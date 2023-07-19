from peewee import (Model, SqliteDatabase, IntegerField, 
                    BooleanField, ForeignKeyField, CharField,
                    TextField)


db = SqliteDatabase('aqulangustin.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        db_table = 'user'
    
    vk_id = IntegerField()
    state = IntegerField(default=0)
    messages_allowed = BooleanField()
    edit_flag = BooleanField(null=True)
    offset = IntegerField(null=True)


class Order(BaseModel):
    class Meta:
        db_table = 'order_'

    user = ForeignKeyField(User)
    location = CharField(max_length=500, null=True)
    datetime = CharField(max_length=500, null=True)
    other_info = CharField(max_length=1000, null=True)
    edit_mode = BooleanField(default=False)


class Feedback(BaseModel):
    class Meta:
        db_table = "feedback"

    user = ForeignKeyField(User)
    message_id = CharField(max_length=500)
    is_published = BooleanField(default=False)
    on_moderation = BooleanField(default=True)


if __name__ == "__main__":
    db.create_tables([User, Order, Feedback])
    
from datetime import datetime

from pydantic import BaseModel
from firestorm import Base


class User(Base):
    class Model(BaseModel):
        id: str
        created: datetime


class Post(Base):
    class Model(BaseModel):
        id: str
        text: str


class Comment(Base):
    class Model(BaseModel):
        id: str
        comment: str = 'this blog sucks!'


# u1 = User(id='1', created=datetime.now())
# u2 = User(id='2', created=datetime.now())
# u3 = User(id='3', created=datetime.now())
# u1.save()
# u2.save()
# u3.save()


# with Post.parents(u1):
#     p1 = Post(id='1', text='My coooooool post!')
#     p2 = Post(id='2', text='My coooooool post!')
#     p3 = Post(id='3', text='My coooooool post!')
#     p1.save()
#     p2.save()
#     p3.save()


doc = User.collection().document('1').get()
print(doc.to_dict())
import logging
logging.basicConfig(level=logging.DEBUG)
for item in User.where('created', '>', '1').stream():
    print('nice')

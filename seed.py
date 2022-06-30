from models import *
from app import app

db.drop_all()
db.create_all()
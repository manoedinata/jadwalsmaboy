from flask import Blueprint

from .database import db
from .database import Siswa
from .whatsapp import do_send

routes = Blueprint("routes", __name__)

@routes.get("/")
def home():
    return "Hello, World!"

@routes.get("/send")
def send():
    return do_send()

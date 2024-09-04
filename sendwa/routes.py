from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from .database import db
from .database import Siswa
from .whatsapp import do_send

routes = Blueprint("routes", __name__)

@routes.get("/")
def home():
    return "Hello, World!"

@routes.get("/siswa")
def siswa():
    return [s.serialize for s in Siswa.query.all()]

@routes.route("/siswa/add", methods=["GET", "POST"])
def siswa_add():
    if request.method == "GET":
        return render_template("add.html")

    nama = request.form.get("nama")
    panggilan = request.form.get("panggilan")
    kelas = request.form.get("kelas")
    nomor = request.form.get("nomor")

    siswa = Siswa(nama=nama, panggilan=panggilan, kelas=kelas, nomor=nomor)
    db.session.add(siswa)
    db.session.commit()

    return redirect(url_for("routes.siswa"))

@routes.get("/send")
def send():
    return do_send()

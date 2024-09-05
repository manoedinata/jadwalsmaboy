from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from .config import BOT_TOKEN
from .database import db
from .database import Siswa
from .whatsapp import sendMessage
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

    greetingTexts = ""
    greetingTexts += f"Halo, {nama} 👋 \n"
    greetingTexts += "\n"
    greetingTexts += "Terima kasih sudah mendaftar layanan jadwal otomatis. "
    greetingTexts += "Notifikasi jadwal akan dikirimkan ke kamu melalui nomor ini. "
    greetingTexts += "Silahkan di-save jika mau. \n"
    greetingTexts += "\n"
    greetingTexts += "Layanan akan dimulai secepatnya. \n"
    greetingTexts += "\n"
    greetingTexts += f"Nama: *{nama}* \n"
    if panggilan: greetingTexts += f"Panggilan kustom: *{panggilan}* \n"
    greetingTexts += f"Kelas: *{kelas}* \n"

    send = sendMessage(greetingTexts, nomor, BOT_TOKEN)
    print(send)

    return redirect(url_for("routes.siswa"))

@routes.get("/send")
def send():
    return do_send()

import requests
from datetime import datetime, timedelta
from typing import Optional

from .config import BOT_TOKEN
from .database import db
from .database import Siswa

FONTE_WHATSAPP_SEND_API = "https://api.fonnte.com/send"

# TODO: Gunakan timezone Asia/Jakarta
hariIni = datetime.today()
besok = hariIni + timedelta(days=1)
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"] # TODO: Gunakan array yang lebih baik

DATA_URL = "https://jadwal.sman1boyolangu.sch.id/kelas/"

def getKelasInfo(url: str = DATA_URL + "info.json") -> dict:
    req = requests.get(url)
    return req.json()

def getJadwalData(kelas: str) -> dict:
    req = requests.get(DATA_URL + f"{kelas}.json")
    return req.json()

def parseJadwal(data: list, tanggal: int) -> Optional[dict]:
    if tanggal > len(data) - 1:
        return

    return data[tanggal]

def sendMessage(message: str, number: str, bot_token: str, url: str = FONTE_WHATSAPP_SEND_API):
    req = requests.post(url, headers={
        "Authorization": bot_token
    }, json={
        "target": number,
        "message": message,
        "typing": True
    })

    return req.json()

def addSiswa(nama: str, panggilan: str, kelas: str, nomor: int):
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

    return siswa.serialize

def do_send():
    # Cek jika besok libur
    if besok.weekday() > len(HARI) - 1:
        print(f"Jadwal untuk besok tidak ada!")
        return

    # Cek jika gaada siswa
    siswa = Siswa.query.all()
    if len(siswa) < 1:
        print("Tidak ada siswa terdaftar!")
        return

    for s in siswa:
        print(s.nama)
        # Initialize WhatsApp message text
        whatsappText = ""
        whatsappText += f"*Semangat, {s.panggilan if s.panggilan else s.nama}! 🔥* \n"
        whatsappText += "\n"
        whatsappText += f"Jadwal Pelajaran untuk kelas {s.kelas} \n"
        whatsappText += "\n"
        whatsappText += f"Hari: *{HARI[besok.weekday()]}* \n"
        whatsappText += "\n"

        print(f"Mengambil data jadwal...")
        jadwalData = getJadwalData(s.kelas)
        jadwal = parseJadwal(jadwalData, besok.weekday())
        if not jadwal:
            print(f"Jadwal {s.kelas} untuk besok tidak ada!")
            continue

        # Update text
        sendText = whatsappText.format(s.kelas)
        for j in jadwal:
            jam = j["jam"]
            mapel = j["keterangan"]
            sendText += f"Jam ke-{jam}: *{mapel}* \n"
        print(sendText)

        send = sendMessage(sendText, s.nomor, BOT_TOKEN)
        print(send)

    return "send jadwal"

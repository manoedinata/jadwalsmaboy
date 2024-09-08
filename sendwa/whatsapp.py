import requests
from datetime import datetime, timedelta
from typing import Optional
import time, random

from .config import BOT_TOKEN
from .database import db
from .database import Siswa
from .utils import getRandomGreet

WAHA_API = "http://arthur.manoedinata.com:27004/api"

# TODO: Gunakan timezone Asia/Jakarta
hariIni = datetime.today()
besok = hariIni + timedelta(days=1)
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"] # TODO: Gunakan array yang lebih baik

DATA_URL = "https://jadwal.sman1boyolangu.sch.id/kelas/"

def setTyping(nomor: str, typing: bool = True) -> bool:
    if typing:
        typingUrl = WAHA_API + "/startTyping"
    else:
        typingUrl = WAHA_API + "/stopTyping"

    req = requests.post(typingUrl, json={
        "chatId": nomor + "@c.us",
        "session": "default"
    })

    print(req.json())
    return True

def sendSeenToChat(nomor: str, messageId: str):
    req = requests.post(WAHA_API + "/sendSeen", json={
        "chatId": nomor + "@c.us",
        "messageId": messageId,
        "participant": None,
        "session": "default"
    })

    return req.ok

def checkIfSiswaHasMessage(nomor: str) -> bool:
    req = requests.get(WAHA_API + f"/default/chats/{nomor + '@c.us'}/messages")

    if not req.ok: return False
    if len(req.json()) < 1: return False

    # Send seen
    messageId = req.json()[-1]["id"]
    sendSeen = sendSeenToChat(nomor, messageId)
    # if not sendSeen: return False

    return True

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

def sendMessage(message: str, number: str, bot_token: str, url: str = WAHA_API + "/sendText"):
    req = requests.post(url, json={
        "chatId": number + "@c.us",
        "reply_to": None,
        "text": message,
        "session": "default"
    })

    print(req.json())
    return req

def addSiswa(nama: str, panggilan: str, kelas: str, nomor: int, greetSiswa: bool = True):
    # Cek apakah siswa pernah chat duluan
    siswa = checkIfSiswaHasMessage(nomor)
    if not siswa: return {"error": "Siswa belum pernah chat bot"}, 400

    siswa = Siswa.query.filter_by(nomor=nomor).first()
    if siswa:
        print("Siswa sudah ada")
        return {"error": "Siswa sudah ada"}, 400

    siswa = Siswa(nama=nama, panggilan=panggilan, kelas=kelas, nomor=nomor)
    db.session.add(siswa)

    if greetSiswa:
        # Typing: ON
        setTyping(nomor, True)

        greetingTexts = ""
        greetingTexts += f"{getRandomGreet()}, {nama} 👋 \n"
        greetingTexts += "\n"
        greetingTexts += "Kamu sudah mendaftar layanan jadwal otomatis. "
        greetingTexts += "Notifikasi jadwal akan dikirimkan ke kamu melalui nomor ini. "
        greetingTexts += "Silahkan di-save jika ingin. \n"
        greetingTexts += "\n"
        greetingTexts += f"Nama: *{nama}* \n"
        if panggilan: greetingTexts += f"Panggilan kustom: *{panggilan}* \n"
        greetingTexts += f"Kelas: *{kelas}* \n"
        print(greetingTexts)

        # Typing: OFF
        setTyping(nomor, False)

        try:
            send = sendMessage(greetingTexts, nomor, BOT_TOKEN)
            print(send.json())
            if not send.ok:
                db.session.rollback()
                return

            print(send.json())
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return

    db.session.commit()
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

        # Cek apakah siswa pernah chat duluan
        cekSiswa = checkIfSiswaHasMessage(s.nomor)
        if not cekSiswa: continue

        # Cek apakah pesan sdh dikirim sebelumnya
        if s.last_sent and (s.last_sent.date() == datetime.today().date()):
            print("Jadwal telah terkirim sebelumnya")
            continue

        # Typing: ON
        setTyping(s.nomor, True)

        # Initialize WhatsApp message text
        whatsappText = ""
        whatsappText += f"*{getRandomGreet()}, {s.panggilan if s.panggilan else s.nama}! 🔥* \n"
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

        # Typing: OFF
        setTyping(s.nomor, False)

        send = sendMessage(sendText, s.nomor, BOT_TOKEN)
        print(send)

        # Update last sent
        s.last_sent = datetime.now()
        db.session.add(s)
        db.session.commit()

        # TODO: Ini harusnya async. Klo synchronous bakalan lemot
        time.sleep(random.randint(60, 120))

    return "send jadwal"

import requests
from datetime import datetime, timedelta

from .config import BOT_TOKEN
from .database import Siswa
from .utils import *

FONTE_WHATSAPP_SEND_API = "https://api.fonnte.com/send"

# TODO: Gunakan timezone Asia/Jakarta
hariIni = datetime.today()
besok = hariIni + timedelta(days=1)
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"] # TODO: Gunakan array yang lebih baik

def sendMessage(message: str, number: str, bot_token: str, url: str = FONTE_WHATSAPP_SEND_API):
    req = requests.post(url, headers={
        "Authorization": bot_token
    }, json={
        "target": number,
        "message": message,
        "typing": True
    })

    return req.json()

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

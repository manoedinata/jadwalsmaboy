import os
import asyncio
from datetime import datetime
from datetime import timedelta

from .retrieve import getKelasInfo
from .retrieve import getJadwalData
from .retrieve import parseJadwal

from .whatsapp import sendMessage

# Check if we must use configuration from env
ENV = os.environ.get("ENV")
if ENV:
    from . import Config
    config = Config(
        group_id=os.environ.get("GROUP_ID"),
        bot_token=os.environ.get("BOT_TOKEN")
    )
else:
    from .config import config

# TODO: Gunakan timezone Asia/Jakarta
hariIni = datetime.today()
besok = hariIni + timedelta(days=1)
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"] # TODO: Gunakan array yang lebih baik

# Initialize WhatsApp message text
whatsappText = ""
whatsappText += "*Jadwal Pelajaran* \n"
whatsappText += "\n"
whatsappText += "Kelas: *{}* \n"
whatsappText += f"Hari: *{HARI[besok.weekday()]}* \n"
whatsappText += "\n"

async def main():
    print("Mengambil informasi kelas...")
    kelasInfo = await getKelasInfo()

    for jenjang in kelasInfo:
        for kelas in jenjang["kelas"]:
            nomorGrup = config.group_id.get(kelas)
            if not nomorGrup:
                print(f"Nomor grup {kelas} tidak ada! Skip")
                continue

            print(f"Mengambil data jadwal ({kelas})...")
            jadwalData = await getJadwalData(kelas)
            jadwal = parseJadwal(jadwalData, besok.weekday())
            if not jadwal:
                print(f"Jadwal {kelas} untuk besok tidak ada!")
                continue

            # Update text
            sendText = whatsappText.format(kelas)
            for j in jadwal:
                jam = j["jam"]
                mapel = j["keterangan"]
                sendText += f"Jam ke-{jam}: *{mapel}* \n"
            print(sendText)

            # Send message
            send = await sendMessage(sendText, nomorGrup, config.bot_token)
            print(send)

    return

asyncio.run(main())

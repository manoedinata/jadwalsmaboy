import requests
from typing import Optional

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

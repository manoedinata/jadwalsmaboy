import httpx
from typing import Optional

DATA_URL = "https://jadwal.sman1boyolangu.sch.id/kelas/"
INFO_URL = DATA_URL + "info.json"

async def getKelasInfo(url: str = INFO_URL) -> dict:
    async with httpx.AsyncClient() as client:
        req = await client.get(url)
        return req.json()

async def getJadwalData(kelas: str) -> dict:
    async with httpx.AsyncClient() as client:
        req = await client.get(DATA_URL + f"{kelas}.json")
        return req.json()

def parseJadwal(data: list, tanggal: int) -> Optional[dict]:
    if tanggal > len(data) - 1:
        return

    return data[tanggal]

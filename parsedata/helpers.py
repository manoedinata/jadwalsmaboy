from openpyxl.worksheet.worksheet import Worksheet

# Iterate each element in list
# and add them in variable total
def jumlahkanList(list: list) -> int:
    total = 0
    for ele in range(len(list)):
        total += list[ele]

    return total

# Get jadwal information
def getDetailGuru(index: int, worksheet: Worksheet) -> dict:
    guru_info = {}
    for row in worksheet.iter_rows(min_row=3, max_row=worksheet.max_row):
        index_guru = row[0].value
        if index_guru != index:
            continue

        nama_guru = row[1].value
        keterangan_guru = row[3].value

        guru_info = {
            "index": index_guru,
            "nama": nama_guru,
            "keterangan": keterangan_guru
        }

    return guru_info

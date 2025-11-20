import os

# Klasör yoksa oluştur
if not os.path.exists("data"):
    os.makedirs("data")

# CSV içeriği (Faz 1 verisi)
csv_content = """dock_id,arrival_time,departure_time
0,08:15,09:00
1,07:30,10:45
2,09:00,11:00
0,13:00,14:00
3,10:00,12:30
4,15:00,16:00
1,14:00,18:00
5,00:00,02:00
6,20:00,23:59
2,14:00,15:00"""

# Dosyayı yaz
with open("data/raw_logs.csv", "w") as f:
    f.write(csv_content)

print("✅ raw_logs.csv oluşturuldu!")
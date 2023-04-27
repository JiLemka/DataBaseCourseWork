import sqlite3


def connect_db():
    db_connection = None
    try:
        db_connection = sqlite3.connect('ElectroStore.sqlite')
    except sqlite3.Error as e:
        print(e)
    return db_connection


def select_wish_list_item(conn, client_id, device_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Wish_list WHERE client_id = ? AND device_id = ?", (client_id, str(device_id)))
    item = c.fetchall()
    return item


def select_cart_list_item(conn, client_id, device_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Cart_list WHERE client_id = ? AND device_id = ?", (client_id, device_id))
    item = c.fetchall()
    return item


def select_wish_list_items(conn, client_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Wish_list WHERE client_id = ?", str(client_id))
    items = c.fetchall()
    return items


def select_cart_list_items(conn, client_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Cart_list WHERE client_id = ?", client_id)
    items = c.fetchall()
    return items


def select_reservations(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Reservation")
    reservations = c.fetchall()
    return reservations


def select_client_reservations(conn, client_id, status_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Reservation WHERE client_id = ? and status_id = ?", (client_id, status_id,))
    items = c.fetchall()
    return items


def select_device(conn, device_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Device WHERE id = ?", (str(device_id),))
    device = c.fetchall()
    return device


def select_client(conn, login, password):
    c = conn.cursor()
    c.execute("SELECT * FROM Client WHERE client_login = ? AND client_password = ?", (login, password))
    client = c.fetchall()
    return client


def select_client_by_id(conn, client_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Client WHERE id = ?", (client_id,))
    client = c.fetchall()
    return client[0]


def select_worker(conn, login, password):
    c = conn.cursor()
    c.execute("SELECT * FROM Worker WHERE worker_login = ? AND worker_password = ?", (login, password))
    worker = c.fetchall()
    return worker


def select_companies(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Company")
    companies = c.fetchall()
    return companies


def select_devices(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Device")
    devices = c.fetchall()
    return devices


def select_device_types(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Company")
    companies = c.fetchall()
    return companies


def insert_client(conn, name, phone, login, password) -> bool:
    c = conn.cursor()
    c.execute("INSERT INTO Client (client_name, client_phone, client_login, client_password) VALUES (?,?,?,?)",
              (name, phone, login, password,))
    conn.commit()
    return True


def insert_wish_list_item(conn, client_id, device_id) -> bool:
    c = conn.cursor()
    c.execute("INSERT INTO Wish_list (client_id, device_id) VALUES (?,?)",
              (client_id, device_id,))
    conn.commit()
    return True


def insert_cart_list_item(conn, client_id, device_id) -> bool:
    c = conn.cursor()
    c.execute("INSERT INTO Cart_list (client_id, device_id) VALUES (?,?)",
              (client_id, device_id))
    conn.commit()
    return True


def insert_reservation(conn, client_id, device_id, status_id) -> bool:
    c = conn.cursor()
    c.execute("INSERT INTO Reservation (client_id, device_id, status_id) VALUES (?,?,?)",
              (client_id, device_id, status_id,))
    conn.commit()
    return True


def set_reservation_status(conn, reservation_id, status_id):
    c = conn.cursor()
    c.execute("UPDATE Reservation SET status_id = ? WHERE id = ?",
              (status_id, reservation_id,))
    conn.commit()
    return True


def insert_worker(conn, worker_name, worker_login, worker_password, worker_phone, role_id):
    c = conn.cursor()
    c.execute("INSERT INTO Worker (worker_name, worker_login, worker_password, worker_phone, role_id) "
              "VALUES (?,?,?,?,?)",
              (worker_name, worker_login, worker_password, worker_phone, role_id,))
    conn.commit()


def set_reservation_worker(conn, reservation_id, worker_id):
    c = conn.cursor()
    c.execute("UPDATE Reservation SET worker_id = ? WHERE id = ?",
              (worker_id, reservation_id,))
    conn.commit()
    return True


def select_remainder(conn, device_id):
    c = conn.cursor()
    c.execute("SELECT remainder FROM Device WHERE device_id = ?", (device_id,))
    remainder = c.fetchall()
    return remainder[0]


def set_device_remainder(conn, remainder, device_id):
    c = conn.cursor()
    c.execute("UPDATE Device SET remainder = ? WHERE id = ?",
              (remainder, device_id,))
    conn.commit()
    return True


def delete_device(conn, device_id) -> bool:
    c = conn.cursor()
    c.execute("DELETE FROM Device WHERE id = ?",
              (device_id,))
    conn.commit()
    return True


def delete_wish_list_item(conn, client_id, device_id) -> bool:
    c = conn.cursor()
    c.execute("DELETE FROM Wish_list WHERE client_id = ? AND device_id = ?",
              (client_id, device_id,))
    conn.commit()
    return True


def delete_cart_list_item(conn, client_id, device_id) -> bool:
    c = conn.cursor()
    c.execute("DELETE FROM Cart_list WHERE client_id = ? AND device_id = ?",
              (client_id, device_id,))
    conn.commit()
    return True


def delete_reservation(conn, reservation_id):
    c = conn.cursor()
    c.execute("DELETE FROM Reservation WHERE id = ?",
              (reservation_id,))
    conn.commit()
    return True


def create_tables(conn):
    create_table_country(conn)
    create_table_company(conn)
    create_table_device_type(conn)
    create_table_device(conn)
    create_table_client(conn)
    create_table_wish_list(conn)
    create_table_worker_role(conn)
    create_table_worker(conn)
    create_table_reservation_status(conn)
    create_table_reservation(conn)
    create_table_cart_list(conn)


def create_table_country(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Country ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "country_name TEXT"
              ")")


def create_table_company(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Company ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "company_name TEXT, "
              "country_id INTEGER"
              ")")


def create_table_device_type(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Device_type ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "device_type_name TEXT"
              ")")


def create_table_device(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Device ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "device_name TEXT, "
              "device_type_id INTEGER, "
              "company_id INTEGER"
              ")")


def create_table_client(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Client ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_name TEXT, "
              "client_login TEXT, "
              "client_password TEXT, "
              "client_phone TEXT"
              ")")


def create_table_reservation_status(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Reservation_status ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "status_name TEXT"
              ")")


def create_table_worker_role(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Worker_role ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "role_name TEXT"
              ")")


def create_table_worker(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Worker ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "worker_name TEXT, "
              "worker_login TEXT, "
              "worker_password TEXT, "
              "worker_phone TEXT, "
              "role_id INTEGER"
              ")")


def create_table_wish_list(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Wish_list ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_id INTEGER, "
              "device_id INTEGER"
              ")")


def create_table_reservation(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Reservation ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_id INTEGER, "
              "device_id INTEGER, "
              "status_id INTEGER, "
              "worker_id INTEGER"
              ")")


def create_table_cart_list(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Cart_list ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_id INTEGER, "
              "device_id INTEGER"
              ")")


# devices_collection.insert_many([
#    {
#       "_id": 0,
#       "model": "iPhone 14",
#       "screenSize": "6.1 inches",
#       "screenResolution": "2532 x 1170 pixels",
#       "screenType": "Super Retina XDR OLED",
#       "dimensions": {"length": 146.7, "width": 71.5, "thickness": 7.65},
#       "weight": "162 g",
#       "processor": "A16 Bionic",
#       "ram": "6 GB",
#       "rom": "128 GB / 256 GB / 512 GB",
#       "camera": {"rear": [{"resolution": "12 MP", "zoom": "2x optical zoom"}, {"resolution": "12 MP"}], "front": {"resolution": "12 MP"}},
#       "battery": {"capacity": "3100 mAh", "talkTime": "up to 22 hours", "internetUse": "up to 13 hours"},
#       "operatingSystem": "iOS 16",
#       "features": ["Face ID", "Wireless charging", "Water and dust resistance (IP68)", "Siri"]
#    },
#    {
#       "_id": 1,
#       "model": "iPhone 14 Pro",
#       "screenSize": "6.1 inches",
#       "screenResolution": "2532 x 1170 pixels",
#       "screenType": "Super Retina XDR OLED",
#       "dimensions": {"length": 146.7, "width": 71.5, "thickness": 7.65},
#       "weight": "187 g",
#       "processor": "A16 Bionic",
#       "ram": "8 GB",
#       "rom": "256 GB / 512 GB / 1 TB",
#       "camera": {"rear": [{"resolution": "12 MP", "zoom": "3x optical zoom"}, {"resolution": "12 MP"}, {"resolution": "12 MP", "LiDAR": True}], "front": {"resolution": "12 MP"}},
#       "battery": {"capacity": "3500 mAh", "talkTime": "up to 23 hours", "internetUse": "up to 15 hours"},
#       "operatingSystem": "iOS 16",
#       "features": ["Face ID", "Wireless charging", "Water and dust resistance (IP68)", "Siri", "LiDAR scanner", "5G capable"]
#    }
# ])

# devices_collection.insert_many([
#    {
#       "_id": 2,
#       "model": "Samsung Galaxy S23",
#       "screenSize": "6.5 inches",
#       "screenResolution": "3200 x 1440 pixels",
#       "screenType": "Dynamic AMOLED 2X",
#       "dimensions": {"length": 164.3, "width": 75.8, "thickness": 8.9},
#       "weight": "202 g",
#       "processor": "Exynos 2200",
#       "ram": "8 GB",
#       "rom": "128 GB / 256 GB / 512 GB",
#       "camera": {"rear": [{"resolution": "108 MP", "zoom": "3x optical zoom"}, {"resolution": "12 MP"}, {"resolution": "12 MP", "ultraWide": True}], "front": {"resolution": "20 MP"}},
#       "battery": {"capacity": "4500 mAh", "talkTime": "up to 24 hours", "internetUse": "up to 15 hours"},
#       "operatingSystem": "Android 13",
#       "features": ["Fingerprint sensor", "Wireless charging", "Water and dust resistance (IP68)", "Bixby"]
#    },
#    {
#       "_id": 3,
#       "model": "Samsung Galaxy S23 Ultra",
#       "screenSize": "6.8 inches",
#       "screenResolution": "3200 x 1440 pixels",
#       "screenType": "Dynamic AMOLED 2X",
#       "dimensions": {"length": 165.2, "width": 77.1, "thickness": 8.9},
#       "weight": "228 g",
#       "processor": "Exynos 2200",
#       "ram": "12 GB",
#       "rom": "256 GB / 512 GB / 1 TB",
#       "camera": {"rear": [{"resolution": "108 MP", "zoom": "10x optical zoom"}, {"resolution": "12 MP"}, {"resolution": "12 MP", "ultraWide": True}, {"resolution": "64 MP", "telephoto": True}], "front": {"resolution": "40 MP"}},
#       "battery": {"capacity": "5000 mAh", "talkTime": "up to 25 hours", "internetUse": "up to 17 hours"},
#       "operatingSystem": "Android 13",
#       "features": ["Fingerprint sensor", "Wireless charging", "Water and dust resistance (IP68)", "Bixby", "S Pen support", "5G capable"]
#    }
# ])

# devices_collection.insertMany([
#    {
#       "_id": 4,
#       "model": "Apple iPad",
#       "screenSize": "10.2 inches",
#       "screenResolution": "2160 x 1620 pixels",
#       "screenType": "Retina display",
#       "dimensions": {"length": 250.6, "width": 174.1, "thickness": 7.5},
#       "weight": "487 g",
#       "processor": "A13 Bionic",
#       "ram": "3 GB",
#       "rom": "64 GB / 256 GB",
#       "camera": {"rear": {"resolution": "8 MP"}, "front": {"resolution": "12 MP"}},
#       "battery": {"capacity": "32.4 Wh", "talkTime": "up to 10 hours", "internetUse": "up to 9 hours"},
#       "operatingSystem": "iPadOS 15",
#       "features": ["Touch ID", "Apple Pencil (1st generation) support", "Smart Keyboard support"]
#    },
#    {
#       "_id": 5,
#       "model": "Apple iPad Pro",
#       "screenSize": "11 inches",
#       "screenResolution": "2388 x 1668 pixels",
#       "screenType": "Liquid Retina XDR display",
#       "dimensions": {"length": 247.6, "width": 178.5, "thickness": 5.9},
#       "weight": "468 g",
#       "processor": "M1",
#       "ram": "8 GB / 16 GB",
#       "rom": "128 GB / 256 GB / 512 GB / 1 TB / 2 TB",
#       "camera": {"rear": [{"resolution": "12 MP", "wide": True}, {"resolution": "10 MP", "ultraWide": True}], "front": {"resolution": "12 MP"}},
#       "battery": {"capacity": "40.9 Wh", "talkTime": "up to 10 hours", "internetUse": "up to 9 hours"},
#       "operatingSystem": "iPadOS 15",
#       "features": ["Face ID", "Apple Pencil (2nd generation) support", "Smart Keyboard Folio support", "5G capable"]
#    }
# ])

# devices_collection.insert_many([
#     {
#       "_id": 6,
#       "model": "Galaxy Tab S8 5G",
#       "screenSize": "11 inches",
#       "screenResolution": "2560 x 1600 pixels",
#       "screenType": "Super AMOLED",
#       "dimensions": {"length": 253.8, "width": 165.3, "thickness": 6.3},
#       "weight": "502 g",      "processor": "Qualcomm Snapdragon 888",
#       "ram": "8 GB / 12 GB",      "rom": "128 GB / 256 GB / 512 GB",
#       "camera": {"rear": {"resolution": "13 MP"}, "front": {"resolution": "8 MP"}},
#       "battery": {"capacity": "8000 mAh", "talkTime": "up to 15 hours", "internetUse": "up to 10 hours"},
#       "operatingSystem": "Android 12",
#       "features": ["S Pen support", "5G capable", "Quad speakers"]
#    },
#    {
#       "_id": 7,
#       "model": "Galaxy Tab S8 Ultra 5G",
#       "screenSize": "12.4 inches",
#       "screenResolution": "2800 x 1752 pixels",
#       "screenType": "Super AMOLED",
#       "dimensions": {"length": 285, "width": 185, "thickness": 6.4},
#       "weight": "575 g",
#       "processor": "Qualcomm Snapdragon 888",
#       "ram": "8 GB / 12 GB",
#       "rom": "128 GB / 256 GB / 512 GB",
#       "camera": {"rear": {"resolution": "13 MP"}, "front": {"resolution": "8 MP"}},
#       "battery": {"capacity": "11000 mAh", "talkTime": "up to 14 hours", "internetUse": "up to 10 hours"},
#       "operatingSystem": "Android 12",
#       "features": ["S Pen support", "5G capable", "Quad speakers", "Under-display camera"]
#    }
# ])

# devices_collection.insert_many([
#     {
#         "_id": 8,
#         "model": "MacBook Air",
#         "screenSize": "13.3 inches",
#         "screenResolution": "2560 x 1600 pixels",
#         "screenType": "Retina display",
#         "dimensions": {"length": 304.1, "width": 212.4, "thickness": 16.1},
#         "weight": "1.29 kg",
#         "processor": "Apple M1 chip",
#         "ram": "8 GB / 16 GB",
#         "rom": "256 GB / 512 GB / 1 TB / 2 TB",
#         "graphics": "Apple M1 chip",
#         "battery": {"capacity": "Up to 17 hours", "videoPlayback": "Up to 15 hours"},
#         "operatingSystem": "macOS Monterey",
#         "features": ["Touch ID", "Thunderbolt 3 ports", "FaceTime HD camera", "Backlit Magic Keyboard"]
#    },
#    {
#       "_id": 9,
#       "model": "MacBook Pro",
#       "screenSize": "14.2 inches",
#       "screenResolution": "3024 x 1964 pixels",
#       "screenType": "Retina display with True Tone",
#       "dimensions": {"length": 307.6, "width": 212.4, "thickness": 15.5},
#       "weight": "1.83 kg",
#       "processor": "Apple M1 Pro or M1 Max chip",
#       "ram": "16 GB / 32 GB / 64 GB / 128 GB",
#       "rom": "512 GB / 1 TB / 2 TB / 4 TB",
#       "graphics": "Apple M1 Pro or M1 Max chip",
#       "battery": {"capacity": "Up to 11 hours", "videoPlayback": "Up to 17 hours"},
#       "operatingSystem": "macOS Monterey",
#       "features": ["Touch Bar", "Touch ID", "Thunderbolt 4 ports", "FaceTime HD camera", "Backlit Magic Keyboard"]
#    }
# ])

# devices_collection.insert_many([
#     {
#         "_id": 10,
#         "model": "Pixel 7",
#         "screenSize": "6.2 inches",
#         "screenResolution": "2340 x 1080 pixels",
#         "screenType": "OLED",
#         "dimensions": {"length": 151.9, "width": 71.4, "thickness": 7.9},
#         "weight": "168 g",      "processor": "Qualcomm Snapdragon 780G",
#         "ram": "8 GB",
#         "rom": "128 GB / 256 GB",
#         "battery": {"capacity": "4,600 mAh", "charging": "Fast charging up to 50% in 30 min", "wirelessCharging": "Yes"},
#         "operatingSystem": "Android 13",
#         "features": ["5G", "IP68 water and dust resistant", "Dual rear cameras", "Stereo speakers"]
#    },
#    {
#         "_id": 11,
#         "model": "Pixel 7 Pro",
#         "screenSize": "6.7 inches",
#         "screenResolution": "3120 x 1440 pixels",
#         "screenType": "OLED with LTPO",
#         "dimensions": {"length": 163.9, "width": 75.8, "thickness": 7.9},
#         "weight": "210 g",
#         "processor": "Qualcomm Snapdragon 888",
#         "ram": "8 GB / 12 GB",
#         "rom": "128 GB / 256 GB / 512 GB",
#         "battery": {"capacity": "5,000 mAh", "charging": "Fast charging up to 50% in 30 min", "wirelessCharging": "Yes"},
#         "operatingSystem": "Android 13",
#         "features": ["5G", "IP68 water and dust resistant", "Triple rear cameras with telephoto lens", "Stereo speakers", "Fingerprint sensor under the display"]
#    }
# ])

# devices_collection.insert_one({
#    "_id": 12,
#    "model": "PixelBook Go",
#    "screenSize": "13.3 inches",
#    "screenResolution": "1920 x 1080 pixels",
#    "screenType": "Full HD Touchscreen display",
#    "dimensions": {"length": 311.0, "width": 206.0, "thickness": 13.4},
#    "weight": "2.3 lbs",
#    "processor": "Intel Core m3, i5 or i7",
#    "ram": "8 GB / 16 GB",
#    "rom": "64 GB / 128 GB / 256 GB / 512 GB",
#    "battery": {"capacity": "47 Wh", "usageTime": "Up to 12 hours", "fastCharging": "2 hours of use in 20 minutes of charging"},
#    "operatingSystem": "Chrome OS",
#    "features": ["Backlit keyboard", "Titan C security chip", "Two USB-C ports", "Webcam", "Stereo speakers", "Google Assistant built-in"]
# })
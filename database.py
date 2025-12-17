import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# USERS
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

# PRODUCTS
cur.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    short_description TEXT,
    full_description TEXT,
    price REAL,
    image TEXT,
    owner_id INTEGER
)
""")

# COMMENTS
cur.execute("""
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    user_id INTEGER,
    content TEXT
)
""")

# USERS DATA
cur.execute("""
INSERT INTO users (username, password, role) VALUES
('admin', 'admin67!', 'admin'),
('meruyert', 'memo123', 'user'),
('malika', 'memo123', 'user')
""")

# PRODUCTS DATA
cur.execute("""
INSERT INTO products (name, short_description, full_description, price, image, owner_id) VALUES
('Denim Jacket', 'Vintage denim jacket', 'Stylish denim jacket with a timeless vintage design.', 69.99, 'jacket.jpg', 1),
('Cargo Pants', 'Relaxed fit cargo pants', 'Modern cargo pants with multiple pockets and relaxed fit.', 59.99, 'pants.jpg', 2),
('Knit Sweater', 'Warm knit sweater', 'Cozy knit sweater perfect for cold seasons.', 44.99, 'sweater.jpeg', 1),
('Summer Dress', 'Lightweight summer dress', 'Light and breathable dress designed for warm weather.', 39.99, 'dress.jpg', 3),
('Baseball Cap', 'Minimal logo cap', 'Casual baseball cap with minimal branding.', 14.99, 'cap.jpg', 2),
('Sneakers', 'Everyday sneakers', 'Comfortable sneakers designed for everyday walking.', 79.99, 'sneakers.jpg', 3)
""")

conn.commit()
conn.close()

print("✅ Database with roles initialized successfully")

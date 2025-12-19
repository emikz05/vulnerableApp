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
('admin2', '123admin2', 'admin'),
('meruyert', 'memo123', 'user'),
('malika', 'memo123', 'user')
""")

# PRODUCTS DATA
cur.execute("""
INSERT INTO products (name, short_description, full_description, price, image, owner_id) VALUES
('Denim Jacket', 'Vintage denim jacket', 'This vintage-inspired denim jacket is crafted from high-quality cotton denim for long-lasting durability.
It features a classic fit, reinforced stitching, and a timeless design that never goes out of style.
Perfect for layering over t-shirts or sweaters, this jacket is suitable for everyday wear in any season.', 69.99, 'jacket.jpg', 1),
('Cargo Pants', 'Relaxed fit cargo pants', 'These cargo pants combine comfort and functionality with a modern urban look.
Designed with multiple spacious pockets, a relaxed fit, and durable fabric, they are ideal for daily wear,
travel, and casual activities. A versatile piece for anyone who values both style and practicality.', 59.99, 'pants.jpg', 2),
('Knit Sweater', 'Warm knit sweater', 'This knit sweater is made from soft, warm materials to provide maximum comfort during colder seasons.
Its minimalist design and relaxed fit make it easy to pair with jeans, skirts, or layered outfits.
A perfect choice for cozy everyday wear.', 44.99, 'sweater.jpeg', 1),
('Summer Dress', 'Lightweight summer dress', 'This lightweight summer dress is designed for warm weather and effortless style.
Made from breathable fabric, it offers a comfortable fit while maintaining a flattering silhouette.
Ideal for casual outings, vacations, or relaxed summer days.', 39.99, 'dress.jpg', 1),
('Baseball Cap', 'Minimal logo cap', 'A casual baseball cap with a clean, minimal design suitable for everyday use.
Made from durable materials, it provides comfort and sun protection while complementing a wide range of outfits.
A simple accessory that adds a sporty touch to any look.', 14.99, 'cap.jpg', 2),
('Sneakers', 'Everyday sneakers', 'These everyday sneakers are designed for comfort, durability, and modern style.
Featuring cushioned insoles and breathable materials, they are perfect for walking and daily activities.
A versatile footwear option that pairs well with casual and sporty outfits.', 79.99, 'sneakers.jpg', 2)
""")

conn.commit()
conn.close()

print("✅ Database with roles initialized successfully")

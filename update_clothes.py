import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Denim Jacket
cur.execute("""
UPDATE products
SET full_description = 
'This vintage-inspired denim jacket is crafted from high-quality cotton denim for long-lasting durability.
It features a classic fit, reinforced stitching, and a timeless design that never goes out of style.
Perfect for layering over t-shirts or sweaters, this jacket is suitable for everyday wear in any season.'
WHERE name = 'Denim Jacket'
""")

# Cargo Pants
cur.execute("""
UPDATE products
SET full_description = 
'These cargo pants combine comfort and functionality with a modern urban look.
Designed with multiple spacious pockets, a relaxed fit, and durable fabric, they are ideal for daily wear,
travel, and casual activities. A versatile piece for anyone who values both style and practicality.'
WHERE name = 'Cargo Pants'
""")

# Knit Sweater
cur.execute("""
UPDATE products
SET full_description = 
'This knit sweater is made from soft, warm materials to provide maximum comfort during colder seasons.
Its minimalist design and relaxed fit make it easy to pair with jeans, skirts, or layered outfits.
A perfect choice for cozy everyday wear.'
WHERE name = 'Knit Sweater'
""")

# Summer Dress
cur.execute("""
UPDATE products
SET full_description = 
'This lightweight summer dress is designed for warm weather and effortless style.
Made from breathable fabric, it offers a comfortable fit while maintaining a flattering silhouette.
Ideal for casual outings, vacations, or relaxed summer days.'
WHERE name = 'Summer Dress'
""")

# Baseball Cap
cur.execute("""
UPDATE products
SET full_description = 
'A casual baseball cap with a clean, minimal design suitable for everyday use.
Made from durable materials, it provides comfort and sun protection while complementing a wide range of outfits.
A simple accessory that adds a sporty touch to any look.'
WHERE name = 'Baseball Cap'
""")

# Sneakers
cur.execute("""
UPDATE products
SET full_description = 
'These everyday sneakers are designed for comfort, durability, and modern style.
Featuring cushioned insoles and breathable materials, they are perfect for walking and daily activities.
A versatile footwear option that pairs well with casual and sporty outfits.'
WHERE name = 'Sneakers'
""")

conn.commit()
conn.close()

print("✅ Detailed product descriptions updated successfully")

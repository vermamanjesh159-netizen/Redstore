import os
import sys
from sqlalchemy import text

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app5.database import engine, Base, get_db_session
from app5.models import Register, test1
from myadmin.models import products
from user.models import Payment

def seed():
    # 1. Create/Drop tables
    print("Dropping old products and category tables in PostgreSQL...")
    session = get_db_session()
    try:
        session.execute(text("DROP TABLE IF EXISTS myadmin_products CASCADE;"))
        session.execute(text("DROP TABLE IF EXISTS myadmin_subcategroy CASCADE;"))
        session.execute(text("DROP TABLE IF EXISTS myadmin_categroy CASCADE;"))
        session.commit()
    except Exception as e:
        print("Error dropping tables:", e)
        session.rollback()

    print("Creating tables in PostgreSQL...")
    Base.metadata.create_all(engine)
    
    # 2. Seed app5_register
    if session.query(Register).count() == 0:
        print("Seeding app5_register...")
        registers = [
            Register(regid=4, name='pooja', email='pooja300@gmail.com', password='456789', mobile='9175342236', address='vijay nagar', city='Bhopal', gender='Female', status=1, roll='admin', info='<built-in function asctime>'),
            Register(regid=16, name='Manjesh Verma', email='manjeshverma124@gmail.com', password='12345678', mobile='9874563210', address='Dewas Naka Indore', city='Indore', gender='Male', status=1, roll='user', info='Fri Dec 16 20:29:34 2022'),
            Register(regid=20, name='Ashish dost', email='ashishpiplande3669@gmail.com', password='1753142236', mobile='9314567836', address='Robot Square', city='Indore', gender='Male', status=1, roll='user', info='Fri Dec 23 12:21:21 2022'),
            Register(regid=21, name='kr', email='admin@gmail.com', password='123456', mobile='555555', address='ffgfggfg', city='Indore', gender='Male', status=0, roll='user', info='Sun Apr  9 15:23:29 2023'),
        ]
        session.add_all(registers)
        session.commit()
        # Reset sequence
        session.execute(text("SELECT setval(pg_get_serial_sequence('app5_register', 'regid'), coalesce(max(regid), 1)) FROM app5_register;"))
        session.commit()

    # 3. Seed myadmin_products
    if session.query(products).count() == 0:
        print("Seeding myadmin_products...")
        prods = [
            products(prodid=1, title='Product for Pants', subcatname='Pants', description='Cotton Pants', ldate='2022-12-20', edate='2022-12-25', info='Fri Dec 23 22:54:53 2022', prodimage='product-9.jpg', price=25.00, quantity=50),
            products(prodid=2, title='Product for Shirt', subcatname='Shirt', description='Full Fabric Shirt', ldate='2022-12-07', edate='2022-12-10', info='Sat Dec 24 08:07:49 2022', prodimage='product-4.jpg', price=18.00, quantity=35),
            products(prodid=3, title='Seed Product', subcatname='General', description='Seed1', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-1.jpg', price=0.15, quantity=10),
            products(prodid=4, title='Premium Gym Bag', subcatname='General', description='Heavy duty sports duffle bag with wet compartment', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-1.jpg', price=29.99, quantity=100),
            products(prodid=5, title='Running Sneakers', subcatname='General', description='Lightweight breathable road running sneakers', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-2.jpg', price=89.99, quantity=75),
            products(prodid=6, title='Athletic Socks', subcatname='General', description='Cushioned cotton training socks (3 pack)', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-3.jpg', price=9.99, quantity=200),
            products(prodid=7, title='Dry-Fit Training Tee', subcatname='General', description='Sweat-wicking athletic fit training shirt', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-4.jpg', price=24.99, quantity=120),
            products(prodid=8, title='Casual Sneaker Shoes', subcatname='General', description='Stylish low-top canvas sneakers for everyday wear', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-5.jpg', price=65.00, quantity=60),
            products(prodid=9, title='Sport Watch', subcatname='General', description='Waterproof digital sport watch with stopwatch', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-6.jpg', price=120.00, quantity=45),
            products(prodid=10, title='Cotton Crew Socks Pack', subcatname='General', description='Soft combed cotton crew length socks', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-7.jpg', price=12.50, quantity=150),
            products(prodid=11, title='Leather Chronograph Watch', subcatname='General', description='Premium analog watch with genuine leather strap', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-8.jpg', price=150.00, quantity=30),
            products(prodid=12, title='Performance Track Pants', subcatname='General', description='Tapered fit training track pants with zipper pockets', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-9.jpg', price=45.00, quantity=80),
            products(prodid=13, title='Road Running Shoes', subcatname='General', description='High responsiveness running shoes with gel sole', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-10.jpg', price=95.00, quantity=55),
            products(prodid=14, title='Aerodynamic Running Shoes', subcatname='General', description='Marathon class lightweight running footwear', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-11.jpg', price=110.00, quantity=40),
            products(prodid=15, title='Gym Sweatpants', subcatname='General', description='Comfortable fleece sweatpants for workouts', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-12.jpg', price=35.00, quantity=90),
            products(prodid=16, title='Sports Backpack', subcatname='General', description='Durable everyday backpack with laptop sleeve', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-1.jpg', price=39.99, quantity=110),
            products(prodid=17, title='Comfort Training Shoes', subcatname='General', description='All-day wear cushioning training shoes', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-2.jpg', price=79.99, quantity=65),
            products(prodid=18, title='Ankle Socks (3 Pairs)', subcatname='General', description='Low-profile breathable training ankle socks', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-3.jpg', price=7.99, quantity=250),
            products(prodid=19, title='Slim Fit Sport Polo', subcatname='General', description='Classic fit performance polo shirt', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-4.jpg', price=28.00, quantity=85),
            products(prodid=20, title='Urban Walking Shoes', subcatname='General', description='Memory foam sole urban lifestyle shoes', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-5.jpg', price=59.99, quantity=70),
            products(prodid=21, title='Digital Fitness Tracker', subcatname='General', description='OLED fitness tracker with heart rate monitor', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-6.jpg', price=49.99, quantity=120),
            products(prodid=22, title='Thermal Cushion Socks', subcatname='General', description='Thick thermal socks for cold weather sports', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-7.jpg', price=14.99, quantity=100),
            products(prodid=23, title='Waterproof Smart Watch', subcatname='General', description='Smart watch with touch screen and GPS tracking', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-8.jpg', price=199.99, quantity=25),
            products(prodid=24, title='Elastic Jogger Pants', subcatname='General', description='Flex-weave elastic waist jogger sweatpants', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-9.jpg', price=38.00, quantity=110),
            products(prodid=25, title='Trail Running Shoes', subcatname='General', description='Rugged outsole trail running shoes with grip', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-10.jpg', price=105.00, quantity=50),
            products(prodid=26, title='Ultra Light Trainers', subcatname='General', description='Featherweight cross-training gym shoes', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-11.jpg', price=115.00, quantity=45),
            products(prodid=27, title='Fleece Sports Hoodie', subcatname='General', description='Warm insulating fleece pull-over sports hoodie', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-12.jpg', price=42.50, quantity=80),
            products(prodid=28, title='Canvas Shoulder Bag', subcatname='General', description='Heavy duty canvas messenger and shoulder bag', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-1.jpg', price=19.99, quantity=140),
            products(prodid=29, title='Court Tennis Shoes', subcatname='General', description='Non-marking sole shoes for clay and hardcourt', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-2.jpg', price=84.99, quantity=60),
            products(prodid=30, title='Compression Sports Socks', subcatname='General', description='High performance compression socks for recovery', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-3.jpg', price=15.99, quantity=180),
            products(prodid=31, title='Moisture Wicking T-Shirt', subcatname='General', description='Lightweight crewneck tee with flatlock seams', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-4.jpg', price=22.00, quantity=130),
            products(prodid=32, title='Classic Leather Loafers', subcatname='General', description='Elegant slip-on leather footwear for smart casual', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-5.jpg', price=74.99, quantity=40),
            products(prodid=33, title='Smart Sports Chrono', subcatname='General', description='Rugged digital watch with hybrid step counter', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-6.jpg', price=135.00, quantity=35),
            products(prodid=34, title='Wool Blend Hiking Socks', subcatname='General', description='Merino wool blend thick trail socks', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-7.jpg', price=18.00, quantity=90),
            products(prodid=35, title="Men's Luxury Watch", subcatname='General', description='Luxury automatic watch with steel bracelet', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-8.jpg', price=250.00, quantity=15),
            products(prodid=36, title='Loose Fit Gym Shorts', subcatname='General', description='Lightweight polyester training gym shorts', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-9.jpg', price=20.00, quantity=160),
            products(prodid=37, title='Stability Jogging Shoes', subcatname='General', description='Arch support stability road runner shoes', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-10.jpg', price=90.00, quantity=70),
            products(prodid=38, title='Racing Flat Shoes', subcatname='General', description='Minimalist racing flat shoes for speedwork', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-11.jpg', price=125.00, quantity=30),
            products(prodid=39, title='Windbreaker Sport Jacket', subcatname='General', description='Water-resistant lightweight windbreaker jacket', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-12.jpg', price=55.00, quantity=65),
            products(prodid=40, title='Outdoor Duffle Bag', subcatname='General', description='Weatherproof canvas gym duffle with shoe pocket', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-1.jpg', price=45.00, quantity=75),
            products(prodid=41, title='Retro Lifestyle Sneakers', subcatname='General', description='Classic retro design suede lifestyle sneakers', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-2.jpg', price=69.99, quantity=85),
            products(prodid=42, title='No-Show Sports Liners', subcatname='General', description='No-show silicone grip breathable foot liners (5 pack)', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-3.jpg', price=8.50, quantity=300),
            products(prodid=43, title='Breathable Training Tank', subcatname='General', description='Sleeveless athletic tank top for hot training days', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-4.jpg', price=19.50, quantity=150),
            products(prodid=44, title='Lightweight Running Flats', subcatname='General', description='Flexible lightweight road racing flat footwear', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-5.jpg', price=72.00, quantity=55),
            products(prodid=45, title='Rugged Sport GPS Watch', subcatname='General', description='Tactical GPS tracking smartwatch with altimeter', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-6.jpg', price=179.99, quantity=30),
            products(prodid=46, title='Anti-Blister Running Socks', subcatname='General', description='Dry-yarn reinforced toe and heel running socks', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-7.jpg', price=11.99, quantity=220),
            products(prodid=47, title='Titanium Watch Edition', subcatname='General', description='Limited edition titanium finish automatic watch', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-8.jpg', price=299.99, quantity=10),
            products(prodid=48, title='Active Knit Sweatpants', subcatname='General', description='Structured knit joggers with slim tapered fit', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-9.jpg', price=32.99, quantity=95),
            products(prodid=49, title='All-Terrain Trail Sneakers', subcatname='General', description='Mud-grip rugged sole trail running shoes', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-10.jpg', price=110.00, quantity=45),
            products(prodid=50, title='Pro Cushion Runner Shoes', subcatname='General', description='Max cushion comfort running shoes for long distance', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-11.jpg', price=130.00, quantity=35),
            products(prodid=51, title='Full Zip Gym Fleece', subcatname='General', description='Athletic wear full-zip thermal performance fleece', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-12.jpg', price=48.00, quantity=70),
            products(prodid=52, title='Premium Gym Towel Set', subcatname='General', description='Super absorbent quick-dry microfiber gym towels', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-3.jpg', price=12.00, quantity=200),
            products(prodid=53, title='Ergonomic Sports Bottle', subcatname='General', description='BPA-free leakproof sports squeeze bottle 750ml', ldate='2026-06-01', edate='2026-06-30', info='Mon Jun  1 06:19:09 2026', prodimage='product-1.jpg', price=15.00, quantity=250),
        ]
        session.add_all(prods)
        session.commit()
        # Reset sequence
        session.execute(text("SELECT setval(pg_get_serial_sequence('myadmin_products', 'prodid'), coalesce(max(prodid), 1)) FROM myadmin_products;"))
        session.commit()

    # 4. Seed user_payment
    if session.query(Payment).count() == 0:
        print("Seeding user_payment...")
        payments = [
            Payment(txnid=1, uid='manjeshverma124@gmail.com', amt='100', info='Sat Dec 17 20:46:53 2022'),
            Payment(txnid=2, uid='manjeshverma124@gmail.com', amt='100', info='Tue Dec 20 15:57:24 2022'),
        ]
        session.add_all(payments)
        session.commit()
        # Reset sequence
        session.execute(text("SELECT setval(pg_get_serial_sequence('user_payment', 'txnid'), coalesce(max(txnid), 1)) FROM user_payment;"))
        session.commit()

    session.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed()

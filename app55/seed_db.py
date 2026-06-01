import os
import sys
import json
from sqlalchemy import text

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app5.database import engine, Base, get_db_session
from app5.models import Register
from myadmin.models import products as ProductModel
from user.models import Payment

def seed():
    # 1. Create tables if they do not exist
    print("Creating database tables if they do not exist...")
    Base.metadata.create_all(engine)
    
    session = get_db_session()
    
    # Load seed data from JSON
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app5', 'default_data.json')
    if not os.path.exists(json_path):
        print(f"Error: JSON data file not found at {json_path}")
        return
        
    try:
        with open(json_path, 'r') as f:
            default_data = json.load(f)
    except Exception as e:
        print("Error reading seed JSON data:", e)
        session.close()
        return

    # 2. Seed app5_register (default users/admins)
    if session.query(Register).count() == 0:
        print("Seeding app5_register...")
        registers = []
        for r_dict in default_data.get("registers", []):
            registers.append(Register(**r_dict))
        session.add_all(registers)
        session.commit()
        
        # Reset auto-increment sequence
        max_regid = max([r.regid for r in registers]) if registers else 1
        if "sqlite" in str(engine.url):
            try:
                session.execute(text("INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES ('app5_register', :seq)"), {"seq": max_regid})
                session.commit()
            except Exception as e:
                print("SQLite sequence reset skipped or failed for app5_register:", e)
        else:
            try:
                session.execute(text("SELECT setval(pg_get_serial_sequence('app5_register', 'regid'), coalesce(max(regid), 1)) FROM app5_register;"))
                session.commit()
            except Exception as e:
                print("PostgreSQL sequence reset failed for app5_register:", e)

    # 3. Seed myadmin_products (catalog items)
    # Only seed default products in local development (SQLite) or if SEED_PRODUCTS env var is explicitly set
    is_sqlite = "sqlite" in str(engine.url)
    seed_products_env = os.getenv("SEED_PRODUCTS", "false").lower() == "true"
    
    if is_sqlite or seed_products_env:
        if session.query(ProductModel).count() == 0:
            print("Seeding myadmin_products...")
            prods = []
            for p_dict in default_data.get("products", []):
                prods.append(ProductModel(**p_dict))
            session.add_all(prods)
            session.commit()
            
            # Reset sequence to start at 1000 to prevent collisions with default product IDs (1-53)
            max_prodid = max([p.prodid for p in prods]) if prods else 999
            if max_prodid < 999:
                max_prodid = 999
                
            if "sqlite" in str(engine.url):
                try:
                    session.execute(text("INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES ('myadmin_products', :seq)"), {"seq": max_prodid})
                    session.commit()
                except Exception as e:
                    print("SQLite sequence reset skipped or failed for myadmin_products:", e)
            else:
                try:
                    session.execute(text(f"ALTER SEQUENCE myadmin_products_prodid_seq RESTART WITH {max_prodid + 1};"))
                    session.commit()
                except Exception as e:
                    print("PostgreSQL sequence reset failed for myadmin_products:", e)
        else:
            print("myadmin_products table already has records. Skipping product seeding.")
    else:
        print("Skipping myadmin_products seeding in production (PostgreSQL) to preserve database rows.")

    # 4. Seed user_payment (default transaction history)
    if session.query(Payment).count() == 0:
        print("Seeding user_payment...")
        payments = []
        for p_dict in default_data.get("payments", []):
            payments.append(Payment(**p_dict))
        session.add_all(payments)
        session.commit()
        
        # Reset sequence
        max_txnid = max([p.txnid for p in payments]) if payments else 1
        if "sqlite" in str(engine.url):
            try:
                session.execute(text("INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES ('user_payment', :seq)"), {"seq": max_txnid})
                session.commit()
            except Exception as e:
                print("SQLite sequence reset skipped or failed for user_payment:", e)
        else:
            try:
                session.execute(text("SELECT setval(pg_get_serial_sequence('user_payment', 'txnid'), coalesce(max(txnid), 1)) FROM user_payment;"))
                session.commit()
            except Exception as e:
                print("PostgreSQL sequence reset failed for user_payment:", e)

    session.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed()

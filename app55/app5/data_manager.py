import os
import json
from django.conf import settings
from myadmin.models import products as ProductModel
from app5.database import get_db_session

class MockProduct:
    def __init__(self, **kwargs):
        self.prodid = kwargs.get('prodid')
        self.title = kwargs.get('title', '')
        self.subcatname = kwargs.get('subcatname', 'General')
        self.description = kwargs.get('description', '')
        self.ldate = kwargs.get('ldate', '')
        self.edate = kwargs.get('edate', '')
        self.info = kwargs.get('info', '')
        self.prodimage = kwargs.get('prodimage', '')
        self.price = float(kwargs.get('price', 0.0))
        self.quantity = int(kwargs.get('quantity', 0))

    def __repr__(self):
        return f"<MockProduct id={self.prodid} title='{self.title}'>"

_cached_defaults = None

def load_default_products():
    global _cached_defaults
    if _cached_defaults is not None:
        return _cached_defaults

    json_path = os.path.join(settings.BASE_DIR, 'app5', 'default_data.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                _cached_defaults = data.get('products', [])
        except Exception as e:
            print("Error loading default products from JSON:", e)
            _cached_defaults = []
    else:
        print("Default data JSON not found at:", json_path)
        _cached_defaults = []
        
    return _cached_defaults

def get_all_products(session=None):
    # 1. Load default products
    defaults = load_default_products()
    default_objs = [MockProduct(**p) for p in defaults]

    # 2. Get DB products
    db_close = False
    if session is None:
        session = get_db_session()
        db_close = True

    try:
        db_prods = session.query(ProductModel).all()
    except Exception as e:
        print("Error querying products from database:", e)
        db_prods = []
    finally:
        if db_close:
            session.close()

    # 3. Merge them. If a product ID exists in the database, prioritize the database record.
    db_prod_ids = {p.prodid for p in db_prods}
    merged_products = [p for p in default_objs if p.prodid not in db_prod_ids] + list(db_prods)
    return merged_products

def get_product_by_id(prodid, session=None):
    db_close = False
    if session is None:
        session = get_db_session()
        db_close = True

    try:
        db_prod = session.query(ProductModel).filter(ProductModel.prodid == prodid).first()
        if db_prod:
            return db_prod
    except Exception as e:
        print(f"Error querying product {prodid} from database:", e)
    finally:
        if db_close:
            session.close()

    # Fallback to defaults from JSON
    defaults = load_default_products()
    for p in defaults:
        if p.get('prodid') == prodid:
            return MockProduct(**p)
            
    return None

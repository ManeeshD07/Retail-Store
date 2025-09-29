#!/usr/bin/env python3
"""
Seed MongoDB with users, products, carts, orders, reviews.
Usage examples:
  # local (host Mongo on localhost:27017)
  python backend/scripts/seed_db.py --mongo-uri mongodb://localhost:27017 --db retail --users 1000 --products 5000

  # via docker compose (see README)
  docker compose run --rm api python backend/scripts/seed_db.py --mongo-uri mongodb://mongo:27017 --db retail --users 1000 --products 5000
"""
from __future__ import annotations
import argparse
import random
import datetime
import math
from typing import List
from faker import Faker
from pymongo import MongoClient, ASCENDING, TEXT
from bson import ObjectId
import bcrypt
import sys

fake = Faker()

def create_indexes(db):
    print("Creating indexes...")
    db.products.create_index([("name", TEXT), ("description", TEXT)])
    db.products.create_index([("categories", ASCENDING)])
    db.products.create_index([("price", ASCENDING)])
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.orders.create_index([("user_id", ASCENDING), ("created_at", -1)])
    db.carts.create_index([("user_id", ASCENDING)], unique=True)
    print("Indexes created.")

def gen_user():
    name = fake.name()
    email = fake.unique.email()
    pw = "Test1234!"  # default password for seeded users
    pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    user = {
        "name": name,
        "email": email,
        "password_hash": pw_hash,
        "role": "customer",
        "addresses": [
            {
                "label": "Home",
                "line1": fake.street_address(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "zip": fake.zipcode(),
                "country": "US"
            }
        ],
        "created_at": datetime.datetime.utcnow()
    }
    return user

def gen_product(i):
    brands = ["Acme","Nova","Zenwave","Orion","Atlas","Nimbus"]
    cats = ["Accessories","Laptops","Cables","Audio","Home","Office","Wearables"]
    price = round(random.uniform(5.0, 999.0), 2)
    stock = random.randint(0, 1000)
    p = {
        "sku": f"SKU-{i:06d}",
        "name": f"{fake.word().capitalize()} {fake.word().capitalize()}",
        "description": fake.sentence(nb_words=12),
        "categories": [random.choice(cats)],
        "brand": random.choice(brands),
        "price": price,
        "currency": "USD",
        "images": [],
        "stock": stock,
        "rating": round(random.uniform(3.0, 5.0), 1),
        "attributes": {"color": random.choice(["Black","White","Red","Blue","Green"]), "size": random.choice(["S","M","L","XL"])},
        "created_at": datetime.datetime.utcnow()
    }
    return p

def gen_cart(user_id, product_ids, max_items=6):
    items = []
    k = random.randint(1, min(max_items, len(product_ids)))
    sample = random.sample(product_ids, k)
    for pid in sample:
        qty = random.randint(1, 5)
        # price will be filled if needed by reading product price (we keep it simple)
        items.append({"product_id": pid, "qty": qty})
    cart = {
        "user_id": user_id,
        "items": items,
        "updated_at": datetime.datetime.utcnow()
    }
    return cart

def gen_order(user_id, product_ids):
    k = random.randint(1, min(6, len(product_ids)))
    sample = random.sample(product_ids, k)
    items = []
    subtotal = 0.0
    for pid in sample:
        qty = random.randint(1, 3)
        # In seeding we don't fetch product price for performance; server can aggregate prices later.
        price = round(random.uniform(5.0, 199.0), 2)
        subtotal += price * qty
        items.append({"product_id": pid, "qty": qty, "price": price})
    shipping = round(random.uniform(0, 12),2)
    tax = round(subtotal * 0.07, 2)
    total = round(subtotal + shipping + tax, 2)
    order = {
        "user_id": user_id,
        "items": items,
        "subtotal": round(subtotal,2),
        "shipping": shipping,
        "tax": tax,
        "total": total,
        "payment_status": random.choice(["paid","requires_payment","failed"]),
        "fulfillment_status": random.choice(["new","picking","shipped","delivered"]),
        "created_at": datetime.datetime.utcnow()
    }
    return order

def batch_insert(collection, docs, batch_size=1000):
    n = len(docs)
    if n == 0:
        return
    for i in range(0, n, batch_size):
        chunk = docs[i:i+batch_size]
        collection.insert_many(chunk)

def main(args):
    client = MongoClient(args.mongo_uri)
    db = client[args.db]
    if args.drop_first:
        print("Dropping existing collections (users, products, carts, orders, reviews)...")
        db.users.drop()
        db.products.drop()
        db.carts.drop()
        db.orders.drop()
        db.reviews.drop()

    create_indexes(db)

    # Users
    print(f"Seeding {args.users} users...")
    users = []
    for i in range(args.users):
        users.append(gen_user())
        if (i+1) % 5000 == 0:
            print(f"  prepared {i+1} users")
    batch_insert(db.users, users, batch_size=1000)
    print("Users inserted.")
    # Fetch inserted user ids
    user_docs = list(db.users.find({}, {"_id": 1}))
    user_ids = [u["_id"] for u in user_docs]
    if not user_ids:
        print("No users found after insert; exiting.")
        sys.exit(1)

    # Products
    print(f"Seeding {args.products} products...")
    products = []
    for i in range(1, args.products+1):
        products.append(gen_product(i))
        if i % 2000 == 0:
            print(f"  prepared {i} products")
    batch_insert(db.products, products, batch_size=2000)
    print("Products inserted.")
    product_docs = list(db.products.find({}, {"_id": 1}))
    product_ids = [p["_id"] for p in product_docs]

    # Carts (for a subset of users)
    carts_to_create = min(args.carts, len(user_ids))
    print(f"Seeding {carts_to_create} carts...")
    carts = []
    # choose random users for carts
    sample_user_ids = random.sample(user_ids, carts_to_create)
    for uid in sample_user_ids:
        carts.append(gen_cart(uid, product_ids, max_items=args.max_cart_items))
    batch_insert(db.carts, carts, batch_size=1000)
    print("Carts inserted.")

    # Orders
    orders_to_create = min(args.orders, len(user_ids))
    print(f"Seeding {orders_to_create} orders...")
    orders = []
    for _ in range(orders_to_create):
        uid = random.choice(user_ids)
        orders.append(gen_order(uid, product_ids))
    batch_insert(db.orders, orders, batch_size=1000)
    print("Orders inserted.")

    # Reviews (optional)
    reviews_to_create = min(args.reviews, args.products * 2)
    print(f"Seeding {reviews_to_create} reviews...")
    reviews = []
    for _ in range(reviews_to_create):
        pid = random.choice(product_ids)
        uid = random.choice(user_ids)
        reviews.append({
            "product_id": pid,
            "user_id": uid,
            "rating": random.randint(1,5),
            "title": fake.sentence(nb_words=3),
            "body": fake.paragraph(nb_sentences=2),
            "created_at": datetime.datetime.utcnow()
        })
    batch_insert(db.reviews, reviews, batch_size=1000)
    print("Reviews inserted.")

    print("Seeding complete.")
    print(f"Summary: users={len(user_ids)}, products={len(product_ids)}, carts={carts_to_create}, orders={orders_to_create}, reviews={reviews_to_create}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-uri", default="mongodb://localhost:27017", help="MongoDB URI")
    parser.add_argument("--db", default="retail", help="DB name")
    parser.add_argument("--users", type=int, default=1000, help="Number of users to create")
    parser.add_argument("--products", type=int, default=2000, help="Number of products to create")
    parser.add_argument("--carts", type=int, default=500, help="Number of carts to create")
    parser.add_argument("--orders", type=int, default=1000, help="Number of orders to create")
    parser.add_argument("--reviews", type=int, default=2000, help="Number of reviews to create")
    parser.add_argument("--drop-first", action="store_true", help="Drop collections before seeding")
    parser.add_argument("--max-cart-items", type=int, default=6, help="Max items per cart")
    args = parser.parse_args()
    main(args)

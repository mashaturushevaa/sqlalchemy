from app import app
from db import db
from models import StoreModel, ItemModel

with app.app_context():
    store = StoreModel(name="Магазин Тест")
    db.session.add(store)
    db.session.commit()

    item1 = ItemModel(name="Олівець", price=5.0, store_id=store.id)
    item2 = ItemModel(name="Зошит", price=15.0, store_id=store.id)

    db.session.add_all([item1, item2])
    db.session.commit()

    print("Товари та магазин додано!")

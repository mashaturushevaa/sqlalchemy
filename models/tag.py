from db import db

# Проміжна таблиця — item_tags
item_tags = db.Table(
    "item_tags",
    db.Column("item_id", db.Integer, db.ForeignKey("items.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    items = db.relationship("ItemModel", secondary=item_tags, back_populates="tags")

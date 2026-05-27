"""Create shop schema and seed data."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260527_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(length=30), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
    )

    op.bulk_insert(
        sa.table(
            "users",
            sa.column("id", sa.Integer()),
            sa.column("name", sa.String()),
            sa.column("email", sa.String()),
            sa.column("age", sa.Integer()),
        ),
        [
            {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "age": 25},
            {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "age": 31},
        ],
    )
    op.bulk_insert(
        sa.table(
            "profiles",
            sa.column("id", sa.Integer()),
            sa.column("user_id", sa.Integer()),
            sa.column("phone", sa.String()),
            sa.column("address", sa.String()),
        ),
        [
            {"id": 1, "user_id": 1, "phone": "+380501112233", "address": "Kyiv, Main Street 1"},
            {"id": 2, "user_id": 2, "phone": "+380671112233", "address": "Lviv, Market Square 2"},
        ],
    )
    op.bulk_insert(
        sa.table(
            "categories",
            sa.column("id", sa.Integer()),
            sa.column("name", sa.String()),
            sa.column("description", sa.String()),
        ),
        [
            {"id": 1, "name": "Laptops", "description": "Portable computers"},
            {"id": 2, "name": "Accessories", "description": "Useful computer accessories"},
        ],
    )
    op.bulk_insert(
        sa.table(
            "products",
            sa.column("id", sa.Integer()),
            sa.column("category_id", sa.Integer()),
            sa.column("name", sa.String()),
            sa.column("price", sa.Numeric()),
            sa.column("stock", sa.Integer()),
        ),
        [
            {"id": 1, "category_id": 1, "name": "ThinkPad E14", "price": 899.00, "stock": 7},
            {"id": 2, "category_id": 2, "name": "USB-C Hub", "price": 49.99, "stock": 25},
        ],
    )
    op.bulk_insert(
        sa.table(
            "orders",
            sa.column("id", sa.Integer()),
            sa.column("user_id", sa.Integer()),
            sa.column("status", sa.String()),
        ),
        [
            {"id": 1, "user_id": 1, "status": "paid"},
            {"id": 2, "user_id": 2, "status": "new"},
        ],
    )
    op.bulk_insert(
        sa.table(
            "order_items",
            sa.column("id", sa.Integer()),
            sa.column("order_id", sa.Integer()),
            sa.column("product_id", sa.Integer()),
            sa.column("quantity", sa.Integer()),
        ),
        [
            {"id": 1, "order_id": 1, "product_id": 1, "quantity": 1},
            {"id": 2, "order_id": 2, "product_id": 2, "quantity": 2},
        ],
    )


def downgrade() -> None:
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("products")
    op.drop_table("categories")
    op.drop_table("profiles")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

"""Add salted password hashes to users."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260527_0002"
down_revision: str | None = "20260527_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

DEMO_PASSWORD_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$kAOeOoS0bl7FTlXWO/NnAA$"
    "vK0BCfLdm34g/Uoj3tULYwbZXCzdAU6cg2bsIddDqII"
)


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "hashed_password",
            sa.String(length=255),
            nullable=False,
            server_default=DEMO_PASSWORD_HASH,
        ),
    )
    op.alter_column("users", "hashed_password", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "hashed_password")

"""Create toys table

Revision ID: 06797e8e892f
Revises: 21b72afee37a
Create Date: 2022-12-22 15:21:05.387517

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "06797e8e892f"
down_revision = "21b72afee37a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "toys",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id")),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    )
    op.execute(
        "ALTER TABLE toys ENABLE ROW LEVEL SECURITY;",
    )
    op.execute(
        "CREATE POLICY tenant_isolation on toys \
            USING (tenant_id = current_setting('app.current_tenant')::int);",
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tenant_isolation ON toys;")
    op.execute("ALTER TABLE toys DISABLE ROW LEVEL SECURITY;")
    op.drop_table("toys")

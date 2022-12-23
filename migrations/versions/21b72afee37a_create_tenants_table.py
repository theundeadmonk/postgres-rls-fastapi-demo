"""Create tenants table

Revision ID: 21b72afee37a
Revises: 
Create Date: 2022-12-22 14:48:24.853236

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "21b72afee37a"
down_revision = "4c39bdd8dd20"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    )
    op.execute(
        "ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;",
    )
    op.execute(
        "CREATE POLICY tenant_isolation on tenants \
            USING (id = current_setting('app.current_tenant')::int);",
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tenant_isolation ON tenants;")
    op.execute("ALTER TABLE tenants DISABLE ROW LEVEL SECURITY;")
    op.drop_table("tenants")

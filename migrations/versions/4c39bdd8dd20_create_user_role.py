"""Create user role

Revision ID: 4c39bdd8dd20
Revises: 21b72afee37a
Create Date: 2022-12-22 15:19:14.981570

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "4c39bdd8dd20"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
        IF NOT EXISTS(SELECT * FROM pg_roles WHERE rolname = 'tenant_user') THEN
            CREATE ROLE tenant_user;
            GRANT tenant_user TO admin;
            GRANT USAGE ON SCHEMA public TO tenant_user;
            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO tenant_user;
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO tenant_user;
            GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO tenant_user;
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO tenant_user;
        END IF;
        END
        $$
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
        IF NOT EXISTS(SELECT * FROM pg_roles WHERE rolname = 'tenant_user') THEN
            DROP ROLE tenant_user;
        END IF;
        END
        $$
    """
    )

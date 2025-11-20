"""enable_pgvector_extension

Revision ID: b2344c4cb16e
Revises: 001
Create Date: 2025-11-20 06:13:59.081826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2344c4cb16e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade():
    op.execute("DROP EXTENSION IF EXISTS vector")

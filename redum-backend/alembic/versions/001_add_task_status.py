"""add task status column

Revision ID: 001
Revises: 
Create Date: 2025-11-09

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum type for task status
    op.execute("CREATE TYPE taskstatus AS ENUM ('todo', 'in_progress', 'done')")
    
    # Add status column to tasks table with default value
    op.add_column('tasks', 
        sa.Column('status', sa.Enum('TODO', 'IN_PROGRESS', 'DONE', name='taskstatus'), 
                  nullable=False, server_default='todo')
    )


def downgrade() -> None:
    # Remove status column
    op.drop_column('tasks', 'status')
    
    # Drop enum type
    op.execute("DROP TYPE taskstatus")

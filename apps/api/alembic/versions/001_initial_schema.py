"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2026-02-11 15:53:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', UUID(as_uuid=False), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create tracks table
    op.create_table(
        'tracks',
        sa.Column('id', UUID(as_uuid=False), nullable=False),
        sa.Column('project_id', UUID(as_uuid=False), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('storage_path', sa.String(length=512), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('format', sa.String(length=10), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create jobs table
    op.create_table(
        'jobs',
        sa.Column('id', UUID(as_uuid=False), nullable=False),
        sa.Column('track_id', UUID(as_uuid=False), nullable=False),
        sa.Column('preset', sa.String(length=100), nullable=False),
        sa.Column('status', sa.Enum('queued', 'running', 'succeeded', 'failed', name='jobstatus', create_type=True), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('output_path', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['track_id'], ['tracks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign keys)
    op.drop_table('jobs')
    op.drop_table('tracks')
    op.drop_table('projects')

    # Drop enum type
    sa.Enum(name='jobstatus').drop(op.get_bind(), checkfirst=True)

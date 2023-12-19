"""Initial

Revision ID: 5d4f1b02f4a1
Revises: 
Create Date: 2023-12-19 00:01:51.449385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d4f1b02f4a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_class',
    sa.Column('payment_class_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('payment_class_id'),
    sa.UniqueConstraint('description')
    )
    op.create_table('test',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('record',
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.Column('unid', sa.Integer(), nullable=False),
    sa.Column('active', sa.Float(), nullable=False),
    sa.Column('passive', sa.Float(), nullable=False),
    sa.Column('debit', sa.Float(), nullable=False),
    sa.Column('credit', sa.Float(), nullable=False),
    sa.Column('payment_class_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['payment_class_id'], ['payment_class.payment_class_id'], ),
    sa.PrimaryKeyConstraint('record_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('record')
    op.drop_table('test')
    op.drop_table('payment_class')
    # ### end Alembic commands ###

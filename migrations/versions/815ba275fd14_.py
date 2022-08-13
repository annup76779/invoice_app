"""empty message

Revision ID: 815ba275fd14
Revises: 
Create Date: 2022-08-13 06:14:42.839675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '815ba275fd14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('admin_key', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_table('invoice',
    sa.Column('number', sa.String(length=74), nullable=False),
    sa.Column('password', sa.String(length=90), nullable=False),
    sa.Column('email', sa.String(length=220), nullable=True),
    sa.Column('route_plan', sa.String(length=220), nullable=True),
    sa.Column('customer_name', sa.String(length=225), nullable=True),
    sa.Column('invoice_date', sa.Date(), nullable=True),
    sa.Column('invoice_no', sa.String(length=50), nullable=False),
    sa.Column('invoice_amount', sa.String(length=120), nullable=True),
    sa.Column('paid_amount', sa.String(length=120), nullable=True),
    sa.Column('balance_amount', sa.String(length=120), nullable=True),
    sa.Column('pending_since', sa.String(length=120), nullable=True),
    sa.Column('cash', sa.String(length=120), nullable=True),
    sa.Column('cheque_amount', sa.String(length=125), nullable=True),
    sa.Column('bank_name', sa.String(length=256), nullable=True),
    sa.Column('cheque_number', sa.String(length=135), nullable=True),
    sa.Column('cheque_date', sa.String(length=115), nullable=True),
    sa.Column('neft_amount', sa.String(length=30), nullable=True),
    sa.Column('utrn_number', sa.String(length=135), nullable=True),
    sa.Column('neft_date', sa.String(length=115), nullable=True),
    sa.Column('common_cheque', sa.String(length=110), nullable=True),
    sa.Column('no_collection', sa.String(length=110), nullable=True),
    sa.Column('reason', sa.UnicodeText(), nullable=True),
    sa.Column('note_2000', sa.String(length=118), nullable=True),
    sa.Column('note_500', sa.String(length=118), nullable=True),
    sa.Column('note_200', sa.String(length=118), nullable=True),
    sa.Column('note_100', sa.String(length=118), nullable=True),
    sa.Column('note_50', sa.String(length=118), nullable=True),
    sa.Column('note_20', sa.String(length=118), nullable=True),
    sa.Column('note_10', sa.String(length=118), nullable=True),
    sa.Column('coins', sa.String(length=118), nullable=True),
    sa.Column('total', sa.String(length=125), nullable=True),
    sa.Column('transaction', sa.String(length=110), nullable=True),
    sa.Column('status', sa.String(length=110), nullable=True),
    sa.Column('updated_on', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('invoice_no')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoice')
    op.drop_table('admin')
    # ### end Alembic commands ###
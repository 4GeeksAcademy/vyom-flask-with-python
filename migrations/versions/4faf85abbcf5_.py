"""empty message

Revision ID: 4faf85abbcf5
Revises: 0e43bdc25c31
Create Date: 2024-09-01 18:42:17.214846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4faf85abbcf5'
down_revision = '0e43bdc25c31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_constraint('character_planet_id_fkey', type_='foreignkey')
        batch_op.drop_column('planet_id')

    with op.batch_alter_table('starship', schema=None) as batch_op:
        batch_op.drop_constraint('starship_character_id_fkey', type_='foreignkey')
        batch_op.drop_column('character_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('starship', schema=None) as batch_op:
        batch_op.add_column(sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('starship_character_id_fkey', 'character', ['character_id'], ['id'])

    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('character_planet_id_fkey', 'planet', ['planet_id'], ['id'])

    # ### end Alembic commands ###

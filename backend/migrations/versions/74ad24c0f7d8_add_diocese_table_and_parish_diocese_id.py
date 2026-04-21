"""add_diocese_table_and_parish_diocese_id

Revision ID: 74ad24c0f7d8
Revises: e698cbe10913
Create Date: 2026-04-21 18:50:31.471098

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


revision: str = '74ad24c0f7d8'
down_revision: Union[str, None] = 'e698cbe10913'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DIOCESES = [
    # Norte
    ("Diocese de Óbidos", "PA"), ("Diocese de Santarém", "PA"), ("Diocese de Marabá", "PA"),
    ("Arquidiocese de Belém do Pará", "PA"), ("Diocese de Macapá", "AP"),
    ("Arquidiocese de Manaus", "AM"), ("Diocese de Boa Vista", "RR"),
    ("Diocese de Porto Velho", "RO"), ("Diocese de Rio Branco", "AC"),
    ("Diocese de Palmas", "TO"),
    # Nordeste
    ("Arquidiocese de Fortaleza", "CE"), ("Diocese de Sobral", "CE"), ("Diocese de Crato", "CE"),
    ("Arquidiocese de São Luís do Maranhão", "MA"), ("Diocese de Imperatriz", "MA"),
    ("Arquidiocese de Teresina", "PI"), ("Diocese de Parnaíba", "PI"),
    ("Arquidiocese de Natal", "RN"), ("Diocese de Mossoró", "RN"),
    ("Arquidiocese da Paraíba", "PB"), ("Diocese de Campina Grande", "PB"),
    ("Arquidiocese de Olinda e Recife", "PE"), ("Diocese de Caruaru", "PE"),
    ("Arquidiocese de Maceió", "AL"), ("Diocese de Penedo", "AL"),
    ("Arquidiocese de Aracaju", "SE"),
    ("Arquidiocese de Salvador", "BA"), ("Diocese de Feira de Santana", "BA"),
    ("Diocese de Vitória da Conquista", "BA"), ("Diocese de Ilhéus", "BA"),
    # Centro-Oeste
    ("Arquidiocese de Brasília", "DF"),
    ("Arquidiocese de Goiânia", "GO"), ("Diocese de Anápolis", "GO"),
    ("Arquidiocese de Cuiabá", "MT"), ("Diocese de Rondonópolis", "MT"),
    ("Diocese de Campo Grande", "MS"), ("Diocese de Dourados", "MS"),
    # Sudeste
    ("Arquidiocese de São Paulo", "SP"), ("Diocese de Santo André", "SP"),
    ("Diocese de São Bernardo do Campo", "SP"), ("Diocese de Mogi das Cruzes", "SP"),
    ("Diocese de Guarulhos", "SP"), ("Diocese de Osasco", "SP"),
    ("Diocese de Campinas", "SP"), ("Diocese de Sorocaba", "SP"),
    ("Diocese de Ribeirão Preto", "SP"), ("Diocese de São José do Rio Preto", "SP"),
    ("Diocese de Bauru", "SP"), ("Diocese de Santos", "SP"),
    ("Arquidiocese de Aparecida", "SP"),
    ("Arquidiocese do Rio de Janeiro", "RJ"), ("Diocese de Nova Iguaçu", "RJ"),
    ("Diocese de Duque de Caxias", "RJ"), ("Diocese de Campos dos Goytacazes", "RJ"),
    ("Diocese de Volta Redonda", "RJ"), ("Diocese de Petrópolis", "RJ"),
    ("Arquidiocese de Belo Horizonte", "MG"), ("Diocese de Contagem", "MG"),
    ("Diocese de Divinópolis", "MG"), ("Diocese de Juiz de Fora", "MG"),
    ("Diocese de Uberlândia", "MG"), ("Diocese de Montes Claros", "MG"),
    ("Arquidiocese de Vitória", "ES"), ("Diocese de Colatina", "ES"),
    # Sul
    ("Arquidiocese de Porto Alegre", "RS"), ("Diocese de Caxias do Sul", "RS"),
    ("Diocese de Santa Maria", "RS"), ("Diocese de Passo Fundo", "RS"),
    ("Diocese de Pelotas", "RS"),
    ("Arquidiocese de Florianópolis", "SC"), ("Diocese de Joinville", "SC"),
    ("Diocese de Blumenau", "SC"), ("Diocese de Chapecó", "SC"),
    ("Arquidiocese de Curitiba", "PR"), ("Diocese de Londrina", "PR"),
    ("Diocese de Maringá", "PR"), ("Diocese de Cascavel", "PR"),
    ("Diocese de Foz do Iguaçu", "PR"),
]


def upgrade() -> None:
    # Cria tabela diocese se ainda não existir
    op.execute("""
        CREATE TABLE IF NOT EXISTS diocese (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            state VARCHAR(2) NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_diocese_name ON diocese (name)")

    # Seed das dioceses brasileiras
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "INSERT INTO diocese (name, state, created_at) "
            "VALUES (:name, :state, NOW()) ON CONFLICT DO NOTHING"
        ),
        [{"name": name, "state": state} for name, state in DIOCESES],
    )

    # Adiciona diocese_id na tabela parish
    op.add_column('parish', sa.Column('diocese_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_parish_diocese_id'), 'parish', ['diocese_id'], unique=False)
    op.create_foreign_key(None, 'parish', 'diocese', ['diocese_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'parish', type_='foreignkey')
    op.drop_index(op.f('ix_parish_diocese_id'), table_name='parish')
    op.drop_column('parish', 'diocese_id')
    op.drop_table('diocese')

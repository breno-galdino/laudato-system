from graphemy import Graphemy, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID


class Sacrament(Graphemy, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parish_id: UUID = Field(foreign_key="parish.id", index=True)

    # Tipo: batismo, eucaristia, crisma, matrimonio, ordenacao, uncao, penitencia
    sacrament_type: str

    person_name: str
    person_dob: Optional[date] = None

    # Data em que o sacramento foi ministrado
    sacrament_date: date

    officiant: Optional[str] = None       # Nome do padre celebrante
    godfather: Optional[str] = None       # Padrinho (batismo / crisma)
    godmother: Optional[str] = None       # Madrinha (batismo / crisma)
    witness1: Optional[str] = None        # 1º testemunha (matrimônio)
    witness2: Optional[str] = None        # 2º testemunha (matrimônio)
    certificate_number: Optional[str] = None
    observations: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

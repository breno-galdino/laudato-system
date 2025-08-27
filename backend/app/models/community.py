from graphemy import Graphemy, Field

class Community(Graphemy, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    adress: str | None = None


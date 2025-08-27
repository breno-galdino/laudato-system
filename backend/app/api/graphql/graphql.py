from pathlib import Path
from graphemy import Graphemy, GraphemyRouter, import_files

from ...database import engine
from ...models import category, users, warning

Graphemy.metadata.create_all(engine)

router = GraphemyRouter(
    engine=engine,
    prefix="/graphql",
    tags=["graphql"],
    enable_put_mutations=True,
    enable_delete_mutations=True,
)


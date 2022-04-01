from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from __seedwork.domain.entities import Entity

# 3.10 - DataClass


@dataclass(kw_only=True, frozen=True, slots=True)  # init, repr, eq
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )

    def update(self, name: str, description: str):
        self._set('name', name)
        self._set('description', description)

    def activate(self):
        self._set('is_active',True)

    def deactivate(self):
        self._set('is_active',False)


# piramide de testes
# testes de unidades
# testes de integração
# testes e2e

# Michael Feathers

# update | activate | deactivate
# object.__setattr__()
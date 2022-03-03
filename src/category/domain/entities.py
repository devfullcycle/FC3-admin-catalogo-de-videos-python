from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
# 3.10 - DataClass

@dataclass() #init, repr, eq
class Category:

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )

# piramide de testes
# testes de unidades
# testes de integração
# testes e2e
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import EntityValidationException
#from __seedwork.domain.validators import ValidatorRules
from category.domain.validators import CategoryValidatorFactory

# 3.10 - DataClass


@dataclass(kw_only=True, frozen=True, slots=True)  # init, repr, eq
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=datetime.now
    )

    def __post_init__(self):
        if not self.created_at:
            self._set('created_at',  datetime.now())
        self.validate()

    def update(self, name: str, description: str):
        self._set('name', name)
        self._set('description', description)
        self.validate()

    def activate(self):
        self._set('is_active', True)

    def deactivate(self):
        self._set('is_active', False)

    # @classmethod
    # def validate(cls, name: str, description: str, is_active: bool = None):
    #     ValidatorRules.values(name, "name").required().string().max_length(255)
    #     ValidatorRules.values(description, "description").string()
    #     ValidatorRules.values(is_active, "is_active").boolean()

    def validate(self):
        validator = CategoryValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())
        if not is_valid:
            raise EntityValidationException(validator.errors)
        # lançar uma exceção


# piramide de testes
# testes de unidades
# testes de integração
# testes e2e

# Michael Feathers


# POST /categories - controller - usecase -> { name: "256" , invalidas} -> entidade

# Notification Pattern - Martin Fowler
# lib - Limite Parcial da Arquitetura

# required, max, positive, negativo, email, uuid, cartao de credito

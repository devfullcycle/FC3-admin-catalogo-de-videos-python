from abc import ABC
import abc
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')


class UseCase(Generic[Input, Output], ABC):  # pylint: disable=too-few-public-methods

    @abc.abstractmethod
    def execute(self, input_param: Input) -> Output:
        raise NotImplementedError()

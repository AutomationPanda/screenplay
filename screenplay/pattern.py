"""
Contains the core definitions for the Screenplay Pattern.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

import logging


# --------------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------
# Type Generics
# --------------------------------------------------------------------------------

Answer = TypeVar('Answer')


# --------------------------------------------------------------------------------
# Class: Actor
# --------------------------------------------------------------------------------

class Actor:

  def __init__(self, name: str = 'Actor') -> None:
    self.name: str = name
    self._abilities: dict[str, Any] = dict()

  def can_use(self, **kwargs: Any) -> None:
    self._abilities.update(kwargs)
    logger.debug(f'{self} can use: {kwargs}')

  def has(self, ability: str) -> bool:
    return ability in self._abilities

  def using(self, ability: str) -> Any:
    if not self.has(ability):
      raise MissingAbilityException(self, ability)
    value = self._abilities[ability]
    logger.debug(f'{self} is using "{ability}" as "{value}"')
    return value

  def attempts_to(self, task: Task) -> None:
    logger.info(f'{self} attempts to {task}')
    task.perform_as(self)
    logger.info(f'{self} did {task}')

  def asks_for(self, question: Question[Answer]) -> Answer:
    logger.info(f'{self} asks for {question}')
    answer = question.request_as(self)
    logger.info(f'{self} asked for {question} and got: {answer}')
    return answer

  def calls(self, question: Question[Answer]) -> Answer:
    logger.info(f'{self} calls {question}')
    answer = question.request_as(self)
    logger.info(f'{self} called {question} and got: {answer}')
    return answer

  def __str__(self) -> str:
    return self.name


# --------------------------------------------------------------------------------
# Abstract Class: Interaction
# --------------------------------------------------------------------------------

class Interaction(ABC):
  pass


# --------------------------------------------------------------------------------
# Abstract Class: Task
# --------------------------------------------------------------------------------

class Task(Interaction, ABC):
  @abstractmethod
  def perform_as(self, actor: Actor) -> None:
    pass


# --------------------------------------------------------------------------------
# Abstract Class: Question
# --------------------------------------------------------------------------------

class Question(Interaction, ABC, Generic[Answer]):
  @abstractmethod
  def request_as(self, actor: Actor) -> Answer:
    pass


# --------------------------------------------------------------------------------
# Class: ScreenplayException
# --------------------------------------------------------------------------------

class ScreenplayException(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)


# --------------------------------------------------------------------------------
# Class: MissingAbilityException
# --------------------------------------------------------------------------------

class MissingAbilityException(ScreenplayException):
  def __init__(self, actor: Actor, ability: str) -> None:
    super().__init__(f'The actor "{actor}" does not have an ability named "{ability}"')
    self.actor = actor
    self.ability = ability

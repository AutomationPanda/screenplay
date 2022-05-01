"""
Contains unit tests for the screenplay.pattern module.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest

from screenplay.pattern import Actor, Task, Question, MissingAbilityException


# --------------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def actor() -> Actor:
  return Actor()


# --------------------------------------------------------------------------------
# Tests: Actor
# --------------------------------------------------------------------------------

def test_actor_init_default(actor: Actor) -> None:
  assert len(actor._abilities) == 0   # type: ignore
  assert str(actor) == 'Actor'


def test_actor_init_with_name() -> None:
  andy = Actor('Andy')
  assert andy.name == 'Andy'
  assert str(andy) == 'Andy'
  assert len(andy._abilities) == 0   # type: ignore


def test_actor_has_an_ability(actor: Actor) -> None:
  actor.can_use(thing='tool')
  assert actor.has('thing')


def test_actor_does_not_have_an_ability(actor: Actor) -> None:
  actor.can_use(thing='tool')
  assert not actor.has('other')


def test_actor_has_multiple_abilities(actor: Actor) -> None:
  actor.can_use(thing='tool1', other='tool2')
  actor.can_use(third='tool3')
  assert actor.has('thing')
  assert actor.has('other')
  assert actor.has('third')
  assert not actor.has('tool1')
  assert not actor.has('tool2')
  assert not actor.has('tool3')


def test_actor_using_an_ability(actor: Actor) -> None:
  actor.can_use(thing='tool')
  thing: str = actor.using('thing')
  assert thing == 'tool'


def test_actor_using_one_of_multiple_ability(actor: Actor) -> None:
  actor.can_use(thing='tool1', other='tool2')
  actor.can_use(third='tool3')
  other: str = actor.using('other')
  assert other == 'tool2'


def test_actor_using_a_missing_ability_raises_an_exception(actor: Actor) -> None:
  with pytest.raises(MissingAbilityException) as e:
    actor.using('thing')
  assert e.value.actor == actor
  assert e.value.ability == 'thing'
  assert str(e.value) == 'The actor "Actor" does not have an ability named "thing"'


# --------------------------------------------------------------------------------
# Tests: Task
# --------------------------------------------------------------------------------

class AddAnAbility(Task):

  def __init__(self, name: str) -> None:
    self.name = name

  def perform_as(self, actor: Actor) -> None:
    actor.can_use(new_ability=self.name)


class UseAnAbility(Task):

  def perform_as(self, actor: Actor) -> None:
    value: str = actor.using('thing')
    actor.can_use(new_ability=value)


def test_actor_attempts_a_task_with_an_argument(actor: Actor) -> None:
  actor.attempts_to(AddAnAbility('cool'))
  assert actor.has('new_ability')
  assert actor.using('new_ability') == 'cool'


def test_actor_attempts_a_task_that_uses_an_ability(actor: Actor) -> None:
  actor.can_use(thing='cool')
  actor.attempts_to(UseAnAbility())
  assert actor.has('new_ability')
  assert actor.using('new_ability') == 'cool'


def test_actor_attempts_a_task_but_lacks_the_ability(actor: Actor) -> None:
  with pytest.raises(MissingAbilityException):
    actor.attempts_to(UseAnAbility())


# --------------------------------------------------------------------------------
# Tests: Question
# --------------------------------------------------------------------------------

class AddingOne(Question[int]):

  def __init__(self, amount: int) -> None:
    self.amount = amount

  def request_as(self, actor: Actor) -> int:
    return self.amount + 1


class AddingOneToStart(Question[int]):

  def request_as(self, actor: Actor) -> int:
    start: int = actor.using('start')
    return start + 1


def test_actor_asks_for_a_question_with_an_argument(actor: Actor):
  answer = actor.asks_for(AddingOne(5))
  assert answer == 6


def test_actor_asks_for_a_question_that_uses_an_ability(actor: Actor):
  actor.can_use(start=9)
  answer = actor.asks_for(AddingOneToStart())
  assert answer == 10


def test_actor_asks_for_a_question_but_lacks_the_ability(actor: Actor):
  with pytest.raises(MissingAbilityException):
    actor.asks_for(AddingOneToStart())


def test_actor_calls_a_question_with_an_argument(actor: Actor):
  answer = actor.calls(AddingOne(5))
  assert answer == 6


def test_actor_calls_a_question_that_uses_an_ability(actor: Actor):
  actor.can_use(start=9)
  answer = actor.calls(AddingOneToStart())
  assert answer == 10


def test_actor_calls_a_question_but_lacks_the_ability(actor: Actor):
  with pytest.raises(MissingAbilityException):
    actor.calls(AddingOneToStart())
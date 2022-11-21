# pylint: disable=dangerous-default-value,redefined-builtin,unused-argument
from typing import Any, Callable, Sequence
from django.db.models.manager import Manager
from django.db.models import QuerySet, Model

Deco = QuerySet[Model]


def select_related_decorator(func: Callable[..., Deco]) -> Callable[..., Deco]:
    def select_related_wrapper(
        objects: Manager[Any],
        *args: Any,
        select_related: Sequence[str] = (),
        **kwargs: Any,
    ) -> Deco:
        if select_related:
            return func(objects, *args, **kwargs).select_related(*select_related)
        return func(objects, *args, **kwargs)

    return select_related_wrapper


def prefetch_related_decorator(func: Callable[..., Deco]) -> Callable[..., Deco]:
    def prefetch_related_wrapper(
        objects: Manager[Any],
        *args: Any,
        prefetch_related: Sequence[str] = (),
        **kwargs: Any,
    ) -> Deco:
        if prefetch_related:
            return func(objects, *args, **kwargs).prefetch_related(*prefetch_related)
        return func(objects, *args, **kwargs)

    return prefetch_related_wrapper


def filter_decorator(func: Callable[..., Deco]) -> Callable[..., Deco]:
    def filter_wrapper(
        objects: Manager[Any],
        *args: Any,
        filter: dict[str, str | int] = {},
        **kwargs: Any,
    ) -> Deco:
        if filter:
            return func(objects, *args, **kwargs).filter(**filter)
        return func(objects, *args, **kwargs)

    return filter_wrapper


def aggregate_decorator(func: Callable[..., Deco]) -> Callable[..., Deco]:
    def aggregate_wrapper(
        objects: Manager[Any],
        *args: Any,
        aggregate: dict[str, str | int] = {},
        **kwargs: Any,
    ) -> Deco:
        if aggregate:
            return func(objects, *args, **kwargs).aggregate(**aggregate)  # type: ignore
        return func(objects, *args, **kwargs)

    return aggregate_wrapper


def annotate_decorator(func: Callable[..., Deco]) -> Callable[..., Deco]:
    def annotate_wrapper(
        objects: Manager[Any],
        *args: Any,
        annotate: dict[str, str | int] = {},
        **kwargs: Any,
    ) -> Deco:
        if annotate:
            return func(objects, *args, **kwargs).annotate(**annotate)
        return func(objects, *args, **kwargs)

    return annotate_wrapper


def first_decorator(func: Callable[..., Deco]) -> Callable[..., Deco]:
    def first_wrapper(
        objects: Manager[Any],
        *args: Any,
        first: bool = False,
        **kwargs: Any,
    ) -> Deco:
        if first:
            return func(objects, *args, **kwargs).first()  # type: ignore
        return func(objects, *args, **kwargs)

    return first_wrapper


def all_decorator(func: Callable[..., Deco]) -> Callable[..., Deco]:
    def all_wrapper(
        objects: Manager[Any],
        *args: Any,
        all: bool = False,
        **kwargs: Any,
    ) -> Deco:
        if all:
            return func(objects, *args, **kwargs).all()
        return func(objects, *args, **kwargs)

    return all_wrapper


def values_decorator(func: Callable[..., Deco]) -> Callable[..., Deco]:
    def values_wrapper(
        objects: Manager[Any],
        *args: Any,
        values: Sequence[str] = (),
        **kwargs: Any,
    ) -> Deco:
        if values:
            return func(objects, *args, **kwargs).values(*values)  # type: ignore
        return func(objects, *args, **kwargs)

    return values_wrapper


@annotate_decorator
@aggregate_decorator
@values_decorator
@all_decorator
@first_decorator
@filter_decorator
@select_related_decorator
@prefetch_related_decorator
def get_objects(objects: Deco, *args: Any, **kwargs: Any) -> Deco:
    return objects

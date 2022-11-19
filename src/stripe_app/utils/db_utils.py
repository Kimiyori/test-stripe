def select_related_decorator(func: callable):
    def select_related_wrapper(objects, select_related=(), *args, **kwargs):
        if select_related:
            return func(objects, *args, **kwargs).select_related(*select_related)
        return func(objects, *args, **kwargs)

    return select_related_wrapper


def prefetch_related_decorator(func: callable):
    def prefetch_related_wrapper(objects, prefetch_related=(), *args, **kwargs):
        if prefetch_related:
            return func(objects, *args, **kwargs).prefetch_related(*prefetch_related)
        return func(objects, *args, **kwargs)

    return prefetch_related_wrapper


def filter_decorator(func: callable):
    def filter_wrapper(objects, filter={}, *args, **kwargs):
        if filter:
            return func(objects, *args, **kwargs).filter(**filter)
        return func(objects, *args, **kwargs)

    return filter_wrapper


def aggregate_decorator(func: callable):
    def aggregate_wrapper(objects, aggregate={}, *args, **kwargs):
        if aggregate:
            return func(objects, *args, **kwargs).aggregate(**aggregate)
        return func(objects, *args, **kwargs)

    return aggregate_wrapper


def annotate_decorator(func: callable):
    def annotate_wrapper(objects, annotate={}, *args, **kwargs):
        if annotate:
            return func(objects, *args, **kwargs).annotate(**annotate)
        return func(objects, *args, **kwargs)

    return annotate_wrapper


def first_decorator(func: callable):
    def first_wrapper(objects, first: bool = False, *args, **kwargs):
        if first:
            return func(objects, *args, **kwargs).first()
        return func(objects, *args, **kwargs)

    return first_wrapper


def all_decorator(func: callable):
    def all_wrapper(objects, all: bool = False, *args, **kwargs):
        if all:
            return func(objects, *args, **kwargs).all()
        return func(objects, *args, **kwargs)

    return all_wrapper


def values_decorator(func: callable):
    def values_wrapper(objects, values=(), *args, **kwargs):
        if values:
            return func(objects, *args, **kwargs).values(*values)
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
def get_objects(objects, *args, **kwargs):
    return objects

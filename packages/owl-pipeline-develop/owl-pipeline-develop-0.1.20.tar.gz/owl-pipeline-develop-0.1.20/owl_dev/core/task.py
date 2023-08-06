from typing import Any, Callable

import prefect
from prefect import Task as pTask
from toolz import curry

from ..logging import logger


class Task(pTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger


class FunctionTask(Task):
    def __init__(self, fn: Callable, name: str = None, **kwargs: Any):
        if not callable(fn):
            raise TypeError("fn must be callable.")

        # set the name from the fn
        if name is None:
            name = getattr(fn, "__name__", type(self).__name__)

        prefect.core.task._validate_run_signature(fn)  # type: ignore
        self.run: Callable = fn

        super().__init__(name=name, **kwargs)


@curry
def task(fn: Callable, **task_init_kwargs: Any) -> FunctionTask:
    return FunctionTask(fn=fn, **task_init_kwargs)

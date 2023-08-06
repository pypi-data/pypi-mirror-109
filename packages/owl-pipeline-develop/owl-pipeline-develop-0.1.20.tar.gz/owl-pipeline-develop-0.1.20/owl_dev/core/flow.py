from contextlib import closing, suppress
from datetime import datetime
from functools import partial
from typing import Any, Dict

from prefect import Flow as pFlow
from prefect import Parameter

from owl_dev import database as db
from owl_dev.database import DBSession

from ..logging import logger


def visualize(task, old_state, new_state, flow=None):
    if isinstance(task, Parameter):
        return
    status = type(new_state).__name__
    with closing(DBSession()) as session:
        res = (
            session.query(db.Status)
            .filter(db.Status.flow == flow)
            .filter(db.Status.task == task.name)
            .first()
        )
        if res is None:
            res = db.Status(
                flow=flow, task=task.name, status=status, start=datetime.now(),
            )
            session.add(res)
        else:
            res.status = status

        if status in ["Success", "TriggerFailed", "Failed"]:
            res.end = datetime.now()

        res.last = datetime.now()

        session.commit()


class Flow(pFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

    def pars(self, parameters: Dict[str, Any] = None):
        self._parameters = parameters

    def run(self, **kwargs):
        with suppress(Exception):
            kwargs["parameters"] = self._parameters

        func = partial(visualize, flow=self.name)
        for task in self.get_tasks():
            task.state_handlers.append(func)

        return super().run(**kwargs)

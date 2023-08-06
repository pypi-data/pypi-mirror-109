import json
import os
import sys
import uuid
from contextlib import closing, suppress
from functools import wraps
from pathlib import Path

from prefect import Parameter  # noqa: F401

from owl_dev import database as db

from . import config  # noqa: F401
from .core.flow import Flow  # noqa: F401
from .core.task import Task, task  # noqa: F401

_author__ = "Eduardo Gonzalez Solares"
__email__ = "eglez@ast.cam.ac.uk"
__version__ = "0.1.20"


OWL_DONE = ".owl_completed"
SQLITEDB = "sqlite.db"


def setup(pdef=None):
    pdef = {} or pdef
    output_dir = pdef.get("output_dir", "auto")
    if output_dir == "auto":
        uid = uuid.uuid4().hex
        output_dir = f"/data/meds1_c/processed/{uid}"
        pdef["output_dir"] = output_dir
    config.set({"output_dir": Path(output_dir)})
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        with suppress(Exception):
            os.unlink(f"{output_dir}/sqlite.db")
        db.init_database(f"sqlite:///{output_dir}/sqlite.db")
        # sqlite_handler = SQLiteHandler(db_name=f"{output_dir}/sqlite.db")
        # logger = builtin_logging.getLogger("owl.daemon.pipeline")
        # logger.addHandler(sqlite_handler)
        with open(f"{output_dir}/config.yaml", "w") as fh:
            fh.write(json.dumps(pdef))
        with open(f"{output_dir}/env.yaml", "w") as fh:
            fh.write(json.dumps(dict(os.environ)))
    else:
        db.init_database("sqlite:///:memory:")

    with closing(db.DBSession()) as session:
        info = db.Info(
            config=json.dumps(pdef),
            env=json.dumps(dict(os.environ)),
            python=sys.version,
        )
        session.add(info)
        session.commit()


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            return obj.as_posix()
        return json.JSONEncoder.default(self, obj)


def pipeline(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        pdef = wrapper.config
        input_dir = kwds.get("input_dir")
        output_dir = kwds.get("output_dir")
        if output_dir is not None:
            input_dir = Path(input_dir)

            with suppress(Exception):
                (output_dir / OWL_DONE).unlink()

            with suppress(Exception):
                ({output_dir} / SQLITEDB).unlink()

            db.init_database(f"sqlite:///{output_dir}/{SQLITEDB}")
            # sqlite_handler = SQLiteHandler(db_name=f"{output_dir}/{SQLITEDB}")
            # logger.addHandler(sqlite_handler)
            # logger = builtin_logging.getLogger("owl.daemon.pipeline")
            with open(f"{output_dir}/config.yaml", "w") as fh:
                fh.write(json.dumps(pdef))
            with open(f"{output_dir}/env.yaml", "w") as fh:
                fh.write(json.dumps(dict(os.environ)))

        else:
            db.init_database("sqlite:///:memory:")

        with closing(db.DBSession()) as session:
            info = db.Info(
                config=JSONEncoder().encode(pdef),
                env=JSONEncoder().encode(dict(os.environ)),
                python=sys.version,
            )
            session.add(info)
            session.commit()

        try:
            f(*args, **kwds)
        finally:
            if output_dir is not None:
                (output_dir / OWL_DONE).touch()

    return wrapper

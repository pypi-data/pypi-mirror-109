import logging
import sqlite3

logger = logging.getLogger("owl.daemon.pipeline")


class SQLiteHandler(logging.Handler):
    _SQL_CREATE_TABLE = (
        "CREATE TABLE IF NOT EXISTS log("
        "'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', "
        "'filename', 'module', 'exc_info', 'stack_info', "
        "'lineno', 'funcName', 'created', 'msecs', 'relativeCreated', "
        "'thread', 'threadName', 'processName', 'process', "
        "'message', 'asctime')"
    )

    _SQL_INSERT_STATEMENT = (
        "INSERT INTO log ('name', 'msg', 'args', "
        "'levelname', 'levelno', 'pathname', 'filename', 'module', "
        "'exc_info', 'stack_info', 'lineno', 'funcName', "
        "'created', 'msecs', 'relativeCreated', 'thread', 'threadName', "
        "'processName', 'process', "
        "'message', 'asctime') "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    )

    def __init__(self, db_name: str = "logs.db"):
        logging.Handler.__init__(self)
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn.execute(self._SQL_CREATE_TABLE)
        self.conn.commit()
        self.cursor = self.conn.cursor()
        self.keys = [
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "message",
            "asctime",
        ]

    def emit(self, record):
        self.format(record)
        try:
            d = record.__dict__
            self.cursor.execute(
                self._SQL_INSERT_STATEMENT,
                [str(d[k]) for k in self.keys],
            )
            self.conn.commit()
        except:  # noqa
            print("CRITICAL DB ERROR, logging to database not possible.")

# flake8: noqa: F401
import warnings

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    import MySQLdb  # noqa: F401
except ImportError:
    try:
        import pymysql
    except ImportError as exc:
        raise ImproperlyConfigured(
            "Install mysqlclient or the pymysql extra for synchronous "
            "Django database operations."
        ) from exc

    pymysql.install_as_MySQLdb()

from django.db.backends.mysql.base import (
    DatabaseWrapper as _DatabaseWrapper,
)
from django.db.backends.mysql.base import *

from django_async_backend.db.backends.mariadb.async_base import (
    AsyncCursor,
    AsyncCursorDebugWrapper,
    AsyncDatabaseOperations,
    AsyncDatabaseWrapper,
    AsyncServerBindingCursor,
    AsyncServerSideCursor,
)


class DatabaseWrapper(_DatabaseWrapper):
    def get_connection_params(self):
        params = super().get_connection_params()
        params.pop("pool", None)

        if not getattr(
            settings, "ASYNC_BACKEND_DISABLE_POOL_WARNING", False
        ) and self.settings_dict.get("OPTIONS", {}).get("pool"):
            warnings.warn(
                "Using the asynchronous Django backend with a connection pool "
                "is unsafe in synchronous mode. Connection pools require the "
                "same event loop for each request, but the WSGI handler creates "
                "a new event loop for every request.",
                RuntimeWarning,
            )

        return params

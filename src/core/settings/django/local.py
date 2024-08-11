from .base import *  # noqa

INSTALLED_APPS += [  # noqa
    "django_extensions",
    "debug_toolbar",
]

MIDDLEWARE += [  # noqa
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda _: True,
# }


CELERY_TASK_ALWAYS_EAGER = True
CELERY_ALWAYS_EAGER = True
TASK_ALWAYS_EAGER = True
WORKER_ALWAYS_EAGER = True
ALWAYS_EAGER = True

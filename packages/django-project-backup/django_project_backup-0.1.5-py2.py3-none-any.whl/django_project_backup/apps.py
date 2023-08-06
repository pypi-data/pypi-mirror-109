import sys
import os

from django.apps import AppConfig


class DjangoProjectBackupConfig(AppConfig):
    name = 'django_project_backup'
    verbose_name = 'Django Project Backup'

    def ready(self):
        from .settings import REALTIME_BACKUP

        if REALTIME_BACKUP:
            if "migrate" not in sys.argv:  # disable backup while running django "migrate" command
                try:
                    from . import signals  # noqa F401

                    # create failsafe backup folders
                    from .settings import FAILSAFE_BACKUP_PATH, FAILSAFE_BACKUP_PATH_UPDATE, FAILSAFE_DELETE_PATH_DELETE

                    if not os.path.exists(FAILSAFE_BACKUP_PATH):
                        os.mkdir(FAILSAFE_BACKUP_PATH)
                    if not os.path.exists(FAILSAFE_BACKUP_PATH_UPDATE):
                        os.mkdir(FAILSAFE_BACKUP_PATH_UPDATE)
                    if not os.path.exists(FAILSAFE_DELETE_PATH_DELETE):
                        os.mkdir(FAILSAFE_DELETE_PATH_DELETE)

                except ImportError:
                    pass

import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# ===========================================================================

def _create_module(path):
    """Creates module directory if it doesn't exist and its containing
    __init__.py file."""
    if not os.path.isdir(path):
        os.makedirs(path)

    # create __init__.py
    i_file = os.path.join(path, '__init__.py')
    if not os.path.isfile(i_file):
        with open(i_file, 'w'):
            # write and empty file
            pass

# ---------------------------------------------------------------------------

class Command(BaseCommand):
    """Creates the local_settings directory structure used by yaset. Will not
    over-write any existing files. Creates an empty "import_redirect" file if
    it does not exist. Optionally takes a list of profiles to create.

    This command assumes the project root (i.e. where the settings.py is
    found) is ".../project/project" where the project base is defined in
    settings.BASE_DIR.
    """ 

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.__doc__

    def add_arguments(self, parser):
        # Command uses argparse, this method is called to add arguments
        parser.add_argument('profiles', nargs='*', type=str, help=(
            'Optional list of profile names to create. For example passing '
            'in "dev" and "prod" would create "dev.py", "prod.py", '
            '"secrets/dev.py" and "secrets/prod.py"'))

    def handle(self, *args, **options):
        project_name = os.path.basename(settings.BASE_DIR)
        project_root = os.path.join(settings.BASE_DIR, project_name)

        local_settings = os.path.join(project_root, 'local_settings')
        _create_module(local_settings)
        secrets = os.path.join(local_settings, 'secrets')
        _create_module(secrets)

        target = os.path.join(local_settings, 'import_redirect')
        if not os.path.isfile(target):
            with open(target, 'w'):
                # write and empty file
                pass

        for profile in options['profiles']:
            target = os.path.join(local_settings, '%s.py' % profile)
            if not os.path.isfile(target):
                with open(target, 'w'):
                    # write and empty file
                    pass

            target = os.path.join(secrets, '%s.py' % profile)
            if not os.path.isfile(target):
                with open(target, 'w'):
                    # write and empty file
                    pass

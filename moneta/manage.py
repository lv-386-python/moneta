<<<<<<< HEAD
#!/usr/bin/env python

=======
>>>>>>> origin/dev
import os
import sys


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "python"))
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "www"))
<<<<<<< HEAD

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'www.settings.settings')
=======
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
>>>>>>> origin/dev
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
execute_from_command_line(sys.argv)
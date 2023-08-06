"""
    Main app components definition.
"""
import sys

from pkg_resources import get_distribution
from cliff.commandmanager import CommandManager
from digicloud.cli.app import BaseApp
from digicloud.error_handlers import ErrorHandler

from .utils import get_help_file
from .middlewares import (
    ConfigMiddleware,
    SessionMiddleware,
    SignalHandlerMiddleware,
    VersionCheckMiddleware,
    RichMiddleware,
)


class DigicloudApp(BaseApp):
    def __init__(self):
        command_manager = CommandManager('digicloud.cli')
        self.current_version = get_distribution('digicloud').version
        super(DigicloudApp, self).__init__(
            description=get_help_file('digicloud.txt'),
            version=self.current_version,
            command_manager=command_manager,
            deferred_help=True
        )
        self.middlewares = [
            SignalHandlerMiddleware(self),
            ConfigMiddleware(self),
            SessionMiddleware(self),
            RichMiddleware(self),
            VersionCheckMiddleware(self),
        ]
        self.error_handler = ErrorHandler(self)


def main(argv=None):
    """Initialize main ``cliff.app.App`` instance and run.

    Cliff look for this function as a console script entry point.
    """
    if not argv:
        argv = sys.argv[1:]
    if len(argv) == 0:  # Disable interactive mode
        argv = ['--help']  # display --help instead of interactive mode
    if argv == ['--help']:
        print(get_help_file('digicloud.txt'))
        sys.exit()
    return DigicloudApp().run(argv)


if __name__ == '__main__':
    sys.exit(main())

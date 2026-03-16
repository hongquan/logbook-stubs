from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import logbook

from chameleon_log import RichHandler


def do_some_failed_action() -> None:
    msg = 'Something went wrong!'
    raise ValueError(msg)


def main() -> None:
    # Create a RichHandler with default settings
    handler = RichHandler()

    # Or customize the handler
    # handler = RichHandler(level=logbook.DEBUG)

    with handler:
        # Get a logger
        logger = logbook.Logger(__name__)

        # Log messages at different levels
        logger.debug('This is a debug message')
        logger.info('Application started successfully')
        logger.notice('This is a notice message')
        logger.warning('This is a warning message')
        logger.error('An error occurred')

        # Log with structured data
        birthday = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).replace(
            hour=20, minute=0, second=0, microsecond=0
        ) - timedelta(20 * 365)
        user_data = {'id': 123, 'name': 'Lê Lợi', 'active': True, 'birthday': birthday}
        logger.info('User logged in: {}', user_data)

        # Log a gunicorn-style access log to show HTTP method highlighting
        logger.info(
            '127.0.0.1 - - [15/Mar/2026:17:30:45 +0700] "GET /api/v1/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"'
        )

        # Log an exception
        try:
            do_some_failed_action()
        except ValueError:
            logger.exception('An error occurred during processing')


if __name__ == '__main__':
    main()

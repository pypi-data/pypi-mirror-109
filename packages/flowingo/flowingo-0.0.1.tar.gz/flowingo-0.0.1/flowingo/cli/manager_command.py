import socket

import click

from ..manager.app import app


@click.command()
@click.option('-d', '--demonize', is_flag=True, default=False, show_default=True, help='Demonize webserver')
def manager(demonize: bool):
    """Starts flowingo manager"""

    worker = app.Worker(
        hostname=f'manager@{socket.gethostname()}',
        # loglevel='INFO',
        loglevel='DEBUG',
        queues='manager',
        concurrency=1,
        pool='solo',
        send_task_events=True,  # TODO: fix enable events
    )
    worker.start()

import click
import uvicorn


@click.command()
@click.option('-p', '--port', type=int, default=8080, show_default=True, help='Webserver port')
# @click.option('--debug', is_flag=True, default=False, show_default=True, help='Debug mode')
@click.option('-d', '--demonize', is_flag=True, default=False, show_default=True, help='Demonize webserver')
def webserver(port: int, demonize: bool):
    """Starts flowingo webserver"""
    print('webserver !!')
    uvicorn.run(
        "app.app:app",
        host='0.0.0.0',
        port=4557,
        reload=True,
        debug=True,
        workers=1
    )

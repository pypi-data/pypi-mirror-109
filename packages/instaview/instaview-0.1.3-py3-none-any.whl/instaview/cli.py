import click
from .scraper import InstaViewer


@click.command()
@click.argument("username")
def stories(username):
    ig = InstaViewer(username)
    data = ig.get_stories(format="json")
    print(data)

@click.command()
@click.argument("username")
def posts(username):
    ig = InstaViewer(username)
    data = ig.get_posts(format="json")
    print(data)


@click.group()
def cli():
    pass


if __name__ == "__main__":
    cli.add_command(stories)
    cli.add_command(posts)
    cli()
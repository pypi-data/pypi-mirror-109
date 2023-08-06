"""Console script for notion_py."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("notionpy")
    click.echo("=" * len("notionpy"))
    click.echo("A terminal client of Notion.so in Python")


if __name__ == "__main__":
    main()  # pragma: no cover

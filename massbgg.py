from boardgamegeek import BGGClient
import click
import csv

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('path')
@click.option('--out', default=None)
def open_file_find_games(path, out=None):
    lines = None
    with open(path, 'r') as file:
        lines = [l.strip() for l in file.readlines()]
    click.echo('Read {} lines'.format(len(lines)))

    client = BGGClient()
    games = search_games(lines, client)
    click.echo('Found {} games'.format(len(games)))

    if out:
        with open(out, 'w', newline='') as file:
            fieldnames = list(printable_game_dict(games[0].data()).keys())
            csvfile = csv.DictWriter(file, delimiter=',', fieldnames=fieldnames)
            csvfile.writeheader()

            for game in games:
                printable = printable_game_dict(game.data())
                logger.debug(printable)
                csvfile.writerow(printable)


def printable_game_dict(game_dict):
    safe = game_dict.copy()
    safe.pop('alternative_names', None) # Has non unicode chars
    safe.pop('description', None) # Has newline chars
    return safe


def search_games(names, bgg_client):
    g = []
    for name in names:
        logger.info('Searching for: {}'.format(name))
        g.append(bgg_client.game(name))
        logger.debug(g[-1])
    return g


if __name__ == "__main__":
    open_file_find_games()
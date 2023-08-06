# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotify_backup']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['spotify-backup = spotify_backup:main']}

setup_kwargs = {
    'name': 'spotify-backup',
    'version': '0.0.2',
    'description': 'A Python script that exports all of your Spotify playlists.',
    'long_description': '# spotify-backup ![CI](https://github.com/emkor/spotify-backup/workflows/CI/badge.svg)\nFork of [caseychu/spotify-backup](https://github.com/caseychu/spotify-backup)\n\nPython CLI tool that exports all of your Spotify playlists and/or liked songs into CSV file\n\n## installation\n- pre-requisites: Python >=3.7, pip\n- command to install: `pip install spotify-backup` (dependency-free)\n\n## usage\n- get your Spotify OAuth Token [here](https://developer.spotify.com/web-api/console/get-playlists/)\n    - required scopes: `user-read-private`, `user-library-read`, `playlist-read-private`\n- execute `spotify-backup <OUTPUT FILE> --dump playlists,liked --token <YOUR TOKEN>`\n    - example: `spotify-backup my_backup.csv --dump playlists,liked --token SOME_VERY_LONG_TOKEN`\n\n## output format\n`<PLAYLIST NAME>,<TRACK URI>,<COMMA-SEPARATED TRACK ARTISTS>,<ALBUM NAME>,<TRACK NAME>`\n\n## output example\n```csv\nLiked Songs,spotify:track:7eMlLQXY5QICXuafv4haUg,"Massive Attack, Azekel",Ritual Spirit,Ritual Spirit\nLiked Songs,spotify:track:53Zvj4xbSFKwSJeXjyocHK,Boy Harsher,Careful,Fate\nLiked Songs,spotify:track:1IP0wkv3Hj7cPE159G9c2O,"PRO8L3M, Brodka",Fight Club,Żar\ntest,spotify:track:4u3cJaAUcmp4qPKUUcxXZv,UNKLE,War Stories,Mistress (feat Alicia Temple)\ntest,spotify:track:0MabrxpL9vrCJeOjGMnGgM,"Perturbator, Greta Link",The Uncanny Valley,Venger (feat. Greta Link)\ntest,spotify:track:0FoR0PrLkw6t64waJX3qT5,"Brodka, A_GIM",Wszystko czego dziś chcę (z serialu Rojst na Showmax),Wszystko czego dziś chcę (z serialu Rojst na Showmax)\ntest,spotify:track:5b2ACxzxhGeLPDr500fQzy,"deadmau5, Rob Swire",Ghosts \'n\' Stuff,Ghosts \'N\' Stuff - Radio Edit\ntest,spotify:track:4oezx4rQJnIBpKurukB2gN,trentemøller,Moan,Moan - Trentemøller Remix - Radio Edit\ntest,spotify:track:1itVstaGVBLPXqlv50HvDn,Goldfrapp,Ride A White Horse,Ride a White Horse - Serge Santiágo Re-Edit\n```\n\n## options\n```\nusage: spotify-backup [-h] [--token TOKEN] --dump {liked,playlists,playlists,liked,playlists,liked} [-d] file\n\nExports your Spotify playlists and/or Liked songs to CSV file.\n\npositional arguments:\n  file                  output filename\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --token TOKEN         Spotify OAuth token; requires `playlist-read-private` and `user-library-read` scopes; to get it, visit\n                        https://developer.spotify.com/console/get-playlists/ may also use SPOTIFY_OAUTH_TOKEN env var\n  --dump {liked,playlists,playlists,liked,playlists,liked}\n                        dump playlists or liked songs, or both (default: playlists)\n  -d, --debug           Enable more verbose logging\n```\n\n## known issues\n- collaborative playlists and playlist folders don\'t show up in the API, sadly.\n- tool downloads everything into memory before writing to file, need to rewrite client and use streaming / generators\n',
    'author': 'emkor93',
    'author_email': 'emkor93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emkor/spotify-backup',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

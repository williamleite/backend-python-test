"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt

from alayatodo import app
from alayatodo.service.utils import init_db

if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        init_db()
    else:
        app.run(use_reloader=True)

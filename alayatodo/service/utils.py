import os
import subprocess
import sys

import alayatodo


def init_db():
    print("Creating project structure")
    __create_folder_structure()

    print("Creating database")
    __create_db()

    print("Running \"fixtures\"")
    __run_sql(os.path.join('resources', 'fixtures.sql'))

    print("Running \"migrations\"")
    __run_sql(os.path.join('resources', 'V0001__alter_todos.sql'))

    print ("AlayaTodo: Database initialized.")


def __run_sql(filename):
    with alayatodo.app.open_resource(filename) as f:
        content = f.read().decode('utf-8').split(';')
        for line in content:
            alayatodo.db.engine.execute(line)


def __create_db():
    file_path = os.path.join(alayatodo.app.name, 'resources', 'database.sql')
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (alayatodo.app.config['DATABASE'], file_path),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, ex:
        print ex.output
        sys.exit(1)


def __create_folder_structure():
    db_path = alayatodo.app.config['DATABASE']
    dir_path = os.path.dirname(db_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

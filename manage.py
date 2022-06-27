from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api import create_app, db

# create app
app = create_app()

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
#db = SQLAlchemy(toxicity_analysis)
#migrate = Migrate(toxicity_analysis, db)


from app import routes

from flask import Flask
from flask_cors import CORS
from flask_restx import Api

app = Flask(__name__)
CORS(app)


api = Api(app, title='Emotion Recognition', description='Created by Amol Jagadambe',
          default='Flask', default_label='Controllers', doc='/swagger-ui.html/',
          validate=True, contact_url='http://www.gais.co.in', contact_email='amol.jagadambe@gmail.com',
          license='Apache 2.0', license_url='http://www.apache.org/licenses/LICENSE-2.0')

from application.resources import home

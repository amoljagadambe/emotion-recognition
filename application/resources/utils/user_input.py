from flask_restx import fields
from application import api

user_fields = api.model('Emotion Classification', {
    'audio_location': fields.String(required=True)
})

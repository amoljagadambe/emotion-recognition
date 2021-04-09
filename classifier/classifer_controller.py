# from application.resources.utils.user_input import user_fields
# from application.resources.utils.log_control import super_logs, error_logs
# from flask_restx import Resource
# from application import api
from flask import request
import os
from emotion_classifier import EmotionClassifier

classifier = EmotionClassifier()

# speakersController = api.namespace('emotion', description='Emotion Classifier Controller')

#check emotions
file_path = "/home/hp/gais/combo_emotion_recog/testaud.wav"
if os.path.exists(file_path):
    predicted_emotion_array = classifier.classify_audio(file_path)
    print(predicted_emotion_array[0])

# @speakersController.route('/classify')
# class EmotionController(Resource):
#     @api.expect(user_fields, validate=False)
#     def post(self):
#         try:
#             json_data = request.get_json(force=True)
#             file_path = json_data['audio_location']
#             if os.path.exists(file_path):
#                 predicted_emotion_array = classifier.classify_audio(file_path)
#                 super_logs.info(f"EMOTION CLASSIFICATION STATUS : {predicted_emotion_array[0]}")
#                 return predicted_emotion_array[0]
#
#             else:
#                 error_logs.error('FILE NOT FOUND -  FILE:{}'.format(file_path))
#                 return 'FILE NOT FOUND'
#         except (ValueError, KeyError):
#             error_logs.error('BAD KEY IN JSON')
#             return 'BAD KEY IN JSON'

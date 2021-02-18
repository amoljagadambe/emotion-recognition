import pyaudio
import wave
import librosa
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras import backend as K
from keras.models import load_model
from keras.optimizers import RMSprop
import os


BASE_DIR = os.path.abspath(os.path.dirname(__name__))
LABELS_PATH = BASE_DIR + "/application/resources/saved_models/label_classes.npy"
MODEL_PATH = BASE_DIR + "/application/resources/saved_models/Emotion_Voice_Detection_Model.h5"


class EmotionClassifier:

    # For recording audio
    def record_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16  # paInt8
        CHANNELS = 1
        RATE = 44100  # sample rate
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "live_audio.wav"
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)  # 2 bytes(16 bits) per channel

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        return True

    def classify_audio(self, file_path: str):
        X, sample_rate = librosa.load(file_path, res_type='kaiser_best', duration=3, sr=22050 * 2,
                                      offset=0.5)
        sample_rate = np.array(sample_rate)
        model = self.load_model()
        lb = LabelEncoder()
        lb.classes_ = np.load(LABELS_PATH, allow_pickle=True)
        features = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13), axis=0)
        features_df = pd.DataFrame(data=features)
        features_stacked = features_df.stack().to_frame().T
        features_expanded = np.expand_dims(features_stacked, axis=2)
        predictions = model.predict(features_expanded, batch_size=512, verbose=1)
        predictions_mod = predictions.argmax(axis=1)
        preds_flat = predictions_mod.astype(int).flatten()
        predictions_array = (lb.inverse_transform((preds_flat)))
        K.clear_session()
        return predictions_array

    def load_model(self):
        K.clear_session()
        model = load_model(MODEL_PATH)
        opt = RMSprop(learning_rate=0.0001, decay=1e-6)
        model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
        return model

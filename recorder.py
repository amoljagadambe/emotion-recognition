import pyaudio
import wave
import time
from remove_noise import remove_noise
from feat_util import speech_segments_with_vad
import os


def trim_audio_ffmpeg(src_file, start_tm, end_tm, dst_file):
    if not os.path.exists(src_file):
        return
    if os.path.exists(dst_file):
        os.remove(dst_file)
    commands = 'ffmpeg  -i \"{}\" -ss {:.2f} -to {:.2f} \"{}\" -y -loglevel panic'.format(
        src_file, start_tm, end_tm, dst_file)
    os.system(commands)
    return dst_file


def filename():

    timestr = time.strftime("%Y%m%d%H%M%S")
    # print(timestr)
    # the file name output you want to record into
    filename = "record_" + timestr + '.wav'

    return filename


class Recorder(object):

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._p = pyaudio.PyAudio()
        self.filewave = None
        self._stream = None

    def start_recording(self, filename, audio_format):
        self.filewave = self.prepare_file(filename, audio_format)
        self._stream = self._p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer,
            stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def get_callback(self):
        def callback(data, frame_count, time_info, status):
            self.filewave.writeframes(data)
            return data, pyaudio.paContinue
        return callback

    def prepare_file(self, filename, audio_format="wb"):
        filewave = wave.open(filename, audio_format)
        filewave.setnchannels(self.channels)
        filewave.setsampwidth(self._p.get_sample_size(pyaudio.paInt16))
        filewave.setframerate(self.rate)
        return filewave

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def close_recording(self):
        self._stream.close()
        self._p.terminate()
        self.filewave.close()

if __name__ == "__main__":
    fname = filename()
    rfile = Recorder(channels=2)
    rfile.start_recording(fname, 'wb')
    time.sleep(5.0)
    rfile.stop_recording()
    #remove noise
    nr_audio = fname[:-4] + '_nr.wav'
    if not remove_noise(fname, nr_audio, False):
        print("noise reduction not done yet!")
    else:
        sp_seg = speech_segments_with_vad(nr_audio)
        dst = fname[:-4] + '_trim.wav'
        dst_file = trim_audio_ffmpeg(nr_audio, sp_seg[0], sp_seg[1], dst)


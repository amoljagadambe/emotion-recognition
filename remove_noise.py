from os.path import exists, basename
from os import remove
import numpy as np
import scipy.signal as signal
import librosa
import matplotlib.pyplot as plt
from feat_util import speech_segments_with_vad


def remove_noise(org_file, dst_file, verbose=False):
    if not exists(org_file):
        print("No such file: {}".format(basename(org_file)))
        return False
    data, sr = librosa.load(org_file, 16000)
    N = 3
    Wn = 0.1
    B, A = signal.butter(N, Wn, output='ba')
    smooth_data = np.array(signal.filtfilt(B, A, data))

    if verbose:
        plt.plot(data, 'r-')
        plt.plot(smooth_data, 'b-')
        plt.show()

    # output result audio file
    if exists(dst_file):
        try:
            remove(dst_file)
        except Exception as e:
            print(e)
            return False

    librosa.output.write_wav(dst_file, smooth_data, sr)
    return True


if __name__ == '__main__':
    sp_seg = speech_segments_with_vad('noise_test_output.wav')
    print(sp_seg)
    # remove_noise('noise_test.wav', 'noise_test_output.wav', True)

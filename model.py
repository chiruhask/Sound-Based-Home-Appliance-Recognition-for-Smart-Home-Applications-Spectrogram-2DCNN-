import numpy as np
import librosa.display, os
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet import preprocess_input

base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
predictor = load_model('ui/model.keras')
class_labels = ['can_opening', 'clock_alarm', 'clock_tick', 'door_wood_creaks','door_wood_knock','glass_breaking','keyboard_typing','mouse_click','vaccum_cleaner','washing_machine','non_related']

def create_spectrogram(audio_file, image_file):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    audio_sig, sampling_rate = librosa.load(audio_file, sr=None)
    audio_stft = librosa.stft(audio_sig)
    S_dB = librosa.amplitude_to_db(np.abs(audio_stft),ref=np.max)
    librosa.display.specshow(S_dB)

    fig.savefig(image_file)
    plt.close(fig)

def get_sound_class(image_path):
    x = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(x)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    y = base_model.predict(x)
    predictions = predictor.predict(y)

    vectors = {}

    for i, label in enumerate(class_labels):
        vectors[label] = predictions[0][i]

    max_key = max(vectors, key=vectors.get)
    max_value = vectors[max_key]
    return max_key, max_value


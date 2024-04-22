import os
import numpy as np
import librosa
from scipy.io import wavfile
import soundfile as sf

# Get the list of all files in the audio directory
audio_path = "audio_in_use"
audio_files = os.listdir(audio_path)


def normalize_signal_to_rms_of_one(signal):
    """Normalize the signal to the target RMS = 1"""
    current_rms = np.sqrt(np.mean(np.square(signal)))
    return signal / current_rms 

values = np.logspace(np.log10(0.5), np.log10(2), num=5)

for i in range(len(audio_files)):
    """Normalise signal of clean audio file"""
    # Load the audio file
    filename = audio_files[i]
    print(os.path.splitext(filename)[0])
    clean_signal, clean_sr = librosa.load(audio_path+'\\'+filename, sr=None)  # Load with original sampling rate

    # Normalize the signal to the target RMS
    normalized_audio_signal = normalize_signal_to_rms_of_one(clean_signal)

    """Normalise signal of noise file"""
    # Get pink noise file
    pink_noise, sr = librosa.load('pink_noise.wav', sr=None)
    # truncate noise file to euqal to clean audio
    pink_noise = pink_noise[:len(clean_signal)]
    # Normalize the noise to the target RMS
    normalized_noise_signal = normalize_signal_to_rms_of_one(pink_noise)
    # Scale the noise to a desired level (optional)
    noise_level = 0.9  # Adjust the noise level as needed
    normalized_noise_signal = normalized_noise_signal * (noise_level / max(abs(normalized_noise_signal)))
    
    """Combine clean audio with noise"""
    if i in range(0,20):
        gain = values[0]
        noise_speech = normalized_audio_signal + gain*normalized_noise_signal
        
        sf.write('noisy_audio_0.5\\'+os.path.splitext(filename)[0]+'.wav', noise_speech, clean_sr)
   
    elif i in range(20,40):
        gain = values[1]
        noise_speech = normalized_audio_signal + gain*normalized_noise_signal
        
        sf.write('noisy_audio_0.7\\'+os.path.splitext(filename)[0]+'.wav', noise_speech, clean_sr)
    
    elif i in range(40,60):
        gain = values[2]
        noise_speech = normalized_audio_signal + gain*normalized_noise_signal
        
        sf.write('noisy_audio_1.0\\'+os.path.splitext(filename)[0]+'.wav', noise_speech, clean_sr)
    
    elif i in range(60,80):
        gain = values[3]
        noise_speech = normalized_audio_signal + gain*normalized_noise_signal
        
        sf.write('noisy_audio_1.4\\'+os.path.splitext(filename)[0]+'.wav', noise_speech, clean_sr)
   
    elif i in range(80,100):
        gain = values[4]
        noise_speech = normalized_audio_signal + gain*normalized_noise_signal
        
        sf.write('noisy_audio_2.0\\'+os.path.splitext(filename)[0]+'.wav', noise_speech, clean_sr)
        
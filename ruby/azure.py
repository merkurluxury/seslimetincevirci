import tkinter as tk
from tkinter import filedialog
import requests
import json
from PIL import Image, ImageTk
import pyaudio
import wave

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    convert_speech_to_text(file_path)

def convert_speech_to_text(file_path):
    subscription_key = "5d9eb28a005947e99fd7ac361b54a12d"
    region = "eastus"

    endpoint = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=tr-TR"

    with open(file_path, "rb") as audio_file:
        audio_data = audio_file.read()

    headers = {
        "Content-Type": "audio/wav",
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    response = requests.post(endpoint, headers=headers, data=audio_data)

    if response.status_code == 200:
        result = json.loads(response.content.decode())
        text_entry.delete(1.0, tk.END)
        text_entry.insert(tk.END, result["DisplayText"])
    else:
        print("Hata:", response.status_code, response.reason)
def record_audio():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    duration = 5  # 5 saniye kayıt

    filename = "recorded_audio.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    print("Ses kaydediliyor...")
    for i in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    convert_speech_to_text(filename)


# Tkinter uygulaması oluşturma
window = tk.Tk()
window.title("Sesli Metin Çevirici")
window.geometry("1280x720")
window.iconbitmap("gg.ico")

# Arka plan resmini yükle
background_image = Image.open("azureback.png")
background_photo = ImageTk.PhotoImage(background_image)

# Arka plan resmini görüntülemek için bir label oluştur
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
title_label = tk.Label(window, text="", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

# Ses dosyası seçme butonu
select_button = tk.Button(window, text="🎤 Ses Dosyası Seç", command=open_file_dialog, font=("Arial", 12, "bold"), bg="blue", fg="white", width=20, height=2)
select_button.pack(side=tk.LEFT, padx=20, pady=70)

# Ses kaydetme butonu
record_button = tk.Button(window, text="🔴 Ses Kaydet", command=record_audio,  font=("Arial", 12, "bold"), bg="red", fg="white", width=20, height=2)
record_button.pack(side=tk.LEFT, padx=20, pady=20)


# Metin alanı
text_entry = tk.Text(window, height=30, width=60, font=("Arial", 12))
text_entry.pack(pady=8)
# Uygulamayı çalıştırma
window.mainloop()

import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
import pyaudio
import wave
from PIL import Image, ImageTk

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    convert_speech_to_text(file_path)

def convert_speech_to_text(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        print("Ses dosyası yükleniyor...")
        audio = r.record(source)
        print("Ses dosyası yüklendi. Metne çevriliyor...")
        try:
            text = r.recognize_google_cloud(audio, credentials_json='C:/Users/serha/PycharmProjects/ruby/ruby-388713-59f8f5b631f1.json', language='tr-TR')
            text_entry.delete(1.0, tk.END)
            text_entry.insert(tk.END, text)
        except sr.UnknownValueError:
            print("Ses algılanamadı.")
        except sr.RequestError as e:
            print("İstek gönderilemedi; {0}".format(e))

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

def copy_text():
    text = text_entry.get(1.0, tk.END)
    window.clipboard_clear()
    window.clipboard_append(text)

def cut_text():
    copy_text()
    text_entry.delete(1.0, tk.END)

def paste_text():
    text = window.clipboard_get()
    text_entry.insert(tk.END, text)

# Tkinter uygulaması oluşturma
window = tk.Tk()
window.title("Sesli Metin Çevirici")
window.geometry("1280x720")
window.iconbitmap("gg.ico")
# Arka plan resmini yükle
background_image = Image.open("holi.png")
background_photo = ImageTk.PhotoImage(background_image)

# Arka plan resmini görüntülemek için bir label oluştur
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Başlık etiketi
title_label = tk.Label(window, text="", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

# Ses dosyası seçme butonu
select_button = tk.Button(window, text="🎤 Ses Dosyası Seç", command=open_file_dialog, font=("Arial", 12, "bold"), bg="blue", fg="white", width=50)
select_button.pack(pady=150)

# Ses kaydetme butonu
record_button = tk.Button(window, text="🔴 Ses Kaydet", command=record_audio, font=("Arial", 12, "bold"), bg="red", fg="white", width=50)
record_button.pack(pady=1)

# Metin alanı
text_entry = tk.Text(window, height=100, width=70, font=("Arial", 12))
text_entry.pack(pady=20)

# Uygulamayı çalıştırma
window.mainloop()


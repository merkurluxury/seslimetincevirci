import subprocess
import tkinter as tk
import pyaudio
import sys


def run_script1():
    subprocess.run([sys.executable, "google.py"])

def run_script2():
    subprocess.run([sys.executable, "aws.py"])

def run_script3():
    subprocess.run([sys.executable, "azure.py"])

root = tk.Tk()
root.title("Bulut Bilişim Final/ Ses- Metin Çevirici")
root.geometry("400x500")  # Masaüstü pencere boyutunu 300x400 olarak ayarlar

# Arka plan resmini yükleme
bg_image = tk.PhotoImage(file="main1.png")
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Buton 1
button1 = tk.Button(root, text="Google", command=run_script1, bg="blue", fg="white", width=15, height=5)
button1.pack(side=tk.LEFT, padx=10, pady=5)

# Buton 2
button2 = tk.Button(root, text="Amazon", command=run_script2, bg="green", fg="white", width=15, height=5)
button2.pack(side=tk.LEFT, padx=10, pady=5)

# Buton 3
button3 = tk.Button(root, text="Azure", command=run_script3, bg="red", fg="white", width=15, height=5)
button3.pack(side=tk.LEFT, padx=10, pady=3)

root.mainloop()

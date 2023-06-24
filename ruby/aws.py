import tkinter as tk
from tkinter import filedialog
import boto3

# AWS kimlik bilgilerini ayarlayın
aws_access_key_id = 'AKIAZVOHAGZDG3MNCD2E'
aws_secret_access_key = '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'
region_name = 'us-east-1'  # Amazon Transcribe hizmetinin bulunduğu bölgeye göre değiştirin

# AWS Transcribe istemcisini oluşturun
transcribe_client = boto3.client('transcribe', aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key,
                                 region_name=region_name)


def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    convert_speech_to_text(file_path)


def convert_speech_to_text(file_path):
    # Amazon Transcribe API ayarları
    job_name = 'xxx4'
    language_code = 'tr-TR'  # Gerekli dili seçin, isteğe bağlı olarak değiştirin

    # Ses dosyasını Amazon Transcribe'a gönderin
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        Media={'MediaFileUri': 's3://bulutbilisims3/' + file_path}
    )

    # Transkript işleminin tamamlanmasını bekleyin
    transcribe_client.get_waiter('transcription_job_completed').wait(
        TranscriptionJobName=job_name
    )

    # Transkript sonuçlarını alın
    response = transcribe_client.get_transcription_job(
        TranscriptionJobName=job_name
    )

    # Transkript metnini alın
    transcript_url = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    transcript = get_transcript_text(transcript_url)

    # Metni ekranda gösterin
    text_entry.delete(1.0, tk.END)
    text_entry.insert(tk.END, transcript)


def get_transcript_text(transcript_url):
    # Transkript dosyasını indirin
    response = boto3.client('s3').get_object(Bucket=transcript_url.split('/')[2], Key=transcript_url.split('/')[3])
    transcript = response['Body'].read().decode('utf-8')

    # JSON'dan metni çıkarın
    import json
    transcript_json = json.loads(transcript)
    transcript_text = transcript_json['results']['transcripts'][0]['transcript']

    return transcript_text


# Tkinter uygulaması oluşturma
window = tk.Tk()
window.title("Sesli Metin Dönüştürücü")
window.geometry("400x300")

# Ses dosyası seçme butonu
select_button = tk.Button(window, text="Ses Dosyası Seç", command=open_file_dialog)
select_button.pack(pady=10)

# Metin alanı
text_entry = tk.Text(window, height=10, width=40)
text_entry.pack(pady=10)

# Uygulamayı çalıştırma
window.mainloop()

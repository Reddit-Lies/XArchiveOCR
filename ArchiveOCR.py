import pytesseract
from PIL import Image
import os
import tqdm
import sqlite3
from datetime import datetime
import queue
import threading

# Connect to ArchiveIndex.db inside Twitter Archive
conn = sqlite3.connect('Twitter Archive/ArchiveIndex.db')
c = conn.cursor()

# Create a thread-safe queue
ocr_results_queue = queue.Queue()

# in the file "Twitter Archive" there are multiple folders with the date format "March 2022"
# Find the latest folder
folders = os.listdir("Twitter Archive")
folders.sort(key=lambda x: os.path.getmtime(os.path.join("Twitter Archive", x)), reverse=True)
# Find the latest folder
folders = [folder for folder in os.listdir("Twitter Archive") if os.path.isdir(os.path.join("Twitter Archive", folder))]
folders.sort(key=lambda x: os.path.getmtime(os.path.join("Twitter Archive", x)), reverse=True)
latest_folder = folders[0]

# print(f"Latest folder: {latest_folder}")

# navigate to data/tweets_media
media_folder = os.path.join("Twitter Archive", latest_folder, "data", "tweets_media")

# count the number of png and jpg files in the folder
img_count = len([file for file in os.listdir(media_folder) if file.endswith(".png")]) + len([file for file in os.listdir(media_folder) if file.endswith(".jpg")])

# create a progress bar
progress_bar = tqdm.tqdm(total=img_count, desc="Extracting text")

import concurrent.futures

# Define a function to process each image
def process_image(file):
    if file in processed_filenames:
        progress_bar.update(1)  # Update the progress bar to reflect this image was skipped
        return  # Skip processing since this image has already been analyzed
    
    progress_bar.set_description(f"Extracting text from {file}")
    text = pytesseract.image_to_string(Image.open(os.path.join(media_folder, file)))
    progress_bar.update(1)
    date = datetime.now().strftime('%Y-%m-%d')
    ocr_results_queue.put((os.path.join(media_folder, file), text, date))


def db_worker():
    conn = sqlite3.connect('Twitter Archive/ArchiveIndex.db')
    c = conn.cursor()
    batch_count = 0  # Initialize a counter to track the number of processed items in the batch

    while True:
        item = ocr_results_queue.get()
        
        # Check if the queue is sending a termination signal (None)
        if item is None:
            # If there are uncommitted changes when the termination signal is received, commit them
            if batch_count > 0:
                conn.commit()
            break
        
        c.execute("INSERT INTO OCR (image_path, OCR_text, OCR_date) VALUES (?, ?, ?)", item)
        batch_count += 1
        
        # Check if the batch size has reached 100
        if batch_count >= 100:
            conn.commit()  # Commit the batch
            batch_count = 0  # Reset the counter for the next batch

    conn.close()

# Before starting the database thread and the image processing

def load_existing_filenames():
    conn = sqlite3.connect('Twitter Archive/ArchiveIndex.db')
    c = conn.cursor()
    c.execute("SELECT image_path FROM OCR")
    filenames = {os.path.basename(row[0]) for row in c.fetchall()}
    conn.close()
    return filenames

processed_filenames = load_existing_filenames()


# Start the database thread
db_thread = threading.Thread(target=db_worker)
db_thread.start()

# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    # Create a list of futures for each image processing task
    futures = [executor.submit(process_image, file) for file in os.listdir(media_folder) if file.endswith(".png") or file.endswith(".jpg")]

    # Wait for all the futures to complete
    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
        # Get the result of each future (if needed)
        result = future.result()

# Signal the db_thread to stop and wait for it to finish
ocr_results_queue.put(None)
db_thread.join()

# close the progress bar
progress_bar.close()

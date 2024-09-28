import os
import requests
import csv
from tqdm import tqdm  # For progress bars

# Path to the CSV file
csv_file = 'download_list_swissALTI3D.csv'

# Directory to save the TIFF files
output_dir = 'TIF_download'

# Create the directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if not os.path.exists("TIF_merge"):
    os.makedirs("TIF_merge")

# Function to download files with a progress bar
def download_tiff(url):
    # Get the file name from the URL
    file_name = os.path.join(output_dir, url.split('/')[-1])
    
    # Send a GET request to download the file
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))  # Total size in bytes
    
    # Download the file with a progress bar
    with open(file_name, 'wb') as f, tqdm(
        desc=file_name,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        ncols=80,
        leave=False  # Prevents overwriting the global bar
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))
    
    return file_name

# Read URLs from the CSV file
with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    urls = [row[0] for row in reader]  # List of URLs

# Global progress bar for all files
with tqdm(total=len(urls), desc="Overall progress", ncols=80) as global_bar:
    for url in urls:
        # Download each file and update the global progress bar
        download_tiff(url)
        global_bar.update(1)  # Increment global bar after each file download

print("All files downloaded!")

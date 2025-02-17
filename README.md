# XArchiveOCR
Uses OCR to make an sqlite database of all the text in images you've uploaded to X.

# How to use
1. Create a folder called "Twitter Archive"
2. Download your twitter archive and extract it into a file named "[Month] [Year]" (ex. "February 2025")
   - (There should be 2 folders called "assets" and "data" and "Your archive.html" file in this folder.)
3. Ensure the python program is running in the folder containing "Twitter Archive"
4. The python program will check if 'ArchiveIndex.db' exists, if it does not it will create one in the Twitter Archive folder.

# Note
The program works best with screenshots, it cannot extract data from video, and it does not preserve the text of the tweet itself.

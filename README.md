# X Archive OCR
Uses OCR to make an sqlite database of all the text in images you've uploaded to X.

# File Structure
```
root
├── Twitter Archive
│   ├── ArchiveOCR.py
│   └── [Month] [Year] (ex. "February 2025)
│       ├── assets
│       ├── data
│       └── Your archive.html
```

# How to use
1. Create a folder called "Twitter Archive"
2. Download your twitter archive and extract it into a file named "[Month] [Year]" (ex. "February 2025")
   - (There should be 2 folders called "assets" and "data" and "Your archive.html" file in this folder.)
3. Ensure the python program is running from the root folder
4. The python program will check if 'ArchiveIndex.db' exists, if it does not it will create one in the Twitter Archive folder.

# How to search data once OCR is complete
1. Download DBbrowser from here: https://sqlitebrowser.org/
2. Click "Open Database" and open ArchiveIndex.db
3. Go to the "Browse Data" column
4. You can now search for text contained in images by typing in the "filter" box in the "OCR_Text" column

# Note
The program works best with screenshots, it cannot extract data from video, and it does not preserve the text of the tweet itself.

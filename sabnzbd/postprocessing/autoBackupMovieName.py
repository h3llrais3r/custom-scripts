# Custom sabnzbd post processing script to backup the original movie name.
# It stores the original movie file name in a custom nfo-sub file at the same location of the movie.

# sabnzbd parameters passed to the script at startup:
# %1 - full download path
# %2 - nzb name
# %3 - download name
# %4 - indexer report number
# %5 - category
# %6 - newsgroup
# %7 - status


import sys
import os


# Extension for the backup file
BACKUP_EXTENSION = ".nfo-sub"


def run():
    # Read parameters
    download_path = sys.argv[1]
    nzb_name = sys.argv[2]
    download_name = sys.argv[3]
    indexer_report_number = sys.argv[4]
    category = sys.argv[5]
    newsgroup = sys.argv[6]
    status = sys.argv[7]

    # Print parameters
    print "full download path: " + download_path
    print "nzb name: " + nzb_name
    print "download name: " + download_name
    print "indexer report number: " + indexer_report_number
    print "category: " + category
    print "newsgroup: " + newsgroup
    print "status: " + status

    # Backup
    _backup_movie_name(download_path, nzb_name, download_name, indexer_report_number, category, newsgroup, status)


def _backup_movie_name(download_path, nzb_name, download_name, indexer_report_number, category, newsgroup, status):
    for dirname, dirnames, filenames in os.walk(os.path.join(download_path)):
        for filename in filenames:
            splitname = filename.split(".")
            ext = splitname[len(splitname) - 1]
            if ext in ('avi', 'mkv', 'wmv', 'ts', 'mp4', 'iso', 'm2ts'):
                backup_filename = filename + BACKUP_EXTENSION
                backup_file = os.path.join(dirname, backup_filename)
                file = open(backup_file, "w")
                file.write("<?xml version='1.0' encoding='utf-8'?>")
                file.write("<details>")
                file.write("<originalFileName>")
                file.write(filename)
                file.write("</originalFileName>")
                file.write("<finalFileName>")
                file.write(filename)
                file.write("</finalFileName>")
                file.write("</details>")
                file.close()
                print "autoBackupMovieName: created backup file: " + backup_file


# Run the script
run()
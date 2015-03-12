# Custom Sick-Beard post processing script to backup the original tv show name.
# It stores the original tv show file name in a custom .nfo-sub file and moves it to the backup location.
# CONFIGURATION: change the value of BACKUP_LOCATION_PATH to the path of your backup location!

# sabnzbd parameters passed to the script at startup:
# %1 - final filename
# %2 - original filename
# %3 - tvdb id
# %4 - season number
# %5 - episode number
# %6 - episode air date


import logging
import os
import sys
import shutil


BACKUP_EXTENSION = ".nfo-sub"
BACKUP_LOCATION_PATH = "C:/Tools/Downloads/subtitles/backup/"
LOG_FILE = os.path.dirname(os.path.realpath(sys.argv[0])) + "/autoBackupTVShowName.log"

# Logging config (change to logging.DEBUG for debug info)
logging.basicConfig(filename=LOG_FILE, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("autoBackupTVShowName")


def run():
    # Read parameters
    full_final_name = sys.argv[1]
    full_original_name = sys.argv[2]
    tvdb_id = sys.argv[3]
    season = sys.argv[4]
    episode = sys.argv[5]
    air_date = sys.argv[6]

    # Print parameters
    print "final filename: " + full_final_name
    print "original filename: " + full_original_name
    print "tvdb id: " + tvdb_id
    print "season number: " + season
    print "episode number: " + episode
    print "episode air date: " + air_date

    # Log parameters
    logger.info("final filename: " + full_final_name)
    logger.info("original filename: " + full_original_name)
    logger.info("tvdb id: " + tvdb_id)
    logger.info("season number: " + season)
    logger.info("episode number: " + episode)
    logger.info("episode air date: " + air_date)

    # Backup
    backup_file = _backup_tvshow_name(full_final_name, full_original_name, tvdb_id, season, episode, air_date)

    # Move
    _move_backup_file(backup_file)


def _backup_tvshow_name(full_final_name, full_original_name, tvdb_id, season, episode, air_date):
    original_name = os.path.basename(full_original_name)
    final_name = os.path.basename(full_final_name)
    backup_file = full_final_name + BACKUP_EXTENSION
    file = open(backup_file, "w")
    file.write("<?xml version='1.0' encoding='utf-8'?>")
    file.write("<details>")
    file.write("<originalFileName>")
    file.write(original_name)
    file.write("</originalFileName>")
    file.write("<finalFileName>")
    file.write(final_name)
    file.write("</finalFileName>")
    file.write("</details>")
    file.close()
    print "Created backup file %s" % backup_file
    logger.info("Created backup file %s" % backup_file)
    return backup_file


def _move_backup_file(backup_file_path):
    location = os.path.join(BACKUP_LOCATION_PATH)
    backup = os.path.join(backup_file_path)
    backup_file = os.path.join(BACKUP_LOCATION_PATH, os.path.basename(backup_file_path))
    try:
        os.remove(backup_file)
        print "Backup already exists, deleting old backup %s" % backup_file
        logger.info("Backup already exists, deleting old backup %s" % backup_file)
    except OSError:
        # Backup file does not exist yet, continue
        pass
    try:
        shutil.move(backup, location)
        print "Moved backup file %s to the backup location %s" % (backup, location)
        logger.info("Moved backup file %s to the backup location %s" % (backup, location))
    except Exception, e:
        print "Exception: %s" % e
        logger.error("Exception: %s" % e)


# Run the script
run()
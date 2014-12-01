# Custom utorrent post processing script for handling torrents based on their label.
# It moves the download to it's appropriate location and renames it (if needed) while moving.
# CONFIGURATION: create an entry in the LABELS dict for each label that you want to be supported/processed.

# utorrent parameters that are available:
# %F - Name of downloaded file (for single file torrents)
# %D - Directory where files are saved
# %N - Title of torrent
# %P - Previous state of torrent
# %L - Label
# %T - Tracker
# %M - Status message string (same as status column)
# %I - hex encoded info-hash
# %S - State of torrent
# %K - kind of torrent (single|multi)

# utorrent parameters passed to the script at startup:
# %D - Directory where files are saved
# %N - Title of torrent
# %L - Label
# %K - kind of torrent (single|multi)
# %F - Name of downloaded file (for single file torrents)
# %S - State of torrent
#
# Example: C:\Tools\Scripts\autoProcessTorrent.bat "%D" "%N" "%L" "%K" "%F" "%S"


import logging
import os
import sys
import shutil


LOG_FILE = os.path.dirname(os.path.realpath(sys.argv[0])) + "/autoProcessTorrent.log"
SICKRAGE_PROCESSING_PATH = "//HTPC/Downloads/complete/sickrage"

# Dict with supported labels
# Usage: 'LABEL_KEY' : {'label' : 'label_value', 'destination' : 'destination_path'}
LABELS = {
    'SICKRAGE-ANIME': {'label': 'sickrage-anime', 'destination': SICKRAGE_PROCESSING_PATH}
}

# Logging config (change to logging.DEBUG for debug info)
logging.basicConfig(filename=LOG_FILE, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("autoProcessTorrent")


def run():
    # Read parameters
    download_dir = sys.argv[1]
    title = sys.argv[2]
    label = sys.argv[3]
    kind = sys.argv[4]
    downloaded_filename = sys.argv[5]
    state = sys.argv[6]

    # Skip when state is not 'Finished'
    if state != '11':
        return

    logger.info("----------------------------------------------")
    logger.info("Start auto processing torrent '%s'" % title)
    logger.debug("Input parameters:")
    logger.debug("download dir: " + download_dir)
    logger.debug("title: " + title)
    logger.debug("label: " + label)
    logger.debug("kind: " + kind)
    logger.debug("downloaded file name (in case of kind = 'single'): " + downloaded_filename)
    logger.debug("state: " + state)

    try:
        _move(download_dir, title, label, kind, downloaded_filename)
    except Exception, e:
        logger.error("Exception: %s" % e)

    logger.info("Finished.")
    logger.info("----------------------------------------------")


def _move(download_dir, title, label, kind, download_filename):
    # Check label specs
    label_specs = _get_label_specs(label)
    # Move based on kind of torrent
    if label_specs is not None:
        if kind == 'single':
            _move_file(download_dir, download_filename, label_specs)
        elif kind == 'multi':
            _move_all(download_dir, label_specs)
        else:
            logger.warn("No valid kind of torrent found")
            logger.warn("Skipping auto process")
    else:
        logger.warn("No supported label found")
        logger.warn("Skipping auto process")


def _get_label_specs(label):
    logger.info("Getting label specs")
    for key, specs in LABELS.items():
        # Matching spces found
        if label.find(specs['label']) != -1:
            logger.info("Found specs for label '%s'" % (specs['label']))
            logger.debug("Label specs: %s" % specs)
            return specs
    return None


def _move_file(directory, filename, label_specs):
    try:
        logger.info("Trying to move file '%s'" % filename)
        origin = os.path.join(directory, filename)
        destination = os.path.join(label_specs['destination'], filename)
        shutil.move(origin, destination)
        logger.info("Moved file '%s' to '%s'" % (origin, destination))
    except Exception, e:
        logger.error("Exception: %s" % e)


# Not yet tested!!!!
def _move_all(directory, label_specs):
    try:
        logger.info("Trying to move all files in '%s'" % directory)
        origin_dir = os.path.join(directory)
        files = os.listdir(origin_dir)
        for fileName in files:
            _move_file(directory, fileName, label_specs)
    except Exception, e:
        logger.error("Exception: %s" % e)


# Run the script
run()
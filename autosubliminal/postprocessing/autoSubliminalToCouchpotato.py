# Custom Auto-Subliminal post processing script.
# It moves an movie and its subtitle from Auto-Subliminal to the Couchpotato post processing folder.
# CONFIGURATION: changes the values of AUTOSUBLIMINAL_PATH and COUCHPOTATO_PATH to your paths.

# Auto-Subliminal parameters passed to the script at startup:
# %1 - encoding
# %2 - movie path
# %3 - subtitle path

import glob
import logging
import os
import stat
import sys
import shutil

# Paths
AUTOSUBLIMINAL_PATH = "//SERVER/couchpotato-autosubliminal/"
COUCHPOTATO_PATH = "C:/Tools/Downloads/complete/couchpotato/"

# Normalized paths (path and case) because paths are compaired when executing cleanup
NORM_AUTOSUBLIMINAL_PATH = os.path.normcase(os.path.normpath(AUTOSUBLIMINAL_PATH))
NORM_COUCHPOTATO_PATH = os.path.normcase(os.path.normpath(COUCHPOTATO_PATH))

# Logging config (change to logging.DEBUG for debug info)
LOG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/autoSubliminalToCouchpotato.log"
logging.basicConfig(filename=LOG_FILE, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("autoSubliminalToCouchpotato")


def run():
    print ""
    print "#" * 30
    print "Couchpotato post processing folder: %s" % NORM_COUCHPOTATO_PATH
    logger.info("----------------------------------------------")
    logger.info("Couchpotato post processing folder: %s" % NORM_COUCHPOTATO_PATH)

    # Read parameters (sys.argv[0] = path to this script)
    encoding = sys.argv[1]
    movie_path = _decode(sys.argv[2], encoding)
    subtitle_path = None
    if len(sys.argv) == 4:
        subtitle_path = _decode(sys.argv[3], encoding)

    # Print parameters
    print "encoding: " + encoding
    logger.info("encoding: " + encoding)
    print "movie path: " + movie_path
    logger.info("movie path: " + movie_path)
    if subtitle_path:
        print "subtitle path: " + subtitle_path
        logger.info("subtitle path: " + subtitle_path)

    # Move
    if _move(movie_path, subtitle_path):
        # Move additional subtitles
        _move_additional_subtitles(movie_path)
        # Cleanup
        _cleanup(movie_path)

    print "#" * 30
    logger.info("----------------------------------------------")


def _decode(value, encoding):
    # Decode a value if encoding is specified
    if encoding:
        return value.decode(encoding)
    return value


def _move(movie_path, subtitle_path):
    try:
        destination = os.path.join(NORM_COUCHPOTATO_PATH)
        movie = os.path.join(movie_path)
        shutil.move(movie, destination)
        print "Moved movie to the Couchpotato post processing folder"
        logger.info("Moved movie to the Couchpotato post processing folder")
        if subtitle_path:
            subtitle = os.path.join(subtitle_path)
            shutil.move(subtitle, destination)
            print "Moved subtitle to the Couchpotato post processing folder"
            logger.info("Moved subtitle to the Couchpotato post processing folder")
        return True
    except Exception, e:
        print "Exception: %s" % e
        logger.error("Exception: %s" % e)
        return False


def _move_additional_subtitles(movie_path):
    """
    Move additional subtitles if there are any found at the same location.
    """
    try:
        path_name = os.path.splitext(os.path.normpath(movie_path))[0]
        subtitles = glob.glob(path_name + '*' + '.srt')
        if subtitles:
            destination = os.path.join(NORM_COUCHPOTATO_PATH)
            for subtitle in subtitles:
                shutil.move(subtitle, destination)
                print "Moved additional subtitle to the Couchpotato post processing folder: %s" % subtitle
                logger.info("Moved additional subtitle to the Couchpotato post processing folder: %s" % subtitle)

    except Exception, e:
        print "Exception: %s" % e
        logger.error("Exception: %s" % e)


def _cleanup(movie_path):
    """
    Cleanup leftovers.
    We need to clean up when:
    - the movie is located in the autosubliminal path
    - the movie is in a subfolder underneath the autosubliminal path
    """
    norm_movie_path = os.path.normcase(os.path.normpath(movie_path))
    in_root_folder = os.path.commonprefix([NORM_AUTOSUBLIMINAL_PATH, norm_movie_path]) == NORM_AUTOSUBLIMINAL_PATH
    if in_root_folder:
        # Check if the movie is in a subfolder of the root folder
        movie_folder = os.path.dirname(norm_movie_path)
        in_sub_folder = movie_folder != NORM_AUTOSUBLIMINAL_PATH
        if in_sub_folder:
            while movie_folder != NORM_AUTOSUBLIMINAL_PATH:
                folder_to_clean = movie_folder
                # Move 1 folder up
                movie_folder = os.path.dirname(movie_folder)
            try:
                # Remove the folder of the movie inside the root folder
                shutil.rmtree(folder_to_clean, onerror=_set_rw_and_remove)
                print "Removed movie folder: %s" % folder_to_clean
                logger.info("Removed movie folder: %s" % folder_to_clean)
            except Exception, e:
                print "Exception: %s" % e
                logger.error("Exception: %s" % e)
        else:
            print "Movie is located directly under an autosubliminal video folder"
            print "Skipping cleanup"
    else:
        print "Movie is not located in an autosubliminal video folder"
        print "Skipping cleanup"
        logger.info("Movie is not located in an autosubliminal video folder")
        logger.info("Skipping cleanup")


def _set_rw_and_remove(operation, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


# Run the script
run()

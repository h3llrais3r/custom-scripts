# Custom Auto-Subliminal post processing script.
# It moves an episode and its subtitle from Auto-Subliminal to the Sick-Beard post processing folder.
# CONFIGURATION: changes the values of AUTOSUBLIMINAL_PATH and SICKBEARD_PATH to your paths.

# Auto-Subliminal parameters passed to the script at startup:
# %1 - encoding
# %2 - episode path
# %3 - subtitle path

import glob
import logging
import os
import stat
import sys
import shutil

# Paths
AUTOSUBLIMINAL_PATH = "//SERVER/sickbeard-autosubliminal/"
SICKBEARD_PATH = "C:/Tools/Downloads/complete/sickbeard/"

# Normalized paths (path and case) because paths are compaired when executing cleanup
NORM_AUTOSUBLIMINAL_PATH = os.path.normcase(os.path.normpath(AUTOSUBLIMINAL_PATH))
NORM_SICKBEARD_PATH = os.path.normcase(os.path.normpath(SICKBEARD_PATH))

# Logging config (change to logging.DEBUG for debug info)
LOG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/autoSubliminalToSickbeard.log"
logging.basicConfig(filename=LOG_FILE, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("autoSubliminalToSickbeard")


def run():
    print ""
    print "#" * 30
    print "Sickbeard post processing folder: %s" % NORM_SICKBEARD_PATH
    logger.info("----------------------------------------------")
    logger.info("Sickbeard post processing folder: %s" % NORM_SICKBEARD_PATH)

    # Read parameters (sys.argv[0] = path to this script)
    encoding = sys.argv[1]
    episode_path = _decode(sys.argv[2], encoding)
    subtitle_path = None
    if len(sys.argv) == 4:
        subtitle_path = _decode(sys.argv[3], encoding)

    # Print parameters
    print "encoding: " + encoding
    logger.info("encoding: " + encoding)
    print "episode path: " + episode_path
    logger.info("episode path: " + episode_path)
    if subtitle_path:
        print "subtitle path: " + subtitle_path
        logger.info("subtitle path: " + subtitle_path)

    # Move
    if _move(episode_path, subtitle_path):
        # Move additional subtitles
        _move_additional_subtitles(episode_path)
        # Cleanup
        _cleanup(episode_path)

    print "#" * 30
    logger.info("----------------------------------------------")


def _decode(value, encoding):
    # Decode a value if encoding is specified
    if encoding:
        return value.decode(encoding)
    return value


def _move(episode_path, subtitle_path):
    try:
        destination = os.path.join(NORM_SICKBEARD_PATH)
        episode = os.path.join(episode_path)
        shutil.move(episode, destination)
        print "Moved episode to the Sickbeard post processing folder"
        logger.info("Moved episode to the Sickbeard post processing folder")
        if subtitle_path:
            subtitle = os.path.join(subtitle_path)
            shutil.move(subtitle, destination)
            print "Moved subtitle to the Sickbeard post processing folder"
            logger.info("Moved subtitle to the Sickbeard post processing folder")
        return True
    except Exception, e:
        print "Exception: %s" % e
        logger.error("Exception: %s" % e)
        return False


def _move_additional_subtitles(episode_path):
    """
    Move additional subtitles if there are any found at the same location.
    """
    try:
        path_name = os.path.splitext(os.path.normpath(episode_path))[0]
        subtitles = glob.glob(path_name + '*' + '.srt')
        if subtitles:
            destination = os.path.join(NORM_SICKBEARD_PATH)
            for subtitle in subtitles:
                shutil.move(subtitle, destination)
                print "Moved additional subtitle to the Sickbeard post processing folder: %s" % subtitle
                logger.info("Moved additional subtitle to the Sickbeard post processing folder: %s" % subtitle)

    except Exception, e:
        print "Exception: %s" % e
        logger.error("Exception: %s" % e)


def _cleanup(episode_path):
    """
    Cleanup leftovers.
    We need to clean up when:
    - the episode is located in the autosubliminal path
    - the episode is in a subfolder underneath the autosubliminal path
    """
    norm_episode_path = os.path.normcase(os.path.normpath(episode_path))
    in_root_folder = os.path.commonprefix([NORM_AUTOSUBLIMINAL_PATH, norm_episode_path]) == NORM_AUTOSUBLIMINAL_PATH
    if in_root_folder:
        # Check if the episode is in a subfolder of the root folder
        episode_folder = os.path.dirname(norm_episode_path)
        in_sub_folder = episode_folder != NORM_AUTOSUBLIMINAL_PATH
        if in_sub_folder:
            while episode_folder != NORM_AUTOSUBLIMINAL_PATH:
                folder_to_clean = episode_folder
                # Move 1 folder up
                episode_folder = os.path.dirname(episode_folder)
            try:
                # Remove the folder of the episode inside the root folder
                shutil.rmtree(folder_to_clean, onerror=_set_rw_and_remove)
                print "Removed episode folder: %s" % folder_to_clean
                logger.info("Removed episode folder: %s" % folder_to_clean)
            except Exception, e:
                print "Exception: %s" % e
                logger.error("Exception: %s" % e)
        else:
            print "Episode is located directly under an autosubliminal video folder"
            print "Skipping cleanup"
    else:
        print "Episode is not located in an autosubliminal video folder"
        print "Skipping cleanup"
        logger.info("Episode is not located in an autosubliminal video folder")
        logger.info("Skipping cleanup")


def _set_rw_and_remove(operation, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


# Run the script
run()

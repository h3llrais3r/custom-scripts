# Custom Auto-Subliminal post processing script.
# It moves a video file and (optionally) its subtitle from Auto-Subliminal to a new destination.
# CONFIGURATION: changes the values of AUTOSUBLIMINAL_PATH to your path.

# Required parameter to be specified when running the script:
# %1 - destination path

# Auto-Subliminal parameters passed to the script:
# %2 - encoding
# %3 - video path
# %4 - subtitle path (optional)

import glob
import logging
import os
import stat
import sys
import shutil

# Paths
AUTOSUBLIMINAL_PATH = "//SERVER/sickrage-autosubliminal/"

# Normalized paths (path and case) because paths are compaired when executing cleanup
NORM_AUTOSUBLIMINAL_PATH = os.path.normcase(os.path.normpath(AUTOSUBLIMINAL_PATH))

# Logging config (change to logging.DEBUG for debug info)
LOG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/autoMoveAndCleanup.log"
logging.basicConfig(filename=LOG_FILE, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("autoMoveAndCleanup")


def run():
    print ""
    print "#" * 30
    logger.info("----------------------------------------------")

    # Read parameters (sys.argv[0] = path to this script)
    destination_path = os.path.normcase(os.path.normpath(sys.argv[1]))
    encoding = sys.argv[2]
    video_path = _decode(sys.argv[3], encoding)
    subtitle_path = None
    if len(sys.argv) == 5:
        subtitle_path = _decode(sys.argv[4], encoding)

    # Print parameters
    print "destination: %s" % destination_path
    logger.info("destination: %s" % destination_path)
    print "encoding: " + encoding
    logger.info("encoding: " + encoding)
    print "video path: " + video_path
    logger.info("video path: " + video_path)
    if subtitle_path:
        print "subtitle path: " + subtitle_path
        logger.info("subtitle path: " + subtitle_path)

    # Move
    if _move(destination_path, video_path, subtitle_path):
        # Move additional subtitles
        _move_additional_subtitles(destination_path, video_path)
        # Cleanup
        _cleanup(video_path)

    print "#" * 30
    logger.info("----------------------------------------------")


def _decode(value, encoding):
    # Decode a value if encoding is specified
    if encoding:
        return value.decode(encoding)
    return value


def _move(destination_path, video_path, subtitle_path):
    try:
        destination = os.path.join(destination_path)
        video = os.path.join(video_path)
        shutil.move(video, destination)
        print "Moved video to destination folder"
        logger.info("Moved video to destination folder")
        if subtitle_path:
            subtitle = os.path.join(subtitle_path)
            shutil.move(subtitle, destination)
            print "Moved subtitle to destination folder"
            logger.info("Moved subtitle to destination folder")
        return True
    except Exception, e:
        print "Exception: %s" % e
        logger.error("Exception: %s" % e)
        return False


def _move_additional_subtitles(destination_path, episode_path):
    """
    Move additional subtitles if there are any found at the same location.
    """
    try:
        path_name = os.path.splitext(os.path.normpath(episode_path))[0]
        subtitles = glob.glob(path_name + '*' + '.srt')
        if subtitles:
            destination = os.path.join(destination_path)
            for subtitle in subtitles:
                shutil.move(subtitle, destination)
                print "Moved additional subtitle to the destination folder: %s" % subtitle
                logger.info("Moved additional subtitle to the destination folder: %s" % subtitle)

    except Exception, e:
        print "Exception: %s" % e
        logger.error("Exception: %s" % e)


def _cleanup(video_path):
    """
    Cleanup leftovers.
    We need to clean up when:
    - the video is located in the autosubliminal path
    - the video is in a subfolder underneath the autosubliminal path
    """
    norm_video_path = os.path.normcase(os.path.normpath(video_path))
    in_root_folder = os.path.commonprefix([NORM_AUTOSUBLIMINAL_PATH, norm_video_path]) == NORM_AUTOSUBLIMINAL_PATH
    if in_root_folder:
        # Check if the video is in a subfolder of the root folder
        video_folder = os.path.dirname(norm_video_path)
        in_sub_folder = video_folder != NORM_AUTOSUBLIMINAL_PATH
        if in_sub_folder:
            while video_folder != NORM_AUTOSUBLIMINAL_PATH:
                folder_to_clean = video_folder
                # Move 1 folder up
                video_folder = os.path.dirname(video_folder)
            try:
                # Remove the folder of the video inside the root folder
                shutil.rmtree(folder_to_clean, onerror=_set_rw_and_remove)
                print "Removed video folder: %s" % folder_to_clean
                logger.info("Removed video folder: %s" % folder_to_clean)
            except Exception, e:
                print "Exception: %s" % e
                logger.error("Exception: %s" % e)
        else:
            print "Video is located directly under an autosubliminal video folder"
            print "Skipping cleanup"
    else:
        print "Video is not located in an autosubliminal video folder"
        print "Skipping cleanup"
        logger.info("Video is not located in an autosubliminal video folder")
        logger.info("Skipping cleanup")


def _set_rw_and_remove(operation, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


# Run the script
run()

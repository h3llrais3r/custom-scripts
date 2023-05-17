# Custom Auto-Subliminal post processing script.
# It moves a video file and (optionally) its subtitle from Auto-Subliminal to a new destination.
# CONFIGURATION: changes the values of AUTOSUBLIMINAL_PATH to your path.

# Auto-Subliminal parameters passed to the script:
# %1 - encoding
# %2 - root path
# %3 - video path
# %4 - subtitle path (optional)

# Required parameter to be specified when running the script:
# %5 - destination path

import glob
import locale
import logging
import os
import stat
import sys
import shutil

# Enable debug
DEBUG = False

# Logger config
logger = logging.getLogger('autoMoveAndCleanup')
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
log_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + '/autoMoveAndCleanup.log')
log_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')  # make sure to log in utf-8
log_formatter = logging.Formatter('%(asctime)s %(levelname)-8s - %(message)s')
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
logger.addHandler(log_handler)

# System encoding
SYS_ENCODING = locale.getpreferredencoding()

# System version
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def run():
    # Read parameters (sys.argv[0] = path to this script)
    global ENCODING
    if sys.argv[1]:
        ENCODING = sys.argv[1].lower()
    else:
        ENCODING = SYS_ENCODING.lower()

    _log_message('')
    _log_message('----------------------------------------------')
    _log_message('Running script with python version %s' % sys.version)

    # Default autosubliminal parameters
    encoding = _to_unicode(ENCODING, ENCODING)
    root_path = _to_unicode(sys.argv[2], ENCODING)
    video_path = _to_unicode(sys.argv[3], ENCODING)
    subtitle_path = _to_unicode(sys.argv[4], ENCODING)
    library_path = _to_unicode(sys.argv[5], ENCODING)

    # Required parameter
    destination_path = _to_unicode(sys.argv[6], ENCODING)

    # Log parameters
    _log_message('encoding: %s' % encoding)
    _log_message('root path: %s' % root_path)
    _log_message('video path: %s' % video_path)
    _log_message('subtitle path: %s' % subtitle_path)
    _log_message('library path: %s' % library_path)
    _log_message('destination path: %s' % destination_path)

    # Skip execution of script if video is already located in a video library path
    # If not, execute move and cleanup
    if library_path:
        _log_message('Skipping as video is already located in the video library: %s' % library_path)
    elif _move(root_path, destination_path, video_path, subtitle_path):
        # Move additional subtitles
        _move_additional_subtitles(root_path, destination_path, video_path)
        # Cleanup
        _cleanup(root_path, video_path)

    _log_message('----------------------------------------------')


def _to_unicode(value, encoding):
    # Python 2 uses byte string by default, so decode it to unicode
    if PY2:
        try:
            return value.decode(encoding)
        except Exception:
            # Use without decoding as fallback
            _log_message('Decode failed, using original value', log_level=logging.DEBUG)
            return value
    # Python 3 uses unicode string by default, so use it directly
    if PY3:
        return value


def _move(root_path, destination_path, video_path, subtitle_path):
    try:
        _log_message('Moving video to destination', log_level=logging.DEBUG)
        video = os.path.join(video_path)
        # Keep folder structure when moving to destination
        destination = os.path.join(video_path.replace(root_path, destination_path))
        _log_message('Video: %s' % video, log_level=logging.DEBUG)
        _log_message('Destination: %s' % destination, log_level=logging.DEBUG)
        shutil.move(video, destination)
        _log_message('Moved video to destination: %s' % destination)
        if subtitle_path:
            _log_message('Moving subtitle to destination', log_level=logging.DEBUG)
            subtitle = os.path.join(subtitle_path)
            # Keep folder structure when moving to destination
            destination = os.path.join(subtitle_path.replace(root_path, destination_path))
            _log_message('Subtitle: %s' % subtitle, log_level=logging.DEBUG)
            _log_message('Destination: %s' % destination, log_level=logging.DEBUG)
            shutil.move(subtitle, destination)
            _log_message('Moved subtitle to destination: %s' % destination)
        return True
    except Exception as e:
        _log_message('Error while moving files', exception=e, log_level=logging.ERROR)
        return False


def _move_additional_subtitles(root_path, destination_path, video_path):
    """
    Move additional subtitles if there are any found at the same location.
    """
    try:
        path_name = os.path.splitext(os.path.normpath(video_path))[0]
        subtitles = glob.glob(path_name + '*' + '.srt')
        if subtitles:
            _log_message('Moving additional subtitles', log_level=logging.DEBUG)
            for subtitle in subtitles:
                # Keep folder structure when moving to destination
                destination = os.path.join(subtitle.replace(root_path, destination_path))
                _log_message('Additional subtitle: %s' % subtitle, log_level=logging.DEBUG)
                _log_message('Destination: %s' % destination, log_level=logging.DEBUG)
                shutil.move(subtitle, destination)
                _log_message('Moved additional found subtitle to destination: %s' % destination)
    except Exception as e:
        _log_message('Error while moving additional subtitles', exception=e, log_level=logging.ERROR)


def _cleanup(root_path, video_path):
    """
    Cleanup leftovers.
    We need to clean up when:
    - the video is located in the root path
    - the video is in a sub folder underneath the root path
    """
    _log_message('Cleaning up leftovers', log_level=logging.DEBUG)
    norm_root_path = _norm_path(root_path)
    norm_video_path = _norm_path(video_path)
    in_root_folder = _get_common_path([norm_root_path, norm_video_path]) == norm_root_path
    _log_message('In root folder: %s' % in_root_folder, log_level=logging.DEBUG)
    if in_root_folder:
        # Check if the video is in a sub folder of the root folder
        # Only compare _norm_path values to prevent a possible endless loop with difference in trailing slashes!
        video_folder = _norm_path(os.path.dirname(norm_video_path))
        in_sub_folder = video_folder != norm_root_path
        if in_sub_folder:
            folder_to_clean = None
            while video_folder != norm_root_path:
                folder_to_clean = video_folder
                # Move 1 folder up
                video_folder = _norm_path(os.path.dirname(video_folder))
            try:
                # Check if the folder to clean does not contain other video files before cleaning up
                video_files_found = False
                _, ext = os.path.splitext(norm_video_path)
                _log_message('Checking for other video files before cleaning up', log_level=logging.DEBUG)
                for dirname, dirnames, filenames in os.walk(folder_to_clean):
                    for filename in filenames:
                        norm_file_path = _norm_path(os.path.join(dirname, filename))
                        _log_message('Checking file: %s' % norm_file_path, log_level=logging.DEBUG)
                        byte_size = os.path.getsize(os.path.join(dirname, filename))
                         # Only consider video files > 50 MB that are not the file we are processing
                        if norm_video_path != norm_file_path and filename.endswith(ext) and byte_size > (50 * 1024 * 1024):
                            _log_message('File detected as video file', log_level=logging.DEBUG)
                            video_files_found = True
                if video_files_found:
                    # Skip if other video files are found
                    _log_message('Other video files found in video folder')
                    _log_message('Skipping cleanup')
                else:
                     # Remove the folder of the video inside the root folder
                    _log_message('No other video files found in video folder')
                    _log_message('Cleaning up video folder: %s' % folder_to_clean, log_level=logging.DEBUG)
                    shutil.rmtree(folder_to_clean, onerror=_set_rw_and_remove)
                    _log_message('Removed video folder: %s' % folder_to_clean)
            except Exception as e:
                _log_message('Error while cleaning up video folder', e, logging.ERROR)
        else:
            _log_message('Video is located directly under a root folder')
            _log_message('Skipping cleanup')
    else:
        _log_message('Video is not located in a root folder')
        _log_message('Skipping cleanup')


def _log_message(message, exception=None, log_level=logging.INFO):
    # Print message to standard output
    _print(message, log_level)
    if exception:
        _print('Please check %s for details' % log_file, log_level)
    # Log message
    if exception:
        logger.exception(message)  # This will also print the traceback
    else:
        logger.log(log_level, message)


def _print(message, log_level):
    """
    Print the message.
    Printing should be done with the native string.
    For PY2: encode unicode back to native string with the provided encoding
    For PY3: convert unicode string with provided encoding to string in system encoding
    """
    # Add prefix in debug mode
    if DEBUG and log_level == logging.DEBUG:
        message = 'DEBUG - ' + message
    # Only print message according to log level
    if log_level >= logger.level:
        try:
            if PY2:
                # Encode unicode back to native string with the provided encoding
                print(message.encode(ENCODING))
            if PY3:
                # Convert unicode string with provided encoding to string in system encoding
                print(message.encode(ENCODING).decode(SYS_ENCODING))
        except Exception:
            # This should not occur, but let's try to print anyway with fallback to utf-8
            try:
                print(message.encode('utf-8').decode(SYS_ENCODING))
            except Exception:
                try:
                    print(message.encode('utf-8', errors='replace'))
                except Exception:
                    print(message.encode('utf-8', errors='ignore'))


def _norm_path(path):
    # This only affects case insensitive systems (like Windows)
    norm_path = os.path.normcase(os.path.normpath(path))
    # Make sure to strip trailing os.path.sep characters because we'll be comparing paths
    return norm_path.rstrip(os.path.sep)


def _get_common_path(paths):
    # See https://stackoverflow.com/questions/21498939/how-to-circumvent-the-fallacy-of-pythons-os-path-commonprefix
    # This unlike the os.path.commonprefix version always returns path prefixes as it compares path component wise
    cp = []

    ls = [p.split(os.path.sep) for p in paths]
    ml = min(len(p) for p in ls)
    for i in range(ml):
        s = set(p[i] for p in ls)
        if len(s) != 1:
            break
        cp.append(s.pop())

    return os.path.sep.join(cp) if cp else None


def _set_rw_and_remove(operation, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


# Run the script
run()

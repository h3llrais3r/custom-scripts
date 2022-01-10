import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Variables (from https://wiki.servarr.com/sonarr/custom-scripts)

# Sonarr variables for On Grab
sonarr_eventtype = os.environ.get('sonarr_eventtype') # Grab
sonarr_series_id = os.environ.get('sonarr_series_id') # Internal ID of the series
sonarr_series_title = os.environ.get('sonarr_series_title') # Title of the series
sonarr_series_tvdbid = os.environ.get('sonarr_series_tvdbid') # TVDB ID for the series
sonarr_series_tvmazeid = os.environ.get('sonarr_series_tvmazeid') # TVMaze ID for the series
sonarr_series_imdbid = os.environ.get('sonarr_series_imdbid') # IMDB ID for the series (empty if unknown)
sonarr_series_type = os.environ.get('sonarr_series_type') # Type of the series (Anime, Daily, or Standard)
sonarr_release_episodecount = os.environ.get('sonarr_release_episodecount') # Number of episodes in the release
sonarr_release_seasonnumber = os.environ.get('sonarr_release_seasonnumber') # Season number from release
sonarr_release_episodenumbers = os.environ.get('sonarr_release_episodenumbers') # Comma-delimited list of episode numbers
sonarr_release_absoluteepisodenumbers = os.environ.get('sonarr_release_absoluteepisodenumbers') # Comma-delimited list of absolute episode numbers
sonarr_release_episodeairdates = os.environ.get('sonarr_release_episodeairdates') # Comma-delimited list of air dates from original network
sonarr_release_episodeairdatesutc = os.environ.get('sonarr_release_episodeairdatesutc') # Comma-delimited list of air dates in UTC
sonarr_release_episodetitles = os.environ.get('sonarr_release_episodetitles') # \|-delimited list of episode titles
sonarr_release_title = os.environ.get('sonarr_release_title') # Torrent/NZB title
sonarr_release_indexer = os.environ.get('sonarr_release_indexer') # Indexer from which the release was grabbed
sonarr_release_size = os.environ.get('sonarr_release_size') # Size of the release, as reported by the indexer
sonarr_release_quality = os.environ.get('sonarr_release_quality') # Quality name of the release, as detected by Sonarr
sonarr_release_qualityversion = os.environ.get('sonarr_release_qualityversion') # 1 is the default, 2 is for proper, and 3+ could be used for anime versions
sonarr_release_releasegroup = os.environ.get('sonarr_release_releasegroup') # Release group (empty if unknown)
sonarr_download_client = os.environ.get('sonarr_download_client') # Download client
sonarr_download_id = os.environ.get('sonarr_download_id') # Hash of the torrent/NZB file (used to uniquely identify the download in the download client)

# Sonarr variables for On Import/On Upgrade
sonarr_eventtype = os.environ.get('sonarr_eventtype') # Download
sonarr_isupgrade = os.environ.get('sonarr_isupgrade') # True when an existing file is upgraded, False otherwise
sonarr_series_id = os.environ.get('sonarr_series_id') # Internal ID of the series
sonarr_series_title = os.environ.get('sonarr_series_title') # Title of the series
sonarr_series_path = os.environ.get('sonarr_series_path') # Full path to the series
sonarr_series_tvdbid = os.environ.get('sonarr_series_tvdbid') # TVDB ID for the series
sonarr_series_tvmazeid = os.environ.get('sonarr_series_tvmazeid') # TVMaze ID for the series
sonarr_series_imdbid = os.environ.get('sonarr_series_imdbid') # IMDB ID for the series (empty if unknown)
sonarr_series_type = os.environ.get('sonarr_series_type') # Type of the series (Anime, Daily, or Standard)
sonarr_episodefile_id = os.environ.get('sonarr_episodefile_id') # Internal ID of the episode file
sonarr_episodefile_episodecount = os.environ.get('sonarr_episodefile_episodecount') # Number of episodes in the file
sonarr_episodefile_relativepath = os.environ.get('sonarr_episodefile_relativepath') # Path to the episode file, relative to the series path
sonarr_episodefile_path = os.environ.get('sonarr_episodefile_path') # Full path to the episode file
sonarr_episodefile_episodeids = os.environ.get('sonarr_episodefile_episodeids') # Internal ID(s) of the episode file
sonarr_episodefile_seasonnumber = os.environ.get('sonarr_episodefile_seasonnumber') # Season number of episode file
sonarr_episodefile_episodenumbers = os.environ.get('sonarr_episodefile_episodenumbers') # Comma-delimited list of episode numbers
sonarr_episodefile_episodeairdates = os.environ.get('sonarr_episodefile_episodeairdates') # Comma-delimited list of air dates from original network
sonarr_episodefile_episodeairdatesutc = os.environ.get('sonarr_episodefile_episodeairdatesutc') # Comma-delimited list of air dates in UTC
sonarr_episodefile_episodetitles = os.environ.get('sonarr_episodefile_episodetitles') # \|-delimited list of episode titles
sonarr_episodefile_quality = os.environ.get('sonarr_episodefile_quality') # Quality name of the episode file, as detected by Sonarr
sonarr_episodefile_qualityversion = os.environ.get('sonarr_episodefile_qualityversion') # 1 is the default, 2 is for proper, and 3+ could be used for anime versions
sonarr_episodefile_releasegroup = os.environ.get('sonarr_episodefile_releasegroup') # Release group (empty if unknown)
sonarr_episodefile_scenename = os.environ.get('sonarr_episodefile_scenename') # Original release name (empty if unknown)
sonarr_episodefile_sourcepath = os.environ.get('sonarr_episodefile_sourcepath') # Full path to the imported episode file
sonarr_episodefile_sourcefolder = os.environ.get('sonarr_episodefile_sourcefolder') # Full path to the folder the episode file was imported from
sonarr_download_client = os.environ.get('sonarr_download_client') # Download client
sonarr_download_id = os.environ.get('sonarr_download_id') # Hash of the torrent/NZB file (used to uniquely identify the download in the download client)
sonarr_deletedrelativepaths = os.environ.get('sonarr_deletedrelativepaths') # \|-delimited list of files that were deleted to import this file
sonarr_deletedpaths = os.environ.get('sonarr_deletedpaths') # \|-delimited list of full paths of files that were deleted to import this file

# Sonarr variables for On Rename
sonarr_eventtype = os.environ.get('') # Rename
sonarr_series_id = os.environ.get('') # Internal ID of the series
sonarr_series_title = os.environ.get('') # Title of the series
sonarr_series_path = os.environ.get('') # Full path to the series
sonarr_series_tvdbid = os.environ.get('') # TVDB ID for the series
sonarr_series_tvmazeid = os.environ.get('') # TVMaze ID for the series
sonarr_series_imdbid = os.environ.get('') # IMDB ID for the series (empty if unknown)
sonarr_series_type = os.environ.get('') # Type of the series (Anime, Daily, or Standard)

# Sonarr variables for On Episode File Delete
sonarr_eventtype = os.environ.get('sonarr_eventtype') # EpisodeFileDelete
sonarr_series_id = os.environ.get('sonarr_series_id') # Internal ID of the series
sonarr_series_title = os.environ.get('sonarr_series_title') # Title of the series
sonarr_series_path = os.environ.get('sonarr_series_path') # Full path to the series
sonarr_series_tvdbid = os.environ.get('sonarr_series_tvdbid') # TVDB ID for the series
sonarr_series_tvmazeid = os.environ.get('sonarr_series_tvmazeid') # TVMaze ID for the series
sonarr_series_imdbid = os.environ.get('sonarr_series_imdbid') # IMDB ID for the series (empty if unknown)
sonarr_series_type = os.environ.get('sonarr_series_type') # Type of the series (Anime, Daily, or Standard)
sonarr_episodefile_id = os.environ.get('sonarr_episodefile_id') # Internal ID of the episode file
sonarr_episodefile_episodecount = os.environ.get('sonarr_episodefile_episodecount') # Number of episodes in the file
sonarr_episodefile_relativepath = os.environ.get('sonarr_episodefile_relativepath') # Path to the episode file, relative to the series' path
sonarr_episodefile_path = os.environ.get('sonarr_episodefile_path') # Full path to the episode file
sonarr_episodefile_episodeids = os.environ.get('sonarr_episodefile_episodeids') # Internal ID(s) of the episode file
sonarr_episodefile_seasonnumber = os.environ.get('sonarr_episodefile_seasonnumber') # Season number of episode file
sonarr_episodefile_episodenumbers = os.environ.get('sonarr_episodefile_episodenumbers') # Comma-delimited list of episode numbers
sonarr_episodefile_episodeairdates = os.environ.get('sonarr_episodefile_episodeairdates') # Comma-delimited list of air dates from original network
sonarr_episodefile_episodeairdatesutc = os.environ.get('sonarr_episodefile_episodeairdatesutc') # Comma-delimited list of air dates in UTC
sonarr_episodefile_episodetitles = os.environ.get('sonarr_episodefile_episodetitles') # \|-delimited list of episode titles
sonarr_episodefile_quality = os.environ.get('sonarr_episodefile_quality') # Quality name of the episode file, as detected by Sonarr
sonarr_episodefile_qualityversion = os.environ.get('sonarr_episodefile_qualityversion') # 1 is the default, 2 is for proper, and 3+ could be used for anime versions
sonarr_episodefile_releasegroup = os.environ.get('sonarr_episodefile_releasegroup') # Release group (empty if unknown)
sonarr_episodefile_scenename = os.environ.get('sonarr_episodefile_scenename') # Original release name (empty if unknown)

# Sonarr variables for On Series Delete
sonarr_eventtype = os.environ.get('sonarr_eventtype') # SeriesDelete
sonarr_series_id = os.environ.get('sonarr_series_id') # Internal ID of the series
sonarr_series_title = os.environ.get('sonarr_series_title') # Title of the series
sonarr_series_path = os.environ.get('sonarr_series_path') # Full path to the series
sonarr_series_tvdbid = os.environ.get('sonarr_series_tvdbid') # TVDB ID for the series
sonarr_series_imdbid = os.environ.get('sonarr_series_imdbid') # IMDB ID for the series (empty if unknown)
sonarr_series_type = os.environ.get('sonarr_series_type') # Type of the series (Anime, Daily, or Standard)
sonarr_series_deletedfiles = os.environ.get('sonarr_series_deletedfiles') # True when the delete files option has been selected, otherwise False

# Sonarr variables for On Health Issue
sonarr_eventype = os.environ.get('sonarr_eventype') # HealthIssue
sonarr_health_issue_level = os.environ.get('sonarr_health_issue_level') # Type of health issue (Ok, Notice, Warning, or Error)
sonarr_health_issue_message = os.environ.get('sonarr_health_issue_message') # Message from the health issue
sonarr_health_issue_type = os.environ.get('sonarr_health_issue_type') # Area that failed and triggered the health issue
sonarr_health_issue_wiki = os.environ.get('sonarr_health_issue_wiki') # Wiki URL (empty if does not exist)

# Sonarr variables for On Test
sonarr_eventtype = os.environ.get('sonarr_eventtype') # Test

# Custom variables
if sonarr_eventtype == 'Grab':
    series_details = f'S{sonarr_release_seasonnumber.zfill(2)}' + 'E' + '-'.join([f'{x.zfill(2)}' for x in sonarr_release_episodenumbers.split(',')])
    subject = f'Sonarr - Grabbed {sonarr_series_title} {series_details}'
    content = f'''
    Type: {sonarr_series_type}
    Title: {sonarr_series_title}
    Season: {sonarr_release_seasonnumber}
    Episode(s): {sonarr_release_episodenumbers}
    Imdbid: {sonarr_series_imdbid} (https://www.imdb.com/title/{sonarr_series_imdbid})
    Tvdbid: {sonarr_series_tvdbid} (https://thetvdb.com?tab=series&id={sonarr_series_tvdbid})
    Tvmazeid: {sonarr_series_tvmazeid} (https://www.tvmaze.com/shows/{sonarr_series_tvmazeid})
    Download client: {sonarr_download_client}
    Download id: {sonarr_download_id}
    Indexer: {sonarr_release_indexer}
    Quality: {sonarr_release_quality}
    '''
elif sonarr_eventtype == 'Download':
    event_action = 'Upgraded' if sonarr_isupgrade == 'True' else 'Downloaded'
    series_details = f'S{sonarr_episodefile_seasonnumber.zfill(2)}' + 'E' + '-'.join([f'{x.zfill(2)}' for x in sonarr_episodefile_episodenumbers.split(',')])
    original_filename = os.path.basename(sonarr_episodefile_sourcepath) if sonarr_episodefile_sourcepath else ''
    subject = f'Sonarr - {event_action} {sonarr_series_title} {series_details} - {sonarr_episodefile_quality}'
    content = f'''
    Type: {sonarr_series_type}
    Title: {sonarr_series_title}
    Season: {sonarr_episodefile_seasonnumber}
    Episode(s): {sonarr_episodefile_episodenumbers}
    Imdbid: {sonarr_series_imdbid} (https://www.imdb.com/title/{sonarr_series_imdbid})
    Tvdbid: {sonarr_series_tvdbid} (https://thetvdb.com?tab=series&id={sonarr_series_tvdbid})
    Tvmazeid: {sonarr_series_tvmazeid} (https://www.tvmaze.com/shows/{sonarr_series_tvmazeid})
    Quality: {sonarr_episodefile_quality}
    Download client: {sonarr_download_client}
    Download id: {sonarr_download_id}
    Path: {sonarr_series_path}
    File: {sonarr_episodefile_path}
    Original file: {original_filename}
    '''
elif sonarr_eventtype == 'Rename':
    subject = f'Sonarr - Renamed {sonarr_series_title}'
    content = f'''
    Type: {sonarr_series_type}
    Title: {sonarr_series_title}
    Imdbid: {sonarr_series_imdbid} (https://www.imdb.com/title/{sonarr_series_imdbid})
    Tvdbid: {sonarr_series_tvdbid} (https://thetvdb.com?tab=series&id={sonarr_series_tvdbid})
    Tvmazeid: {sonarr_series_tvmazeid} (https://www.tvmaze.com/shows/{sonarr_series_tvmazeid})
    Path: {sonarr_series_path}
    '''
elif sonarr_eventtype == 'EpisodeFileDelete':
    series_details = f'S{sonarr_episodefile_seasonnumber.zfill(2)}' + 'E' + '-'.join([f'{x.zfill(2)}' for x in sonarr_episodefile_episodenumbers.split(',')])
    subject = f'Sonarr - Deleted episode {sonarr_series_title} {series_details}'
    content = f'''
    Type: {sonarr_series_type}
    Title: {sonarr_series_title}
    Season: {sonarr_episodefile_seasonnumber}
    Episode(s): {sonarr_episodefile_episodenumbers}
    Imdbid: {sonarr_series_imdbid} (https://www.imdb.com/title/{sonarr_series_imdbid})
    Tvdbid: {sonarr_series_tvdbid} (https://thetvdb.com?tab=series&id={sonarr_series_tvdbid})
    Tvmazeid: {sonarr_series_tvmazeid} (https://www.tvmaze.com/shows/{sonarr_series_tvmazeid})
    Path: {sonarr_series_path}
    File: {sonarr_episodefile_path}
    '''
elif sonarr_eventtype == 'SeriesDelete':
    subject = f'Sonarr - Deleted {sonarr_series_title}'
    content = f'''
    Type: {sonarr_series_type}
    Title: {sonarr_series_title}
    Imdbid: {sonarr_series_imdbid} (https://www.imdb.com/title/{sonarr_series_imdbid})
    Tvdbid: {sonarr_series_tvdbid} (https://thetvdb.com?tab=series&id={sonarr_series_tvdbid})
    Tvmazeid: {sonarr_series_tvmazeid} (https://www.tvmaze.com/shows/{sonarr_series_tvmazeid})
    Path: {sonarr_series_path}
    '''
elif sonarr_eventtype == 'HealthIssue':
    subject = f'Sonarr - Health issue'
    content = f'''
    Level: {sonarr_health_issue_level}
    Message: {sonarr_health_issue_message}
    Type: {sonarr_health_issue_type}
    Wiki: {sonarr_health_issue_wiki}
    '''
elif sonarr_eventtype == 'Test':
    subject = 'Sonarr - Test message'
    content = ''
else:
    subject = f'Sonarr - Unknown event - {sonarr_eventtype}'
    content = ''

# Mail variables
mail_host = 'smtp.gmail.com'
mail_port = 587
mail_sender_address = 'xxx@gmail.com'
mail_sender_pass = 'xxx'
mail_receiver_address = 'xxx@gmail.com'

# Setup message
message = MIMEMultipart()
message['From'] = mail_sender_address
message['To'] = mail_receiver_address
message['Subject'] = subject
message.attach(MIMEText('\n'.join([l.lstrip() for l in content.split('\n')]), 'plain')) # Trim all leading spaces from multiline format

# Send mail
session = smtplib.SMTP(mail_host, mail_port)
session.starttls() # enable security
session.login(mail_sender_address, mail_sender_pass)
session.sendmail(mail_sender_address, mail_receiver_address, message.as_string())
session.quit()

print(f'Gmail notification sent: {subject}')
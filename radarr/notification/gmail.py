import os
import smtplib
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Read config file if present
config = ConfigParser()
if os.path.exists(os.path.join(os.path.dirname(__file__), "..", "..", "common", "config.ini")):
    config.read()

# Variables (from https://wiki.servarr.com/radarr/custom-scripts)

# Radarr variables for On Grab
radarr_eventtype = os.environ.get('radarr_eventtype') # Grab
radarr_download_client = os.environ.get('radarr_download_client') # Download client (empty if unknown)
radarr_download_id = os.environ.get('radarr_download_id') # Hash of the torrent/NZB file (used to uniquely identify the download in the download client)
radarr_movie_id = os.environ.get('radarr_movie_id') # Internal ID of the movie
radarr_movie_imdbid = os.environ.get('radarr_movie_imdbid') # IMDb ID for the movie (empty if unknown)
radarr_movie_in_cinemas_date = os.environ.get('radarr_movie_in_cinemas_date') # Cinema release date (empty if unknown)
radarr_movie_physical_release_date = os.environ.get('radarr_movie_physical_release_date') # Physical release date (empty if unknown)
radarr_movie_title = os.environ.get('radarr_movie_title') # Title of the movie
radarr_movie_tmdbid = os.environ.get('radarr_movie_tmdbid') # TMDb ID for the movie
radarr_movie_year = os.environ.get('radarr_movie_year') # Release year of the movie
radarr_release_indexer = os.environ.get('radarr_release_indexer') # Indexer from which the release was grabbed
radarr_release_quality = os.environ.get('radarr_release_quality') # Quality name of the release, as detected by Radarr
radarr_release_qualityversion = os.environ.get('radarr_release_qualityversion') # 1 is the default, 2 is for proper, and 3+ could be used for anime versions
radarr_release_releasegroup = os.environ.get('radarr_release_releasegroup') # Release group (empty if unknown)
radarr_release_size = os.environ.get('radarr_release_size') # Size of the release, as reported by the indexer
radarr_release_title = os.environ.get('radarr_release_title') # Torrent/NZB title

# Radarr variables for On Import/On Upgrade
radarr_eventtype = os.environ.get('radarr_eventtype') # Download
radarr_download_id = os.environ.get('radarr_download_id') # Hash of the torrent/NZB file (used to uniquely identify the download in the download client)
radarr_download_client = os.environ.get('radarr_download_client') # Download client
radarr_isupgrade = os.environ.get('radarr_isupgrade') # True when an existing file is upgraded, False otherwise
radarr_movie_id = os.environ.get('radarr_movie_id') # Internal ID of the movie
radarr_movie_imdbid = os.environ.get('radarr_movie_imdbid') # IMDb ID for the movie (empty if unknown)
radarr_movie_in_cinemas_date = os.environ.get('radarr_movie_in_cinemas_date') # Cinema release date (empty if unknown)
radarr_movie_path = os.environ.get('radarr_movie_path') # Full path to the movie
radarr_movie_physical_release_date = os.environ.get('radarr_movie_physical_release_date') # Physical release date (empty if unknown)
radarr_movie_title = os.environ.get('radarr_movie_title') # Title of the movie
radarr_movie_tmdbid = os.environ.get('radarr_movie_tmdbid') # TMDb ID for the movie
radarr_movie_year = os.environ.get('radarr_movie_year') # Release year of the movie
radarr_moviefile_id = os.environ.get('radarr_moviefile_id') # Internal ID of the movie file
radarr_moviefile_relativepath = os.environ.get('radarr_moviefile_relativepath') # Path to the movie file, relative to the movie path
radarr_moviefile_path = os.environ.get('radarr_moviefile_path') # Full path to the movie file
radarr_moviefile_quality = os.environ.get('radarr_moviefile_quality') # Quality name of the release, as detected by Radarr
radarr_moviefile_qualityversion = os.environ.get('radarr_moviefile_qualityversion') # 1 is the default, 2 is for proper, and 3+ could be used for anime versions
radarr_moviefile_releasegroup = os.environ.get('radarr_moviefile_releasegroup') # Release group (empty if unknown)
radarr_moviefile_scenename = os.environ.get('radarr_moviefile_scenename') # Original release name (empty if unknown)
radarr_moviefile_sourcepath = os.environ.get('radarr_moviefile_sourcepath') # Full path to the imported movie file
radarr_moviefile_sourcefolder = os.environ.get('radarr_moviefile_sourcefolder') # Full path to the folder the movie file was imported from
radarr_deletedrelativepaths = os.environ.get('radarr_deletedrelativepaths') # |-delimited list of files that were deleted to import this file
radarr_deletedpaths = os.environ.get('radarr_deletedpaths') # |-delimited list of full paths to files that were deleted to import this file

# Radarr variables for On Rename
radarr_eventtype = os.environ.get('radarr_eventtype') # Rename
radarr_movie_id = os.environ.get('radarr_movie_id') # Internal ID of the movie
radarr_movie_title = os.environ.get('radarr_movie_title') # Title of the movie
radarr_movie_year = os.environ.get('radarr_movie_year') # Release year of the movie
radarr_movie_path = os.environ.get('radarr_movie_path') # Full path to the movie
radarr_movie_imdbid = os.environ.get('radarr_movie_imdbid') # IMDb ID for the movie (empty if unknown)
radarr_movie_tmdbid = os.environ.get('radarr_movie_tmdbid') # TMDb ID for the movie
radarr_movie_in_cinemas_date = os.environ.get('radarr_movie_in_cinemas_date') # Cinema release date (empty if unknown)
radarr_movie_physical_release_date = os.environ.get('radarr_movie_physical_release_date') # Physical/Web release date (empty if unknown)
radarr_moviefile_ids = os.environ.get('radarr_moviefile_ids') # ,-delimited list of file ID(s)
radarr_moviefile_relativepaths = os.environ.get('radarr_moviefile_relativepaths') # |-delimited list of relative path(s)
radarr_moviefile_paths = os.environ.get('radarr_moviefile_paths') # |-delimited list of path(s)
radarr_moviefile_previousrelativepaths = os.environ.get('radarr_moviefile_previousrelativepaths') # |-delimited list of previous relative path(s)
radarr_moviefile_previouspaths = os.environ.get('radarr_moviefile_previouspaths') # |-delimited list of previous path(s)

# Radarr variables for On Movie Delete
radarr_eventtype = os.environ.get('radarr_eventtype') # MovieDelete
radarr_movie_id = os.environ.get('radarr_movie_id') # Internal ID of the movie
radarr_movie_title = os.environ.get('radarr_movie_title') # Title of the movie
radarr_movie_year = os.environ.get('radarr_movie_year') # Release year of the movie
radarr_movie_path = os.environ.get('radarr_movie_path') # Full path to the movie
radarr_movie_imdbid = os.environ.get('radarr_movie_imdbid') # IMDb ID for the movie (empty if unknown)
radarr_movie_tmdbid = os.environ.get('radarr_movie_tmdbid') # TMDb ID for the movie
# TODO: update variables once they are available in wiki

# Radarr variables for On Health Issue
radarr_eventype = os.environ.get('radarr_eventtype') # HealthIssue
radarr_health_issue_level = os.environ.get('radarr_health_issue_level') # Type of health issue (Ok, Notice, Warning, or Error)
radarr_health_issue_message = os.environ.get('radarr_health_issue_message') # Message from the health issue
radarr_health_issue_type = os.environ.get('radarr_health_issue_type') # Area that failed and triggered the health issue
radarr_health_issue_wiki = os.environ.get('radarr_health_issue_wiki') # Wiki URL (empty if does not exist)

# Radarr variables for On Application Update
radarr_eventype = os.environ.get('radarr_eventtype') # ApplicationUpdate
radarr_update_message = os.environ.get('radarr_update_message') # Message from Update
radarr_update_newversion = os.environ.get('radarr_update_newversion') # Version Radarr updated to (string)
radarr_update_previousversion = os.environ.get('radarr_update_previousversion') # Version Radarr updated from (string)

# Radarr variables for On Test
radarr_eventype = os.environ.get('radarr_eventtype') # Test

# Custom variables
if radarr_eventtype == 'Grab':
    subject = f'Radarr - Grabbed {radarr_movie_title} ({radarr_movie_year})'
    content = f'''
    Title: {radarr_movie_title}
    Year: {radarr_movie_year}
    Imdbid: {radarr_movie_imdbid} (https://www.imdb.com/title/{radarr_movie_imdbid})
    Tmdbid: {radarr_movie_tmdbid} (https://www.themoviedb.org/movie/{radarr_movie_tmdbid})
    Download client: {radarr_download_client}
    Download id: {radarr_download_id}
    Indexer: {radarr_release_indexer}
    Quality: {radarr_release_quality}
    '''
elif radarr_eventtype == 'Download':
    event_action = 'Upgraded' if radarr_isupgrade == 'True' else 'Downloaded'
    original_filename = os.path.basename(radarr_moviefile_sourcepath) if radarr_moviefile_sourcepath else ''
    subject = f'Radarr - {event_action} {radarr_movie_title} ({radarr_movie_year}) - {radarr_moviefile_quality}'
    content = f'''
    Title: {radarr_movie_title}
    Year: {radarr_movie_year}
    Imdbid: {radarr_movie_imdbid} (https://www.imdb.com/title/{radarr_movie_imdbid})
    Tmdbid: {radarr_movie_tmdbid} (https://www.themoviedb.org/movie/{radarr_movie_tmdbid})
    Quality: {radarr_moviefile_quality}
    Download client: {radarr_download_client}
    Download id: {radarr_download_id}
    Path: {radarr_movie_path}
    File: {radarr_moviefile_path}
    Original file: {original_filename}
    '''
elif radarr_eventtype == 'Rename':
    subject = f'Radarr - Renamed {radarr_movie_title} ({radarr_movie_year})'
    content = f'''
    Title: {radarr_movie_title}
    Year: {radarr_movie_year}
    Imdbid: {radarr_movie_imdbid} (https://www.imdb.com/title/{radarr_movie_imdbid})
    Tmdbid: {radarr_movie_tmdbid} (https://www.themoviedb.org/movie/{radarr_movie_tmdbid})
    Path: {radarr_movie_path}
    '''
elif radarr_eventtype == 'MovieDelete':
    subject = f'Radarr - Deleted {radarr_movie_title} ({radarr_movie_year})'
    content = f'''
    Title: {radarr_movie_title}
    Year: {radarr_movie_year}
    Imdbid: {radarr_movie_imdbid} (https://www.imdb.com/title/{radarr_movie_imdbid})
    Tmdbid: {radarr_movie_tmdbid} (https://www.themoviedb.org/movie/{radarr_movie_tmdbid})
    Path: {radarr_movie_path}
    '''
elif radarr_eventtype == 'HealthIssue':
    subject = f'Radarr - Health issue'
    content = f'''
    Level: {radarr_health_issue_level}
    Message: {radarr_health_issue_message}
    Type: {radarr_health_issue_type}
    Wiki: {radarr_health_issue_wiki}
    '''
elif radarr_eventtype == 'ApplicationUpdate':
    subject = f'Radarr - Application update'
    content = f'''
    Message: {radarr_update_message}
    New version: {radarr_update_newversion}
    Previous version: {radarr_update_previousversion}
    '''
elif radarr_eventtype == 'Test':
    subject = 'Radarr - Test message'
    content = ''
else:
    subject = f'Radarr - Unknown event - {radarr_eventtype}'
    content = ''

# Mail variables
mail_host = config.get('mail_host') or 'smtp.gmail.com'
mail_port = config.getint('mail_port') or 587
mail_sender_address = config.get('mail_sender_address') or 'xxx@gmail.com'
mail_sender_pass = config.get('mail_sender_pass') or 'xxx'
mail_receiver_address = config.get('mail_receiver_address') or 'xxx@gmail.com'

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
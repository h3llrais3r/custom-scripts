import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Radarr variables (from https://wiki.servarr.com/radarr/custom-scripts)
radarr_eventtype = os.environ.get('radarr_eventtype') or '' # Download
radarr_download_id = os.environ.get('radarr_download_id') or '' # Hash of the torrent/NZB file (used to uniquely identify the download in the download client)
radarr_download_client = os.environ.get('radarr_download_client') or '' # Download client
radarr_isupgrade = os.environ.get('radarr_isupgrade') or '' # True when an existing file is upgraded, False otherwise
radarr_movie_id = os.environ.get('radarr_movie_id') or '' # Internal ID of the movie
radarr_movie_imdbid = os.environ.get('radarr_movie_imdbid') or '' # IMDb ID for the movie (empty if unknown)
radarr_movie_in_cinemas_date = os.environ.get('radarr_movie_in_cinemas_date') or '' # Cinema release date (empty if unknown)
radarr_movie_path = os.environ.get('radarr_movie_path') or '' # Full path to the movie
radarr_movie_physical_release_date = os.environ.get('radarr_movie_physical_release_date') or '' # Physical release date (empty if unknown)
radarr_movie_title = os.environ.get('radarr_movie_title') or '' # Title of the movie
radarr_movie_tmdbid = os.environ.get('radarr_movie_tmdbid') or '' # TMDb ID for the movie
radarr_movie_year = os.environ.get('radarr_movie_year') or '' # Release year of the movie
radarr_moviefile_id = os.environ.get('radarr_moviefile_id') or '' # Internal ID of the movie file
radarr_moviefile_relativepath = os.environ.get('radarr_moviefile_relativepath') or '' # Path to the movie file, relative to the movie path
radarr_moviefile_path = os.environ.get('radarr_moviefile_path') or '' # Full path to the movie file
radarr_moviefile_quality = os.environ.get('radarr_moviefile_quality') or '' # Quality name of the release, as detected by Radarr
radarr_moviefile_qualityversion = os.environ.get('radarr_moviefile_qualityversion') or '' # 1 is the default, 2 is for proper, and 3+ could be used for anime versions
radarr_moviefile_releasegroup = os.environ.get('radarr_moviefile_releasegroup') or '' # Release group (empty if unknown)
radarr_moviefile_scenename = os.environ.get('radarr_moviefile_scenename') or '' # Original release name (empty if unknown)
radarr_moviefile_sourcepath = os.environ.get('radarr_moviefile_sourcepath') or '' # Full path to the imported movie file
radarr_moviefile_sourcefolder = os.environ.get('radarr_moviefile_sourcefolder') or '' # Full path to the folder the movie file was imported from
radarr_deletedrelativepaths = os.environ.get('radarr_deletedrelativepaths') or '' # |-delimited list of files that were deleted to import this file
radarr_deletedpaths = os.environ.get('radarr_deletedpaths') or '' # |-delimited list of full paths to files that were deleted to import this file

# Custom variables
test_message = radarr_eventtype == 'Test'
action = 'Upgraded' if radarr_isupgrade == 'True' else 'Downloaded'
original_filename = os.path.basename(radarr_moviefile_sourcepath) if radarr_moviefile_sourcepath else ''

# Mail variables
mail_host = 'smtp.gmail.com'
mail_port = 587
mail_sender_address = 'xxx@gmail.com'
mail_sender_pass = 'xxx'
mail_receiver_address = 'xxx@gmail.com'
mail_subject = f'Radarr - {action} {radarr_movie_title} ({radarr_movie_year}) - {radarr_moviefile_quality}'
mail_subject_test = 'Radarr - Test notification'
mail_content = f'''
Title: {radarr_movie_title}
Year: {radarr_movie_year}
Imdbid: {radarr_movie_imdbid} https://www.imdb.com/title/{radarr_movie_imdbid}
Tmdbid: {radarr_movie_tmdbid} https://www.themoviedb.org/movie/{radarr_movie_tmdbid}
Quality: {radarr_moviefile_quality}
Download client: {radarr_download_client}
Download id: {radarr_download_id}
Path: {radarr_movie_path}
File: {radarr_moviefile_path}
Original file: {original_filename}
'''

# Setup message
message = MIMEMultipart()
message['From'] = mail_sender_address
message['To'] = mail_receiver_address
message['Subject'] = mail_subject
message.attach(MIMEText('Test' if test_message else mail_content, 'plain'))

# Send mail
session = smtplib.SMTP(mail_host, mail_port)
session.starttls() # enable security
session.login(mail_sender_address, mail_sender_pass)
session.sendmail(mail_sender_address, mail_receiver_address, message.as_string())
session.quit()

print(f'Gmail notification sent: {mail_subject}')
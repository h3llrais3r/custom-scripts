import os
import smtplib
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

# Read config file if present
config = ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), "..", "..", "common", "config.ini")
if os.path.exists(config_file):
    config.read(config_file)

# Variables (from https://wiki.servarr.com/lidarr/custom-scripts)

# Lidarr variables for On Grab
Lidarr_EventType = os.environ.get('Lidarr_EventType') # Grab
Lidarr_Artist_Id = os.environ.get('Lidarr_Artist_Id') # artist.Id
Lidarr_Artist_Name = os.environ.get('Lidarr_Artist_Name') # artist.Metadata.Value.Name
Lidarr_Artist_MBId = os.environ.get('Lidarr_Artist_MBId') # artist.Metadata.Value.ForeignArtistId
Lidarr_Artist_Type = os.environ.get('Lidarr_Artist_Type') # artist.Metadata.Value.Type
Lidarr_Release_AlbumCount = os.environ.get('Lidarr_Release_AlbumCount') # remoteAlbum.Albums.Count
Lidarr_Release_AlbumReleaseDates = os.environ.get('Lidarr_Release_AlbumReleaseDates') # Comma separated list of album release dates
Lidarr_Release_AlbumTitles = os.environ.get('Lidarr_Release_AlbumTitles') # Pipe separated list of album titles
Lidarr_Release_AlbumMBIds = os.environ.get('Lidarr_Release_AlbumMBIds') # Pipe separated list of album external service IDs (e.g. MusicBrainz)
Lidarr_Release_Title = os.environ.get('Lidarr_Release_Title') # remoteAlbum.Release.Title
Lidarr_Release_Indexer = os.environ.get('Lidarr_Release_Indexer') # remoteAlbum.Release.Indexer
Lidarr_Release_Size = os.environ.get('Lidarr_Release_Size') # remoteAlbum.Release.Size
Lidarr_Release_Quality = os.environ.get('Lidarr_Release_Quality') # remoteAlbum.ParsedAlbumInfo.Quality.Quality.Name
Lidarr_Release_QualityVersion = os.environ.get('Lidarr_Release_QualityVersion') # remoteAlbum.ParsedAlbumInfo.Quality.Revision.Version
Lidarr_Release_ReleaseGroup = os.environ.get('Lidarr_Release_ReleaseGroup') # releaseGroup
Lidarr_Download_Client = os.environ.get('Lidarr_Download_Client') # message.DownloadClient
Lidarr_Download_Id = os.environ.get('Lidarr_Download_Id') # message.DownloadId

# Lidarr variables for On Release Import/On Upgrade
Lidarr_EventType = os.environ.get('Lidarr_EventType') # AlbumDownload
Lidarr_Artist_Id = os.environ.get('Lidarr_Artist_Id') # artist.Id
Lidarr_Artist_Name = os.environ.get('Lidarr_Artist_Name') # artist.Metadata.Value.Name
Lidarr_Artist_Path = os.environ.get('Lidarr_Artist_Path') # artist.Path
Lidarr_Artist_MBId = os.environ.get('Lidarr_Artist_MBId') # artist.Metadata.Value.ForeignArtistId
Lidarr_Artist_Type = os.environ.get('Lidarr_Artist_Type') # artist.Metadata.Value.Type
Lidarr_Album_Id = os.environ.get('Lidarr_Album_Id') # album.Id
Lidarr_Album_Title = os.environ.get('Lidarr_Album_Title') # album.Title
Lidarr_Album_MBId = os.environ.get('Lidarr_Album_MBId') # album.ForeignAlbumId
Lidarr_AlbumRelease_MBId = os.environ.get('Lidarr_AlbumRelease_MBId') # release.ForeignReleaseId
Lidarr_Album_ReleaseDate = os.environ.get('Lidarr_Album_ReleaseDate') # album.ReleaseDate
Lidarr_Download_Client = os.environ.get('Lidarr_Download_Client') # message.DownloadClient
Lidarr_Download_Id = os.environ.get('Lidarr_Download_Id') # message.DownloadId
Lidarr_AddedTrackPaths = os.environ.get('Lidarr_AddedTrackPaths') # Pipe separated list of added track paths
Lidarr_DeletedPaths = os.environ.get('Lidarr_DeletedPaths') # Pipe separated list of deleted files

# Lidarr variables for On Rename
Lidarr_EventType = os.environ.get('Lidarr_EventType') # Rename
Lidarr_Artist_Id = os.environ.get('Lidarr_Artist_Id') # artist.Id
Lidarr_Artist_Name = os.environ.get('Lidarr_Artist_Name') # artist.Metadata.Value.Name
Lidarr_Artist_Path = os.environ.get('Lidarr_Artist_Path') # artist.Path
Lidarr_Artist_MBId = os.environ.get('Lidarr_Artist_MBId') # artist.Metadata.Value.ForeignArtistId
Lidarr_Artist_Type = os.environ.get('Lidarr_Artist_Type') # artist.Metadata.Value.Type

# Lidarr variables for On Track Retag
Lidarr_EventType = os.environ.get('Lidarr_EventType') # TrackRetag
Lidarr_Artist_Id = os.environ.get('Lidarr_Artist_Id') # artist.Id
Lidarr_Artist_Name = os.environ.get('Lidarr_Artist_Name') # artist.Metadata.Value.Name
Lidarr_Artist_Path = os.environ.get('Lidarr_Artist_Path') # artist.Path
Lidarr_Artist_MBId = os.environ.get('Lidarr_Artist_MBId') # artist.Metadata.Value.ForeignArtistId
Lidarr_Artist_Type = os.environ.get('Lidarr_Artist_Type') # artist.Metadata.Value.Type
Lidarr_Album_Id = os.environ.get('Lidarr_Album_Id') # album.Id
Lidarr_Album_Title = os.environ.get('Lidarr_Album_Title') # album.Title
Lidarr_Album_MBId = os.environ.get('Lidarr_Album_MBId') # album.ForeignAlbumId
Lidarr_AlbumRelease_MBId = os.environ.get('Lidarr_AlbumRelease_MBId') # release.ForeignReleaseId
Lidarr_Album_ReleaseDate = os.environ.get('Lidarr_Album_ReleaseDate') # album.ReleaseDate
Lidarr_TrackFile_Id = os.environ.get('Lidarr_TrackFile_Id') # trackFile.Id
Lidarr_TrackFile_TrackCount = os.environ.get('Lidarr_TrackFile_TrackCount') # trackFile.Tracks.Value.Count
Lidarr_TrackFile_Path = os.environ.get('Lidarr_TrackFile_Path') # trackFile.Path
Lidarr_TrackFile_TrackNumbers = os.environ.get('Lidarr_TrackFile_TrackNumbers') # Comma separated list of track numbers
Lidarr_TrackFile_TrackTitles = os.environ.get('Lidarr_TrackFile_TrackTitles') # Pipe separated list of track titles
Lidarr_TrackFile_Quality = os.environ.get('Lidarr_TrackFile_Quality') # trackFile.Quality.Quality.Name
Lidarr_TrackFile_QualityVersion = os.environ.get('Lidarr_TrackFile_QualityVersion') # trackFile.Quality.Revision.Version
Lidarr_TrackFile_ReleaseGroup = os.environ.get('Lidarr_TrackFile_ReleaseGroup') # trackFile.ReleaseGroup
Lidarr_TrackFile_SceneName = os.environ.get('Lidarr_TrackFile_SceneName') # trackFile.SceneName
Lidarr_Tags_Diff = os.environ.get('Lidarr_Tags_Diff') # message.Diff.ToJson()
Lidarr_Tags_Scrubbed = os.environ.get('Lidarr_Tags_Scrubbed') # message.Scrubbed

# Lidarr variables for On Health Issue
Lidarr_EventType = os.environ.get('Lidarr_EventType') # HealthIssue
Lidarr_Health_Issue_Level = os.environ.get('Lidarr_Health_Issue_Level') # nameof(healthCheck.Type)
Lidarr_Health_Issue_Message = os.environ.get('Lidarr_Health_Issue_Message') # healthCheck.Message
Lidarr_Health_Issue_Type = os.environ.get('Lidarr_Health_Issue_Type') # healthCheck.Source.Name
Lidarr_Health_Issue_Wiki = os.environ.get('Lidarr_Health_Issue_Wiki') # Wiki URL for the health issue help page

# Lidarr variables for On Test
Lidarr_EventType = os.environ.get('Lidarr_EventType') # Test

# Custom variables
if Lidarr_EventType == 'Grab':
    subject = f'Lidarr - Grabbed {Lidarr_Artist_Name} {Lidarr_Release_Title}'
    content = f'''
    Artist: {Lidarr_Artist_Name}
    Release title: {Lidarr_Release_Title}
    Download client: {Lidarr_Download_Client}
    Download id: {Lidarr_Download_Id}
    Indexer: {Lidarr_Release_Indexer}
    Quality: {Lidarr_Release_Quality}
    '''
elif Lidarr_EventType == 'AlbumDownload':
    files = '\n'.join(f'- {x}' for x in Lidarr_AddedTrackPaths.split('|'))
    subject = f'Lidarr - Downloaded {Lidarr_Artist_Name} {Lidarr_Album_Title}'
    content = f'''
    Artist: {Lidarr_Artist_Name}
    Album: {Lidarr_Album_Title}
    Artist id: {Lidarr_Artist_MBId} (https://musicbrainz.org/artist/{Lidarr_Artist_MBId})
    Album id: {Lidarr_Album_MBId} (https://musicbrainz.org/release-group/{Lidarr_Album_MBId})
    Download client: {Lidarr_Download_Client}
    Download id: {Lidarr_Download_Id}
    Path: {Lidarr_Artist_Path}
    Files:
    {files}
    '''
elif Lidarr_EventType == 'Rename':
    subject = f'Lidarr - Renamed {Lidarr_Artist_Name}'
    content = f'''
    Artist: {Lidarr_Artist_Name}
    Artist id: {Lidarr_Artist_MBId} (https://musicbrainz.org/artist/{Lidarr_Artist_MBId})
    Path: {Lidarr_Artist_Path}
    '''
elif Lidarr_EventType == 'TrackRetag':
    subject = f'Lidarr - Retagged {Lidarr_Artist_Name} {Lidarr_Album_Title}'
    content = f'''
    Artist: {Lidarr_Artist_Name}
    Album: {Lidarr_Album_Title}
    Artist id: {Lidarr_Artist_MBId} (https://musicbrainz.org/artist/{Lidarr_Artist_MBId})
    Album id: {Lidarr_Album_MBId} (https://musicbrainz.org/release-group/{Lidarr_Album_MBId})
    File: {Lidarr_TrackFile_Path}
    '''
elif Lidarr_EventType == 'HealthIssue':
    subject = f'Lidarr - Health issue'
    content = f'''
    Level: {Lidarr_Health_Issue_Level}
    Message: {Lidarr_Health_Issue_Message}
    Type: {Lidarr_Health_Issue_Type}
    Wiki: {Lidarr_Health_Issue_Wiki}
    '''
elif Lidarr_EventType == 'Test':
    subject = 'Lidarr - Test message'
    content = ''
else:
    subject = f'Lidarr - Unknown event - {Lidarr_EventType}'
    content = ''

# Mail variables
mail_host = config.get('mail', 'host') or 'smtp.gmail.com'
mail_port = config.getint('mail', 'port') or 587
mail_sender_name = config.get('mail', 'sender_name') or 'xxx'
mail_sender_address = config.get('mail', 'sender_address') or 'xxx@gmail.com'
mail_sender_pass = config.get('mail', 'sender_pass') or 'xxx'
mail_receiver_address = config.get('mail', 'receiver_address') or 'xxx@gmail.com'

# Setup message
message = MIMEMultipart()
message['From'] = formataddr((mail_sender_name, mail_sender_address))
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
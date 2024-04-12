from flask import Flask, render_template, send_file
from ftplib import FTP
import os

app = Flask(__name__)

# Use environment variables for FTP server configuration
FTP_HOST = os.getenv('FTP_SERVER', '127.0.0.1')
FTP_USER = os.getenv('FTP_USERNAME', 'ftpuser')
FTP_PASS = os.getenv('FTP_PASSWORD', 'ftppassword')


@app.route('/')
def list_ftp_files():
    # Connect to the FTP server
    ftp = FTP()
    ftp.connect(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)

    # Get list of files and directories
    files = []
    directories = []
    ftp.dir('.', lambda x: files.append(
        x.split()[-1]) if x.startswith('-') else directories.append(x.split()[-1]))

    # Close the FTP connection
    ftp.quit()

    # Render the template with the list of files and directories
    return render_template('index.html', files=files, directories=directories)


@app.route('/download/<filename>')
def download_file(filename):
    # Connect to the FTP server
    ftp = FTP()
    ftp.connect(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)

    # Download the file to a temporary location
    temp_file = '/tmp/' + filename
    with open(temp_file, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)

    # Close the FTP connection
    ftp.quit()

    # Serve the file for download
    return send_file(temp_file, as_attachment=True)

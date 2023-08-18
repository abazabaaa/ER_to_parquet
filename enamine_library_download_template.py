import os
import fnmatch
from ftplib import FTP_TLS


class FTPWalk:
    """
    This class contains corresponding functions for traversing the FTP
    servers using BFS algorithm.
    """

    def __init__(self, connection):
        self.connection = connection

    def listdir(self, _path):
        """
        Return files and directory names within a path (directory).
        """
        file_list, dirs, nondirs = [], [], []
        try:
            self.connection.cwd(_path)
        except Exception as exp:
            print("the current path is:", self.connection.pwd(), exp.__str__(), _path)
            return [], []
        else:
            self.connection.retrlines('LIST', lambda x: file_list.append(x.split()))
            for info in file_list:
                ls_type, name = info[0], info[-1]
                if ls_type.startswith('d'):
                    dirs.append(name)
                else:
                    nondirs.append(name)
            return dirs, nondirs

# Change WALK path to either /S/,/M/,/S/H* or /M/H* to split up the download - MIGHT TIME OUT OTHERWISE
    def walk(self, path='/'):
        """
        Walk through FTP server's directory tree, based on a BFS algorithm.
        """
        dirs, nondirs = self.listdir(path)
        yield path, dirs, nondirs
        for name in dirs:
            path = os.path.join(path, name)
            yield from self.walk(path)
            self.connection.cwd('..')
            path = os.path.dirname(path)


# Establish an FTP_TLS connection - THIS MIGHT NEED TO BE UPDATED!!!!!
connection = FTP_TLS('ftp-rdb-fr.chem-space.com')
connection.login('user1', 'Gs!818HfqT2hoUwh')

# Create an instance of FTPWalk
ftpwalk = FTPWalk(connection)

# Define the pattern for file matching
pattern = '*.cxsmiles.bz2'

# Define the absolute path to the local directory where files will be downloaded- UPDATE THIS!!!
local_directory = '/path/to/local/directory/'

# Iterate through the FTP server's directory tree
for path, dirs, nondirs in ftpwalk.walk():
    for filename in nondirs:
        if fnmatch.fnmatch(filename, '*.cxsmiles.bz2'):
            remote_path = os.path.join(path, filename)
            local_path = os.path.join(local_directory, filename)
            with open(local_path, "wb") as local_file:
                connection.retrbinary(f"RETR {remote_path}", local_file.write)


# Close the FTP connection
connection.quit()

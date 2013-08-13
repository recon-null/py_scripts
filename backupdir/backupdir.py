# *********************************************
# THE BELOW HEADER MUST NOT BE REMOVED OR MODIFIED
#
# Backup Directory
#
# Author:       Recon
# Date:         8-25-09
#
# Copyright (C) 2010 Recon. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# THE ABOVE HEADER MUST NOT BE REMOVED OR MODIFIED
# *********************************************


"""
Backup directory module/script
"""


import os
import sys
import shutil
from optparse import OptionParser
import win32file


class DirectoryMgt:
    """ Directory management class

        Designed for backup purposes
    """

    # Report variables
    total_files = 0
    total_dirs = 0
    copied_files = 0
    copied_dirs = 0
    skipped_files = 0
    skipped_dirs = 0
    failed_files = 0

    def copy_directory(self, topSrc, topDest):
        """ Copies a directory from topSrc to topDest

            This function will only copy changed files
        """

        self.total_dirs += 1

        # If the dest folder doesn't exist,
        # create it
        if (not os.path.exists(topDest)):
            os.mkdir(topDest)
            self.copied_dirs += 1
        else:
            self.skipped_dirs += 1

        # List contents
        for path in os.listdir(topSrc):

            # Get the source info
            srcPath = os.path.join(topSrc, path)
            srcInfo = os.stat(srcPath)

            # Find the dest path
            destPath = os.path.join(topDest, path)

            # Is this a directory?
            if (os.path.isdir(srcPath)):

                # Yes, copy it
                self.copy_directory(srcPath, destPath)

            else:

                # Add one to the total files counter
                self.total_files += 1

                # Does this file already exist in the dest?
                if (os.path.exists(destPath)):

                    # Get the dest info
                    destInfo = os.stat(destPath)

                    # If we have a newer version, copy it
                    if (srcInfo.st_mtime > destInfo.st_mtime):
                        try:
                            win32file.CopyFile(srcPath, destPath, 0)
                            self.copied_files += 1
                        except:
                            print str.format("Error copying file {0} to {1}.\n",
                                             srcPath, destPath)
                            self.failed_files += 1
                    else:

                        # The file already exists, skipping
                        self.skipped_files += 1

                else:
                    try:
                        # The file doesn't exist in the dest, copy it
                        win32file.CopyFile(srcPath, destPath, 1)
                        self.copied_files += 1
                    except:
                        print str.format("Error copying file {0} to {1}.\n",
                                         srcPath, destPath)
                        self.failed_files += 1

def main(argv = None):
    """ Main function

        Runs the program
    """

    # If we weren't passed any args,
    # use the system argv
    if (argv == None):
        argv = sys.argv

    # Setup the parser
    parser = OptionParser()
    parser.add_option("--source", "-s",
                      help="The source directory.", dest="source")
    parser.add_option("--dest", "-d",
                       help="The destination directory.", dest="dest")

    # Parse the args
    (options, args) = parser.parse_args(argv)

    if options.source is not None and options.dest is not None:

        # Perform the copy
        dirmgt = DirectoryMgt()
        dirmgt.copy_directory(options.source, options.dest)

        # Create the report
        print "\n          Total      Copied      Skipped      Failed"
        print str.format("Dirs:     {0:<6}     {1:<6}      {2:<6}       N/A",
                         dirmgt.total_dirs, dirmgt.copied_dirs,
                         dirmgt.skipped_dirs)
        print str.format("Files:    {0:<6}     {1:<6}      {2:<6}       {3:<6}",
                         dirmgt.total_files, dirmgt.copied_files,
                         dirmgt.skipped_files, dirmgt.failed_files)

        print str.format("\nDirectory copy of {0} to {1} is complete.",
                         options.source, options.dest)

        return 0

    else:

        print "You must provide a source and destination."
        return 1


# Run main
if __name__ == "__main__":
    sys.exit(main())
# *********************************************
# THE BELOW HEADER MUST NOT BE REMOVED OR MODIFIED
#
# Recursive file processor
#
# Author:       Recon
# Date:         7-6-10
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
Recursive file processing class/script.
"""


import os
import sys
import shutil
import re
from optparse import OptionParser


class RecursiveFileProcessor:
    """ Recursive file processing class

    """

    # Report variables
    processed_dirs = 0
    total_files = 0
    skipped_files = 0
    processed_files = 0
    failed_files = 0
    command_format = "echo {0}"
    file_filter = ".*"

    def rec_process(self, topPath):
        """ Perform a recursive process on topPath

        """

        # Processing a directory
        self.processed_dirs += 1

        # List contents
        for path in os.listdir(topPath):

            # Get the actual path
            actualPath = os.path.join(topPath, path)

            # Is this a directory?
            if (os.path.isdir(actualPath)):

                # Yes, process it
                self.rec_process(actualPath)

            else:

                # Add one to the total files counter
                self.total_files += 1

                # Are we supposed to process this file?
                if re.search(self.file_filter, path) is not None:

                    try:

                        # Process the file
                        os.system(str.format(self.command_format, actualPath))
                        self.processed_files += 1

                    except:

                        print str.format("Error processing the file {0}.\n",
                                        actualPath)
                        self.failed_files += 1

                else:

                    # No, skip it
                    self.skipped_files += 1

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
    parser.add_option("--dir", "-d",
                      help="The root directory.", dest="dir")
    parser.add_option("--cmd", "-c",
                      help="The command template. E.g. \"echo {0}\", where {0} "
                            + "becomes each file's path in the directory tree.",
                      dest="cmd")
    parser.add_option("--file-filter", "-f",
                      help="The regex file name filter to use.",
                      dest="file_filter")

    # Parse the args
    (options, args) = parser.parse_args(argv)

    if options.dir is not None:

        # Create the processor
        recproc = RecursiveFileProcessor()

        if options.cmd is not None:
            recproc.command_format = options.cmd

        if options.file_filter is not None:
            recproc.file_filter = file_filter

        # Perform the processing
        recproc.rec_process(options.dir)

        # Create the report
        print "\nProcessing complete.\n\nSummary:\n"
        print "Processed directories: " + str(recproc.processed_dirs)
        print "Processed files:       " + str(recproc.processed_files)
        print "Skipped files:         " + str(recproc.skipped_files)
        print "Failed files:          " + str(recproc.failed_files)
        print "Total files:           " + str(recproc.total_files)

        return 0

    else:

        print "Error: You must provide a root directory."
        return 1


# Run main
if __name__ == "__main__":
    sys.exit(main())
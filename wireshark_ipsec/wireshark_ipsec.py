# *********************************************
# THE BELOW HEADER MUST NOT BE REMOVED OR MODIFIED
#
# Wireshark / IPSec
# This script takes a CSV summary export
# (all packets collapsed) from Wireshark and
# converts it into a batch file that adds all exported source
# IPs to an IPSec filter list.
#
# Read the comments below and adjust accordingly.
#
# Author:       Recon
# Date:         1-9-2010
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

# CSV parser
import csv

def main():

    # Open the summary file
    reader = csv.reader(open('packet_summary.csv', 'r'))
    ips = {}

    # Add all the source IPs
    for row in reader:
        if (not ips.has_key(row[2])):
            ips[row[2]] = 1
        else:
            ips[row[2]] += 1

    # Adjust this command template for your filter list
    cmd_template = "netsh ipsec static add filter" + \
                   " filterlist=\"Filter List Name Here\" " + \
                   "srcaddr={0} dstaddr=\"Me\"" \
                   " description=\"Packets from host: {1}\""

    # Create the batch file
    outputFile = open("output.txt", 'w')
    for item in ips.items():
        outputFile.write(cmd_template.format(item[0], item[1]))
        outputFile.write('\n')

    # We're done, write a pause and close the file
    outputFile.write("pause\n")
    outputFile.close()

if __name__ == '__main__':
    main()

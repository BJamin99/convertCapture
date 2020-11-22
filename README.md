# convertCapture
Convert Presonus StudioLive SD card capture to a Studio One/Capture compatible capture.

This has been tested with a capture from StudioLive Series III 32 mixer and Studio One 4 Professional.

Note that to import Fat Channel settings, the Fat Channel XT plugin is needed.  This is included in Studio One Artist and Professional.  It can be purchased for Studio One Prime.

## Usage
To run this file, put the script (convertCapture.py) and the .capture/.scn/.cnfg from the SD card in the same directory and then run convertCapture.py.

The script looks in the current directory for a .capture, .scn, and .cnfg with the same names.  Currently it only works with the first set of matching files it finds.  Ensure that there is only one set of .capture/.scn/.cnfg in the same directory.

The script does not modify the .scn or the .cnfg files.  It does have to change the .capture though, so a backup of the original is made as ".capture.orig".

## Background

For some background, please see the following PreSonus forum post:

https://forums.presonus.com/viewtopic.php?f=154&t=42520

Here is a PreSonus Answers post looking to have this capability built into StudioLive/Studio One:

https://answers.presonus.com/40152/studiolive-capture-sessions-should-tracks-according-track


A Python class for file comparison and new file backup.

Author: Yu Sun at University of Sydney

Email: sunyu0410@gmail.com

Website: https://github.com/sunyu0410/AmendmentBackUp

## Motivation
When it comes to backing up a large amout of data, it is often preferable to only copy the modified and unique files, rather than simply coping the whole directory. The `AmendmentBackUp` (`ABU`) class provides a simple interface to do that. No dependencies are required apart from the Python 3 standard library.

## Design
Say we have two folders, a source folder `dir1` which you have your most recent files and a reference folder `dir2` which holds some of your previous backup. What the `ABU` does is to compare all files in `dir1` with those in `dir2`, and copy the files to a third destination folder `dst`. If you simply want to add the files to the original back, you can set `dst` to `dir2`.



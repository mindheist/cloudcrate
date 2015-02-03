cloudcrate
==========
**cloudcrate** is a simple commandline utility that allows you to "Bring your own Dropbox" backed by Amazon S3.

1. Please download the cloudcrate zip from here(github).

2. Unzip the folder and Cd into it. This now becomes the equivalent of the 'dropbox' folder 

3.  There is a cloudcrate.py file in this folder. Run "python cloudcrate.py setup" from here to install necessary libraries.

4. Run python cloudcrate.py sync to upload files to the S3 bucket.

Check out the files at http://cloudcrate.hari.s3.amazonaws.com/list.html ( for the sake of the demo , the scripts point to a bucket in Amazon S3 already, and the above link allows you to access that bucket on a browser.)

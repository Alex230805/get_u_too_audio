# Get UToo: youtube cli tool for downloading audio files from a specified list


This is a python script designed to accept a list of URLs and download it content  in 
separate audio files. Each file will be named as the original youtube video and all of them will 
be placed inside a single destination folder in the current execution point. 
The file "pool.txt" is the one who contain YouTube's URLs, it can also contain comments for user 
only purposes. It's only possible to have one URL for each line. 

It's possible to specify the output mode for the entire execution by using the "-t" flag during invocation. 
For now there's only two different output types: "wav" and "mp3".
By using "-s" and/or "-d" flag it's possible to change the default source file from which the script will read the 
URLs, and the destination directory for the download.


The program is based on pytubefix library, so it support also playlist download as an option during invocation. By 
using the "-m" flag you can exchange the download mode from "pool" (which is the default who see each URL as a single video link) 
to "playlist" which threat each URL as a playlist link, diving into it and download every video inside. 

Example for possible invocations:

```bash

python3 get_u_too.py -t wav -m playlist -d /my/dest/dir

```

```bash

python3 get_u_too.py -t mp3 -s /my/custom/list.txt

```

```bash

# default invocation, download as mp3 everything inside "./pool.txt" in default mode, outputing in "./out"

python3 get_u_too.py

```

For a quick documentation use "-h" or "--help" flag during invocation.

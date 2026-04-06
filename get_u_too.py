
import pytubefix;
import sys;
import os;
import ffmpeg;
import asyncio;

from pytubefix.cli import on_progress;

def main(argv: [str]):
    url_list: str = "./pool.txt";
    dest_dir: str = "./out";
    file_stream: object;
    try:
        if not os.path.isfile(url_list):
            raise Exception(f"Missing url file list, you must create a file named {url_list} and add some URLs inside");
        if not os.path.isdir(dest_dir):
            print("Destination folder not present, creating it right now");
            os.mkdir(dest_dir);
        file_stream = open(url_list, "r");
        for line in file_stream:
            if not line[0] == '#':
                yt = pytubefix.YouTube(line, on_progress_callback=on_progress);
                file_name = yt.title+".wav";
                print(f"Searching for {file_name}");
                dest_name = os.path.join(dest_dir, file_name);
                main_stream = yt.streams[0].url;
                print("Downloading audio file, please wait ...");
                ffmpeg.input(main_stream).output(dest_name ,format="wav", loglevel="error").run();
                print("Done!");
        file_stream.close();
    except Exception as ex:
        print(f"Unable to continue due to: {ex}");
        exit(1);
    return 0;


main(sys.argv);

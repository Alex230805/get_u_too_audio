
import pytubefix;
import sys;
import os;
import ffmpeg;
import re;

from pytubefix.cli import on_progress;

def print_helper(): 
    print("Get UToo: youtube cli tool for audio files");
    print("\n-d: change destination folder, default is './out'");
    print("\n-s: change source pool file, default is './pool.txt'");
    print("\n-m or --mode: change download mode by specifying it:");
    print("   . pool: download audio from source file, default is './pool.txt', change it with -s. This is the default mode.");
    print("   . playlist: download all video from a specified playlist, each link inside the pool file is considered a playlist.");
    print("\n-t or --type: change output type by specifying one of the following:");
    print("   . mp3: download the video as an mp3 file");
    print("   . wav: download the video as an wav file")
    print("\n-h or --help: show helper");
    return;


def dump_file(yt: object, dest_dir: str, t: str):
    try:
        file_name = yt.title+"."+t;
        file_name = re.sub("/", " - ", file_name);
        print(f"Searching for {file_name}");

        dest_name = os.path.join(dest_dir, file_name);
        main_stream = yt.streams[0].url;
        print("Downloading audio file, please wait ...");
        ffmpeg.input(main_stream).output(dest_name ,format=t, loglevel="error").run();
        print("Done!");
    except Exception as ex:
        raise ex;
    return;

def main(argv: [str]):
    url_list: str = "./pool.txt";
    dest_dir: str = "./out";
    file_stream: object;

    mode: set = set(["pool", "playlist"]);
    output_type: set = set(["mp3", "wav"]);
    current_mode: str = "pool";
    current_type: str = "mp3";

    if len(argv) > 1:
        i: int = 1;
        while i < len(argv):
            if argv[i] == "-d":
                if i+1 >= len(argv):
                    print("The destination folder is not specified\n");
                    exit(1);
                else:
                    dest_dir = argv[i+1];
                    i+=1;
                    custom_dest = True;
            elif argv[i] == "-s":
                if i+1 >= len(argv):
                    print("Source pool file is not specified\n");
                    exit(1);
                else:
                    url_list = argv[i+1];
                    i+=1;
            elif argv[i] == "-m" or argv[i] == "--mode": 
                if i+1 >= len(argv):
                    print("Missing mode, default one is 'pool'. To operate in default mode you can avoid specifying the mode");
                    exit(1);
                else:
                    if argv[i+1] in mode:
                        current_mode = argv[i+1];
                        i+= 1;
                    else:
                        print("The selected one is not a valid mode");
                        exit(1);
            elif argv[i] == "-t" or argv[i] == "--type":
                if i+1 >= len(argv):
                    print("Missing output type, if not specified it would be 'mp3'");
                    exit(1);
                else:
                    if argv[i+1] in output_type:
                        current_type = argv[i+1];
                        i += 1;
                    else:
                        print("The selected output type is not one of the usable one, -h for more information");
                        exit(1);
            elif argv[i] == "-h" or argv[i] == "--help":
                print_helper();
                exit(0);
            else:
                print_helper();
                exit(1);
            i+= 1;
    try:
        if not os.path.isfile(url_list):
            raise Exception(f"Missing url file list, you must create a file named {url_list} and add some URLs inside");
        if not os.path.isdir(dest_dir):
            print("Default destination folder not present, creating it right now");
            os.mkdir(dest_dir);

        file_stream = open(url_list, "r");
        for line in file_stream:
            if len(line) > 0 and not line[0] == '#':
                yt: object;
                if current_mode == "playlist":
                    # downloading content inside a playlist
                    yt = pytubefix.Playlist(line);
                    print(f"Entering playlist mode, downloading content from '{yt.title}'");
                    for v in yt.videos:
                        dump_file(v, dest_dir, current_type);
                else:
                    yt = pytubefix.YouTube(line);
                    dump_file(yt, dest_dir, current_type);
        file_stream.close();
    except Exception as ex:
        print(f"Unable to continue due to: {ex}");
        exit(1);
    return 0;


main(sys.argv);

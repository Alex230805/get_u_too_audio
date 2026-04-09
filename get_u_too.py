
import pytubefix;
import sys;
import os;
import ffmpeg;
import re;

def print_helper(): 
    print("Get UToo: youtube cli tool for audio files");
    print("\n-d: change destination folder, default is './out'");
    print("\n-s: change source pool file, default is './pool.txt'");
    print("\n-m or --mode: change download mode by specifying it:");
    print("   . pool: download audio from source file, default is './pool.txt', change it with -s. This is the default mode.");
    print("   . playlist: download all video from a specified playlist, each link inside the pool file is considered a playlist.");
    print("\n-t or --type: change output type by specifying one of the following:");
    print("   . mp3");
    print("   . wav");
    print("   . flac");
    print("\n-r or --repeat-after-error: max amount of time one download can fail. Default is 5");
    print("\n-h or --help: show helper");
    return;


def dump_file(yt: object, dest_dir: str, t: str) -> int:
    sys.stdout.flush();
    file_name = yt.title+"."+t;
    file_name = re.sub("/", " - ", file_name);
    file_name = re.sub(":", ", ", file_name);
    #print(f"Searching for {file_name}");
    dest_name = os.path.join(dest_dir, file_name);
    if os.path.isfile(dest_name):
        #print("File already present, ignoring it ..");
        return 0;
    main_stream = yt.streams[0].url;
    #print("Downloading audio file, please wait ...");
    try:
        ffmpeg.input(main_stream).output(dest_name ,format=t, loglevel="error").run();
    except Exception as ex:
        #print(f"An erro during the download phase occurred: {ex}");
        if os.path.isfile(dest_name):
            os.remove(dest_name);
        return 1;
   # print("Done!");
    sys.stdout.flush();
    return 0;

def draw_bar(count: int, length: int, resolutions: int, title: str):
    sys.stdout.flush();
    print(f"\033[2K\033[4;36mCurrently downloading: '{title}'\033[0m\n".ljust(length));
    bar = f"\033[0;32m";
    sub = int(length/resolutions);
    i: int = 1;
    while i <= count:
        bar += "#"*sub;
        i += 1;
    bar = bar.ljust(length)[0:length]+"\033[0m";
    print(f"\033[2K[{bar}] \033[1;33m{count}\033[0m of \033[1;31m{resolutions}\033[0m", end="");
    sys.stdout.flush();
    return;

def set_cursor(lineup: int):
    print(f"\033[{lineup}F", end="");
    return;

def main(argv: [str]):
    try:
        url_list: str = "./pool.txt";
        dest_dir: str = "./out";
        file_stream: object;

        mode: set = set(["pool", "playlist"]);
        output_type: set = set(["mp3", "wav", "flac"]);
        current_mode: str = "pool";
        current_type: str = "mp3";
        try_limit: int = 5; # if the server fail to download, it will try again until the limit is reached
        default_bar_length: int = 100;

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
                elif argv[i] == "-r" or argv[i] == "--repeat-after-error":
                    if i+1 >= len(argv):
                        print("Missing max fail value");
                    else:
                        try:
                           try_limit = int(argv[i+1]);
                           i += 1;
                        except: 
                            print("Not a valid number for the max fail value");
                            exit(1);
                elif argv[i] == "-h" or argv[i] == "--help":
                    print_helper();
                    exit(0);
                else:
                    print_helper();
                    exit(1);
                i+= 1;
        if not os.path.isfile(url_list):
            print(f"Missing url file list, you must create a file named {url_list} and add some URLs inside");
            exit(1);
        if not os.path.isdir(dest_dir):
            print("Default destination folder not present, creating it right now");
            os.mkdir(dest_dir);

        file_stream = open(url_list, "r");
        local_file: [str] = [];
        for line in file_stream:
            if line[0] != "#" and "https" in line:
                local_file.append(line);
        file_stream.close();

        print(f"Welcome to Get UToo CLI interface, proceed to download {len(local_file)} URLs");
        for c,line in enumerate(local_file):
            yt: object;
            if current_mode == "playlist":
                # downloading content inside a playlist
                yt = pytubefix.Playlist(line);
                for tr, v in enumerate(yt.videos):
                    i: int = 0;
                    draw_bar(tr+1, default_bar_length, len(yt.videos), v.title);
                    while i < try_limit:
                        if dump_file(v, dest_dir, current_type) == 0:
                            i = try_limit;
                        else:
                            i += 1;
                    set_cursor(2);
                print("\n\n\n");
            else:
                yt = pytubefix.YouTube(line);
                draw_bar(c+1, default_bar_length, len(local_file), yt.title);
                i: int = 0;
                while i < try_limit:
                    if dump_file(yt, dest_dir, current_type) == 0:
                        i = try_limit;
                    else:
                        i += 1;
                set_cursor(2);
        if current_mode != "playlist": print("\n\n\n");
        print("Done, Coffie is ready sir ~ !");
    except KeyboardInterrupt as interrupt:
        print("\nForce exit\n");
        sys.exit(1);
    except Exception as ex:
        print(f"Unable to continue due to {ex}");
        exit(1);
    return 0;

main(sys.argv);

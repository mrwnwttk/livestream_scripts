# livestream_scripts

Collection of scripts for archiving and organizing livestreams (mainly for r/EDMLivestreams).
These should work on Windows, Linux and macOS.

### save_livestream.py

Takes a base filename and twitch link, which can be either a link to a twitch channel or specific video. Automatically adds timestamps to the filename. Loops endlessly and can be left alone to watch for upcoming streams.

Requires `streamlink` and `python3` to be installed and in your respective PATH environment variable.

Example:
```
$ python3 save_livestream.py "Insomniac" https://twitch.tv/insomniac

Downloading from Twitch!
Downloading stream...
URL: https://www.twitch.tv/insomniac
Filename : insomniac - 2020-11-04 06-38-04.ts
[cli][info] Found matching plugin twitch for URL https://www.twitch.tv/insomniac
[cli][info] Available streams: audio_only, 160p (worst), 360p, 480p, 720p, 1080p (best)
[cli][info] Opening stream: 1080p (hls)
[plugin.twitch][info] Will skip ad segments
[download][.. 2020-11-04 06-38-04.ts] Written 6.1 MB (10s @ 618.9 KB/s)

[...]
```

### split.py

Splits a livestream recording into mkv and m4a files given a set of timestamps in the form of a simple text file. There's no transcoding involved, the video and audio streams are always just copied in order for them to not lose any quality.

Here's what one of those text files might look like:

```
couchlands - 2020-09-25 17-50-14.ts
Couchlands
00:10:25 01:08:47 Swarm
01:10:17 02:08:05 Level Up
02:09:01 03:03:34 Samplifire
03:04:26 04:04:39 Hydraulix
04:09:20 05:09:08 Hekler
05:10:10 06:08:37 Habstrakt
06:09:10 07:05:53 Modestep
07:09:47 08:02:01 Kai Wachi
08:10:00 09:10:02 Barely Alive
09:14:08 10:10:12 Virtual Riot
10:11:09 11:33:34 Excision
```

The first line is the filename of the original file, the second line is the name of the event, which will be at the beginning of every filename. Neither can be left out.

If you want a line to be skipped, just put `#` in front of it like this:
```
#09:14:08 10:10:12 Virtual Riot
```

If a line is not skipped but a file with the same name already exists it will be overwritten.

If you named your timestamps file `timestamps.txt`, make sure your recording is inside the same folder you're running the script from and execute it like this:
```
$ python3 split.py timestamps.txt
```
The end result will look a little like this:

![](https://i.imgur.com/U3bHTIn.png)

### upload.py

Used to upload files to gofile.io. Automatically formats links as markdown for convenience.

Uses the timestamps file that was used together with the `split.py` script. You can also skip lines by putting `#` in front the line, same procedure as with `split.py`.

Requires `curl` (which should come pre-installed on Windows/Linux/macOS) and `python3`.

There's also `upload_with_password.py`, which automatically sets a password for every upload. The password is set to `nosharingallowed` by default, but can be changed. It is located right at the top of the file. If you decide to change it, make sure that it doesn't contain any spaces and only consists of letters and numbers.

Installation:
```
$ python3 -m pip install requests
```

Usage:
```
$ python3 upload.py timestamps.txt
```


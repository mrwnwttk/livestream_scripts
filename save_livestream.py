#!/bin/env python3
import sys
import time
import subprocess
from time import gmtime, strftime
from random import uniform

MIN_WAIT = 45
MAX_WAIT = 70
TERM_CHARS = {
    'el': '\33[K', # clr_eol, clear the line
    'el1': '\33[2K', # clr_bol, clear to the beginning of line
    'cuu1': '\033[A' # cursor_up, move cursor up
}
# print(f"DEBUG: Default special characters: {dict([(key, list(val)) for key, val in TERM_CHARS.items()])}")


def get_terminal_char(char_type):
    """Query terminfo string capabilities with tput for a non-printable 
    character that can be used by the current terminal (see man 5 terminfo)."""
    try:
        proc = subprocess.run(["tput", char_type],
            capture_output=True, check=True, text=True
        )
        ret = proc.stdout
        return ret
    except subprocess.CalledProcessError as e:
        print(f"Error getting capability \"{char_type}\" from tput: {e}")
    return None


for key, value in TERM_CHARS.items():
    char = get_terminal_char(key)
    if char is not None:
        TERM_CHARS[key] = char
# print(f"DEBUG: Updated special characters: {dict([(key, list(val)) for key, val in TERM_CHARS.items()])}")


def download(link, quality="best"):
    current_date_time = strftime("%Y-%m-%d %H-%M-%S", gmtime())
    base_filename = current_date_time + " " \
                    + sys.argv[1] \
                    + " [" + quality + "].ts"

    cmd = ["streamlink", "--twitch-disable-hosting", "--twitch-disable-ads",
            "--hls-live-restart", "-o", f"\"{base_filename}\"",
            link, quality
        ]

    # DEBUG simulate streamlink output for testing
    # cmd = 'echo "[cli][info] Found matching plugin twitch for URL https://www.twitch.tv/matsuromeru" ; sleep 1;'\
    #     'echo "error: No playable streams found on this URL: https://www.twitch.tv/matsuromeru" ; sleep 1;'\
    #     'exit 1;'

    try:
        process = subprocess.run(cmd, check=True)  # DEBUG: ,shell=True)
        if process.returncode == 0:
            print(f"Saved Streamlink recording with filename: \"{base_filename}\"")
    except subprocess.CalledProcessError:
        # print(f"{cmd[0]} exit code: \"{e.returncode}\"")

        # Overwrite the two last lines with current time to reduce backlog clutter
        sys.stdout.write(TERM_CHARS['cuu1'])
        sys.stdout.write(TERM_CHARS['cuu1'] + TERM_CHARS['el1'] + '\r' + current_date_time + " " + TERM_CHARS['el'])
        # sys.stdout.flush()


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <base filename> <link to Twitch>\n")
        print(f"Example for Twitch: {sys.argv[0]} sovietwomble https://www.twitch.tv/sovietwomble/")
        print(f"Example for Twitch: {sys.argv[0]} sovietwomble https://www.twitch.tv/videos/571088399")
        exit(1)

    if "twitch.tv" in sys.argv[2]:
        if '/videos/' in sys.argv[2]:
            download(sys.argv[2])
        else:
            while True:
                download(sys.argv[2])
                time.sleep(uniform(MIN_WAIT, MAX_WAIT))

if __name__ == '__main__':
    main()

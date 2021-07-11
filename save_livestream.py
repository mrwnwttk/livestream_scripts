#!/bin/env python3
import sys
import time
import subprocess
from time import gmtime, strftime
from random import uniform

MIN_WAIT = 45
MAX_WAIT = 70
TERM_SEQ = {}
DEFAULT_TERM_SEQ = {
    'el': '\33[K', # clr_eol, clear from the cursor to the end of the line
    'el1': '\33[2K', # clr_bol, clear from the cursor to the beginning of the line
                     # The <n> parameter has 3 possible values according to
                     # https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences#text-modification
                     # so technically, this value is actually el2
    'cuu1': '\033[A', # cursor_up, move cursor up by one line
    'cuu2': '\033[2A'  # same as above, 2 lines
}

def get_term_seq(char_type):
    """Query terminfo string capabilities with tput for a non-printable
    character that can be used by the current terminal (see man 5 terminfo)."""
    try:
        proc = subprocess.run(["tput", char_type],
            capture_output=True, check=True, text=True
        )
        return proc.stdout  # or stdout.decode() if text=False
    except subprocess.CalledProcessError as e:
        print(f"Error getting capability \"{char_type}\" for this terminal: {e}")
    return ""

# Build sequences ahead of time
for key, value in DEFAULT_TERM_SEQ.items():

    # Fallback, because not sure how to query capabilities on Windows
    if sys.platform == "win32":
        TERM_SEQ[key] = ""
        continue

    # Special key. Sequences with parameters (ie. "2") are not retrievable
    if key == 'cuu2':
        if TERM_SEQ.get('cuu1') is not None:  # we don't have this key yet
            # Insert "2" parameter in the seq
            idx = TERM_SEQ['cuu1'].rfind('A')
            if idx == -1:
                TERM_SEQ[key] = TERM_SEQ['cuu1'] + TERM_SEQ['cuu1']
                continue
            TERM_SEQ['cuu2'] = TERM_SEQ['cuu1'][:idx] + "2" + TERM_SEQ['cuu1'][idx:]
            continue
        TERM_SEQ[key] = DEFAULT_TERM_SEQ['cuu2']
        continue

    TERM_SEQ[key] = get_term_seq(key)

# print(f"Default key sequences: {dict([(key, list(val)) for key, val in DEFAULT_TERM_SEQ.items()])}")
# print(f"Updated key sequences: {dict([(key, list(val)) for key, val in TERM_SEQ.items()])}")


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
        sys.stdout.write(
            TERM_SEQ['cuu2']
            + TERM_SEQ['el1']
            + '\r'
            + current_date_time
            + " "
            + TERM_SEQ['el']
        )
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

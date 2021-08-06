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


def download(link, quality="best"):
    current_date_time = strftime("%Y-%m-%d %H-%M-%S", gmtime())
    base_filename = current_date_time + " " \
                    + sys.argv[1] \
                    + " [" + quality + "].ts"

    cmd = ["streamlink", "--twitch-disable-hosting", "--twitch-disable-ads",
            "--hls-live-restart", "-o", base_filename,
            link, quality
        ]

    full_output = ""
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        while True:
            try:
                output = process.stdout.readline()
                if not output:
                    break
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.decode(sys.stdout.encoding), end='')
                    full_output += output.decode(sys.stdout.encoding)
            except:
                raise subprocess.CalledProcessError
            process.returncode = process.poll()

        if process.returncode == 0:
            print(f"Saved Streamlink recording with filename: \"{base_filename}\"")
        else:
            raise subprocess.CalledProcessError(process, process.returncode)

    except subprocess.CalledProcessError as e:
        # Overwrite the two last lines with current time to reduce backlog clutter
        if not sys.platform == "win32":
            sys.stdout.write(
                TERM_SEQ['cuu2']
                + TERM_SEQ['el1']
                + '\r'
                + current_date_time
                + " "
                + TERM_SEQ['el']
            )
        else:
            # We assume that powershell.exe is present on the system
            # That way controlling the cursor will work in both cmd and powershell
            term_width = int(subprocess.check_output(["powershell.exe", "$Host.UI.RawUI.WindowSize.Width"]).decode(sys.stdout.encoding).rstrip())
            current_y = int(subprocess.check_output(["powershell.exe", "[console]::CursorTop"]).decode(sys.stdout.encoding).rstrip())

            if " is hosting " in full_output:
                ln = 5
            else:
                ln = 3

            for y in range(1,ln):
                subprocess.run(["powershell.exe", f"[console]::setcursorposition(0,{current_y - y})"])
                print(" " * term_width, end='\r')


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
                try:
                    time.sleep(uniform(MIN_WAIT, MAX_WAIT))
                except KeyboardInterrupt:
                    print()
                    exit()
if __name__ == '__main__':
    main()

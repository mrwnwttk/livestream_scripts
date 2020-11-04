import sys
import os
import re
import time
from time import gmtime, strftime

def download(link):
		print("Downloading from Twitch!")
		current_date_time = strftime("%Y-%m-%d %H-%M-%S", gmtime())
		base_filename = sys.argv[1] + " - " + current_date_time + ".ts"
		print("Downloading stream...")
		print("URL: {}".format(link))
		print("Filename : {}".format(base_filename))
		os.system("streamlink --twitch-disable-hosting --twitch-disable-ads --hls-live-restart -o \"{}\" {} best".format(base_filename, link))

def main():
	if len(sys.argv) != 3:
		print("Usage: {} <base filename> <link to Twitch>".format(sys.argv[0]))
		print("")
		print("Example for Twitch: {} sovietwomble https://www.twitch.tv/sovietwomble/".format(sys.argv[0]))
		print("Example for Twitch: {} sovietwomble https://www.twitch.tv/videos/571088399".format(sys.argv[0]))
		exit(0)

	if "twitch.tv" in sys.argv[2]:
		if '/videos/' in sys.argv[2]:
			download(sys.argv[2])
		else:
			while True:
				if sys.platform == 'win32':
					os.system("cls")
				else:
					os.system('clear')
				download(sys.argv[2])
				time.sleep(1)

if __name__ == '__main__':
	main()

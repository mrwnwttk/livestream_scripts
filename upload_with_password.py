import os
import sys
import json

password = "nosharingallowed"

def upload(filename):
	global password
	print(filename)
	# Check for best available server
	best_server = os.popen("curl -s https://apiv2.gofile.io/getServer").read()
	j = json.loads(best_server)
	best_server = j['data']['server']
	print(f"Best server: {best_server}")

	# Get extension
	extension = filename.split('.')[-1]
	# Upload file
	if extension == 'mkv':
		content_type = "video/x-matroska"
	if extension == 'm4a':
		content_type = "audio/x-m4a"
	if extension == 'mp4':
		content_type = "video/mp4"
	if extension == 'webm':
		content_type = "video/webm"

	upload_state = os.popen("curl -F file=\"@{};type={}\" -F password={} https://{}.gofile.io/uploadFile".format(filename, content_type, password, best_server)).read()
	j = json.loads(upload_state)
	print(j)
	url = "https://gofile.io/d/" + j['data']['code']
	print(url)
	return url

def main():
	if len(sys.argv) != 2:
		print(f"Usage: {sys.argv[0]} <timestamps.txt>")
		exit()

	with open(sys.argv[1], 'r') as f:
		content = f.read()
		content = content.split('\n')

		# Remove empty elements from list
		content = [x for x in content if x]


	# Remove recording filename
	content.pop(0)
	# Get prefix for all recordings
	prefix = content[0]
	# Remove prefix from list, leaving only the artists
	content.pop(0)

	# Get list of artists
	artists = []

	for index, line in enumerate(content):
		if line[0] != '#':
			artists.append(" ".join(line.split(' ')[2:]))
		else:
			print(f"Skipping line {index + 1}: {line[1:]}")

	# Autodetect audio and video file extensions
	full_fn = ""
	for file in os.listdir():
		if "- Audio" in file:
			audio_file_extension = file.split('.')[-1]
			full_fn = file
			full_fn = full_fn.split(" - Audio")[0]
			break
	for file in os.listdir():
		if not "- Audio" in file and full_fn in file:
			video_file_extension = file.split('.')[-1]
			break

	artist_list = []
	for index, a in enumerate(artists):
		a = [a]
		a.append(f"{prefix} - {a[0]}.{video_file_extension}")
		a.append(f"{prefix} - {a[0]} - Audio.{audio_file_extension}")
		artist_list.append(a)

	artists_uploads = []

	for i in artist_list:
		print(i)
		x = [i[0]]
		video_url = upload(i[1])
		x.append(video_url)
		audio_url = upload(i[2])
		x.append(audio_url)
		artists_uploads.append(x)


	print("\n\n++++++++++++++++\n\n")

	for i in artists_uploads:
		print(f"{i[0]}: [Video]({i[1]}) | [Audio]({i[2]})\n")

if __name__ == '__main__':
	main()

import os
import sys

if len(sys.argv) < 2:
	print("Wrong syntax! Usage: python {} <filename of timestamps>.txt".format(sys.argv[0]))
	print("Content of the timestamps file:\n")
	print("\tVideo Filename.xyz")
	print("\tBase Filename")
	print("\t00:11:22.123 00:22:33 Arist Number 1")
	print("\t00:33:44.1 00:44:5.09 Arist Number 2")
	print("\t[...]")
	exit()

filename_txt = sys.argv[1]

with open(filename_txt) as f:
	file_content = f.read()

file_content = file_content.split('\n')
file_content = [x for x in file_content if x]

filename_to_split = file_content[0]
print(len(filename_to_split))
print("Filename: " + filename_to_split)
del file_content[0]
base_filename = file_content[0]
print("Base filename: " + base_filename)
del file_content[0]

for x in range(len(file_content)):
	if file_content[x][0] != '#':
		y = file_content[x].split(" ")
		print("Start time: " + y[0])
		print("End time: " + y[1])
		artist = ""
		for i in range(len(y)):
			if i > 1:
				artist += y[i]
				if i != (len(y) -1):
					artist += " "
		print(artist)
		os.system("ffmpeg -y -i \"{}\" -ss {} -to {} -c:v copy -c:a copy \"{} - {}.mkv\"".format(filename_to_split, y[0], y[1], base_filename, artist))
		os.system("ffmpeg -y -i \"{} - {}.mkv\" -vn -c:a copy \"{} - {} - Audio.m4a\"".format(base_filename, artist, base_filename, artist))
	else:
		print(f"Skipping line {x + 1}: {file_content[x][1:]}")
print("Done!")

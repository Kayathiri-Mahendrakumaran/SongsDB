import json
import codecs
import unicodedata
import random
import os

song_category = ["குத்து பாடல்","மெல்லிசை பாடல்","கர்நாடக சங்கீதம்","மேலைத்தேய சங்கீதம்"]

directory = 'Lyrics_2019/'
files_list = os.listdir(directory)
f = codecs.open("lyrics_2019_new.txt", 'w', encoding='utf-8')

# files_list = ['உயிரிலே உயிரிலே.json']
print("Processing %d files"%(len(files_list)))

for file in files_list:

    print(file)
    song_json = json.load(codecs.open(directory+file, 'r', 'utf-8-sig'))
    song_json["மதிப்பீடு"] = random.randint(1,5)
    song_json["நுகர்ச்சி"] = random.randint(100,10000)
    song_json["வகை"] = song_category[random.randint(0,3)]

    for attribute, value in song_json.items():
        # print(attribute, value)
        song_json[attribute] = unicodedata.normalize("NFKD", str(value))

    json.dump(song_json, f, ensure_ascii=False)
    f.write('\n')
    print(song_json)
    print()

f.close()

# -*- coding: utf-8 -*-
import wget
import os

# band = "the offspring"
band = input("Type the name of the band: ")
pages = 2
songs_dict = {}
songs_list = []

band = band.replace(' ','+')

for page in range(pages):
    url = 'http://www.setlist.fm/search?page=%d&query=%s'%(page+1,band)
    band_filename = wget.download(url,out='band.html')
    band_file = open(band_filename)
    band_html = band_file.read()
    setlists = band_html.split(' setlistPreview')
    for setlist in setlists[1:]:
        link = setlist.split('href="')[1].split('.html')
        url = 'http://www.setlist.fm/'+link[0]+".html"
        url = url.replace('&amp;','&')
        setlist_filename = wget.download(url,out='setlist.html')
        setlist_file = open(setlist_filename)
        setlist_html = setlist_file.read()
        if not "Sorry, there are no songs in this setlist yet" in setlist_html:
            songs = setlist_html.split('songLabel')[1:]
            for song in songs:
                label = song.split('>')
                label = label[1].split('<')
                label = label[0].replace('&amp;','&').replace('&#039;',"'")
                print('\n%s\n'%label)
                if label in songs_dict:
                    songs_dict[label] += 1
                else:
                    songs_dict[label] = 1

for key in songs_dict:
    if songs_dict[key] < 10:
        songs_list.append('00' + str(songs_dict[key]) + ' ' + key + '\n')
    elif songs_dict[key] < 100:
        songs_list.append('0' + str(songs_dict[key]) + ' ' + key + '\n')
    else:
        songs_list.append(str(songs_dict[key]) + ' ' + key + '\n')

songs_list.sort(reverse=True)

files = os.listdir('.')
for f in files:
    if f != 'crawler.py':
        try:
            os.remove(f)
        except:
            pass

f=open('results/'+band.replace('+','_')+'_setlister.txt','w')
f.writelines(songs_list)
f.close()

print("\n_____________\n\nRESULT:\n")
for song in songs_list:
	print (song)

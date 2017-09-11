# -*- coding: utf-8 -*-
import wget
import os

band = "red hot chili peppers"
# band = input("Type the name of the band: ")
band = band.replace(' ','+')
url = 'http://www.setlist.fm/search?query='+band
band_filename = wget.download(url,out='band.html')
band_file = open(band_filename)
band_html = band_file.read()
artists = band_html.split('<h3>Artist</h3>')
artist = artists[1].split('href="')
link = artist[1].split('" rel')
url = 'http://www.setlist.fm/'+link[0]
url = url.replace('&amp;','&')
setlists_filename = wget.download(url,out='setlists.html')
setlists_file = open(setlists_filename)
setlists_html = setlists_file.read()
setlists_split = setlists_html.split('href="setlist/')[1:11]
songs_dict = {}
for setlist in setlists_split:
    link = setlist.split('" title')
    url = 'http://www.setlist.fm/setlist/'+link[0]
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

songs_list = []
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

f=open(band.replace('+','_')+'_setlister.txt','w')
f.writelines(songs_list)
f.close()

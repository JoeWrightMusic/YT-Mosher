from __future__ import unicode_literals
import urllib.request
import urllib.parse
import re
import os
import youtube_dl
from moviepy.editor import VideoFileClip, concatenate_videoclips
from random import uniform, random, randint
import time
import datetime


#EDIT VALUES TO DETERMINE LENGTH AND CONTENT OF OUTPUT
iterations = 100
word_array = ['ASMR', 'pink noise', 'vine complation', 'slow tv']
x=0
while x < iterations:
    print('BEGIN'+str(x)+'/////////////////////')
    search_res = 0
    search_string = word_array[x%len(word_array)]
    print(search_string)
    query_string = urllib.parse.urlencode({"search_query" : search_string})
    #search for results <4min
    html_content = urllib.request.urlopen("https://www.youtube.com/results?" + 'sp=EgQQARgB&'+ query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    
    if len(search_results) < 40:
        search_res = randint(0, len(search_results-1))
    else: 
        search_res = randint(0, 39)
    full_url = "http://www.youtube.com/watch?v=" + search_results[search_res]
    print('URL:' + full_url + ' RESULT No. ' + str(search_res))
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta =  ydl.extract_info(full_url , download=False) 
        vidlength = meta['duration']
    vidlength = vidlength/2
    print(meta['title']) 
    s=meta['title']
    
    try:
        cur_ytvid = 'temp'+str(x)+'.mp4'
        ydl_opts = {
            'outtmpl': cur_ytvid, 
            'format': 'bestvideo',
            'noplaylist': True,
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([full_url]) 
            time.sleep(0.5)
            print("Video downloaded!")
        clip = 1
    except: 
        print("Mp4 not available, trying something else...")
        clip = 0

    if clip == 1:
        try: 
            # load to videoFileClip and get duration
            fullvideo = VideoFileClip(cur_ytvid)
            vidlength = fullvideo.duration
            # get random length and start point
            if vidlength <= 2: 
                start = 0
                length = 0.1
            else: 
                length = round(uniform(0.1,0.99), 2)
                start = round(uniform(0, vidlength-2), 2)
            print([vidlength, start, length])
            vidclip = fullvideo.subclip(start, start+length)
            print('Got clip')
            time.sleep(0.5)
            join=1
        except: 
            print('Corrupted d-l')
            join=0
        
        if join == 1:
            try:
                # join and store video clips
                if x==0:
                    vidclip.write_videofile('Output0.mp4')
                    print('Output done!')
                    time.sleep(0.5)
                else: 
                    previous = VideoFileClip('Output'+str(x-1)+'.mp4')
                    vidout = concatenate_videoclips([previous, vidclip])
                    vidout.write_videofile('Output'+str(x)+'.mp4')
                    print('Output done!')
                    time.sleep(0.5)
                x+=1
                delete_temps=1
            except:
                print("File read error - rewinding from "+str(x))
                x -= 1
                print('REWIND TO: ' + str(x))
                delete_temps=0
        if delete_temps == 1:
            print('removing: ' + cur_ytvid)
            os.remove(cur_ytvid)
            try:
                if x>2:
                    print('Removing: Output'+str(x-3)+'.mp4')
                    os.remove('Output'+str(x-3)+'.mp4')
                    print('Videos removed')
            except: 
                print('Old video already deleted, moving on...')
                
    
    


    
  
from django.shortcuts import render
from .models import audio
import os
import datetime
from django.contrib import messages

import mutagen
from mutagen.wave import WAVE

# Create your views here.

def upload_file(request):
    if request.method == "POST":
        #request file from frontend
        files = request.FILES.getlist('file')

        # iterating multiple file of list
        for file in files:
            try:
                # extracting audio file size
                file.seek(0, os.SEEK_END)
                audio_size = file.tell()

                # extension of the file
                file_extension = (file.name.split("."))[-1]

                #length of the file
                audio_length_min , audio_length_sec = get_audio_file_length(file)
                audio_length = str(int(audio_length_min))+":"+str(int(audio_length_sec))
                
                # adding data to database
                audio.objects.create(audio_name= file.name,audio_file=file,audio_size=audio_size,audio_extension=file_extension,audio_upload_date=datetime.datetime.now(),audio_length=audio_length)
            
                # checking if the length of audio is more than 10 min
                if audio_length_min >= 10.0:
                    #if length is more that 10 min returning message "Length of audio is more than 10"
                    messages.info(request,"Length of audio is more than 10")

            except:
                pass

        #extracting data from database and rendering html page                  
        data = audio.objects.all().order_by('-id')
        context={"datas":data}
        return render(request, "audio.html",context=context)
    
    #extracting data from database and rendering html page 
    data = audio.objects.all().order_by('-id')
    context={"datas":data}
    return render(request, "audio.html",context=context)

# function to convert length to min and sec
def get_audio_file_length(file_object):
  mutagen_object = mutagen.File(file_object)
  audio_file_length_in_seconds = mutagen_object.info.length
  minutes = audio_file_length_in_seconds // 60
  seconds = audio_file_length_in_seconds % 60
  return minutes, seconds
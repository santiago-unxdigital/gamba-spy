from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time 
import sys
from pprint import pprint
from . import forms
import csv

'''
def index(request, artist):
        client_id = '851985a4c736425fac5e6c803c3c9055'
        client_secret = '86c6552c29664f5aa3b284ecece085b0'
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        search_str = artist
        result = sp.search(search_str,1,0,'artist')
        artist = result['artists']['items'][0]
        
        context = {'result': artist}
        return render(request, 'spy_artist/index.html', context)
'''

def index(request):
    form = forms.InputForm()
    return render(request, 'index.html', {'form': form})

def addition(a,b):
    c = a + b
    return c

def output(request):
    if request.method == 'POST':
        form = forms.InputForm(request.POST)
        if form.is_valid():
            input1 = form.cleaned_data['input1']

            client_id = '851985a4c736425fac5e6c803c3c9055'
            client_secret = '86c6552c29664f5aa3b284ecece085b0'
            client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            search_str = input1
            result = sp.search(search_str,1,0,'artist')


            try:
                artist = result['artists']['items'][0]
                request.session['artist'] = artist
            except:
                artist = None

            context = {'artist': artist}

            return render(request, 'output.html', context)
    else:
            form = forms.InputForm()

def download(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Search Results.csv"'

    artist = request.session.get('artist')


    writer = csv.writer(response)
    writer.writerow(['Name', 'Spotify ID', 'Genders', 'Followers', 'Popularity', 'External url'])
    writer.writerow([artist['name'], artist['id'], artist['genres'], artist['followers']['total'], artist['popularity'], artist['external_urls']['spotify']])
    
    return response

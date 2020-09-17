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
import numpy as np
import json

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

            sleep_min = 2
            sleep_max = 5
            start_time = time.time()
            request_count = 0
            spotify_albums = {}
            album_count = 0

            def albumSongs(uri):
                album = uri #assign album uri to a_name

                spotify_albums[album] = {} #Creates dictionary for that specific album
                #Create keys-values of empty lists inside nested dictionary for album
                spotify_albums[album]['album'] = [] #create empty list
                spotify_albums[album]['track_number'] = []
                spotify_albums[album]['id'] = []
                spotify_albums[album]['name'] = []
                spotify_albums[album]['uri'] = []
                tracks = sp.album_tracks(album) #pull data on album tracks

                for n in range(len(tracks['items'])): #for each song track
                    spotify_albums[album]['album'].append(album_names[album_count]) #append album name tracked via album_count
                    spotify_albums[album]['track_number'].append(tracks['items'][n]['track_number'])
                    spotify_albums[album]['id'].append(tracks['items'][n]['id'])
                    spotify_albums[album]['name'].append(tracks['items'][n]['name'])
                    spotify_albums[album]['uri'].append(tracks['items'][n]['uri'])

            def audio_features(album):
                #Add new key-values to store audio features
                spotify_albums[album]['acousticness'] = []
                spotify_albums[album]['danceability'] = []
                spotify_albums[album]['energy'] = []
                spotify_albums[album]['instrumentalness'] = []
                spotify_albums[album]['liveness'] = []
                spotify_albums[album]['loudness'] = []
                spotify_albums[album]['speechiness'] = []
                spotify_albums[album]['tempo'] = []
                spotify_albums[album]['valence'] = []
                spotify_albums[album]['popularity'] = []
                #create a track counter
                track_count = 0
                for track in spotify_albums[album]['uri']:
                    #pull audio features per track
                    features = sp.audio_features(track)
                    
                    #Append to relevant key-value
                    spotify_albums[album]['acousticness'].append(features[0]['acousticness'])
                    spotify_albums[album]['danceability'].append(features[0]['danceability'])
                    spotify_albums[album]['energy'].append(features[0]['energy'])
                    spotify_albums[album]['instrumentalness'].append(features[0]['instrumentalness'])
                    spotify_albums[album]['liveness'].append(features[0]['liveness'])
                    spotify_albums[album]['loudness'].append(features[0]['loudness'])
                    spotify_albums[album]['speechiness'].append(features[0]['speechiness'])
                    spotify_albums[album]['tempo'].append(features[0]['tempo'])
                    spotify_albums[album]['valence'].append(features[0]['valence'])
                    #popularity is stored elsewhere
                    pop = sp.track(track)
                    spotify_albums[album]['popularity'].append(pop['popularity'])
                    track_count+=1

            try:
                artist = result['artists']['items'][0]

                #Extract Artist's uri
                artist_uri = artist['uri']
                #Pull all of the artist's albums
                sp_albums = sp.artist_albums(artist_uri, album_type='album')
                #Store artist's albums' names' and uris in separate lists
                album_names = []
                album_uris = []
                for i in range(len(sp_albums['items'])):
                    album_names.append(sp_albums['items'][i]['name'])
                    album_uris.append(sp_albums['items'][i]['uri'])
                    
                #Keep names and uris in same order to keep track of duplicate albums
                album_names
                album_uris

                spotify_albums = {}
                album_count = 0
                for i in album_uris: #each album
                    albumSongs(i)
                    print("Album " + str(album_names[album_count]) + " songs has been added to spotify_albums dictionary")
                    album_count+=1 #Updates album count once all tracks have been added

                for i in spotify_albums:
                    audio_features(i)
                    request_count+=1
                    if request_count % 5 == 0:
                        print(str(request_count) + " playlists completed")
                        time.sleep(np.random.uniform(sleep_min, sleep_max))
                        print('Loop #: {}'.format(request_count))
                        print('Elapsed Time: {} seconds'.format(time.time() - start_time))

                dic_df = {}
                dic_df['album'] = []
                dic_df['track_number'] = []
                dic_df['id'] = []
                dic_df['name'] = []
                dic_df['uri'] = []
                dic_df['acousticness'] = []
                dic_df['danceability'] = []
                dic_df['energy'] = []
                dic_df['instrumentalness'] = []
                dic_df['liveness'] = []
                dic_df['loudness'] = []
                dic_df['speechiness'] = []
                dic_df['tempo'] = []
                dic_df['valence'] = []
                dic_df['popularity'] = []
                # agregar mood, key

                for album in spotify_albums: 
                    for feature in spotify_albums[album]:
                        dic_df[feature].extend(spotify_albums[album][feature])
                        
                len(dic_df['album'])
                df = pd.DataFrame.from_dict(dic_df)

                final_df = df.sort_values('popularity', ascending=False).drop_duplicates('name').sort_index()
                final_df = final_df.to_json(orient='records')
                
            except:
                artist = None
                final_df = None
            finally:
                request.session['artist'] = artist
                request.session['final_df'] = final_df

                context = {
                    'artist': artist, 
                    'final_df': final_df 
                }

            return render(request, 'output.html', context)
    else:
            form = forms.InputForm()

def download_artist(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Artis Results.csv"'
    artist = request.session.get('artist')
    writer = csv.writer(response)
    writer.writerow(['Name', 'Spotify ID', 'Genders', 'Followers', 'Popularity', 'External url'])
    writer.writerow([artist['name'], artist['id'], artist['genres'], artist['followers']['total'], artist['popularity'], artist['external_urls']['spotify']])
    
    return response

def download_info(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Search Results.csv"'
    data = json.loads(request.session.get('final_df'))
    df = pd.json_normalize(data)
    df.to_csv(path_or_buf=response,sep=',',index=False)
    return response

# Imports used for file locations, Spotify communication and file downloads
import codecs
import os
import spotipy
from spotipy.oauth2 import SpotifyPKCE 
import spotipy.util
import wget
import pprint



# Fields used for directories, user choice, and accessing the Spotify API
dirPath = os.getcwd()
exportPath = os.path.join(dirPath, "Exports")
folderCache = [ "Exports", ".cache" ]
folders = [ "Artists", "Users", "Albums", "Tracks", "Media", "Media\Pictures", "Media\Song Previews" ]
directories = []
sp = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id="72f54fa540c743268595191fc3a153d0", redirect_uri="http://localhost:5000/callback"))
choice = ""



# A method to write either user or artist information depending on what is passed in
def writeProfileContents(account, isArtist):
    try:
        information = ""
        
        # Artists have a 'name' and 'popularity' field inside the response object
        # Versus users that just have 'display_name'
        if isArtist:
            print(f"Writing contents for {account['name']}\n")
            file = codecs.open(os.path.join(directories[2], f"{account['name']}.txt"), 'w', 'utf-8')
            information += f"Name: {account['name']}\n\n"
            information += f"Popularity: {account['popularity']}\n\n"
            print(f"Downloading Profile Picture URL")
            wget.download(account['images'][0]['url'], os.path.join(directories[7], f"{account['name']}_Avatar.png"))
            print("\n")
        else:
            print(f"Writing contents for {account['display_name']}\n")
            file = codecs.open(os.path.join(directories[3], f"{account['display_name']}.txt"), 'w', 'utf-8')
            information += f"Display Name: {account['display_name']}\n\n"
            print(f"Downloading Profile Picture URL")
            wget.download(account['images'][0]['url'], os.path.join(directories[7], f"{account['display_name']}_User__Avatar.png"))
            print("\n")
        
        information += f"Followers: {account['followers']['total']}\n\n"
        information += f"Type: {account['type']}\n\n"
        information += f"ID: {account['id']}\n\n"
        information += f"Avatar URL: {account['images'][0]['url']}\n\n"
        information += f"Profile URL: {account['external_urls']['spotify']}\n\n"
        information += f"Profile URI: {account['uri']}\n\n"
        file.write(information)
        file.close()
        print("Finished downloading the requested contents!")
    except Exception as e:
        print(f"There was an error trying to write the requested contents\nError: {e}")
        input("\nPress any key to quit")
        quit()



# A method to write track and album information depending on what is passed in
def writeAndDownloadSongContents(content, isAlbum):
    try:
        print(f"Downloading contents for {content['name']}\n")
        information = f"Name: {content['name']}\n\n"
        information += f"Popularity: {content['popularity']}\n\n"
        information += f"Artists:\n"
        for value in content['artists']:
            information += f"- {value['name']}\n"
        information += "\n"
        information += f"Type: {content['type']}\n\n"
        information += f"ID: {content['id']}\n\n"
        information += f"Content URI: {content['uri']}\n\n"
        information += f"Spotify URL: {content['external_urls']['spotify']}\n\n"
        information += f"Spotify API URL: {content['href']}\n\n"

        # Albums have all this information attached to it versus a sole track
        if isAlbum:
            information += f"Artwork URL: {content['images'][0]['url']}\n\n"
            information += f"Release Date: {content['release_date']}\n\n"
            information += f"Album Type: {content['album_type']}\n\n"
            information += f"Is Explicit: {content['tracks']['items'][0]['explicit']}\n\n"
            information += f"Total Tracks: {content['total_tracks']}\n\n"
            information += f"Label: {content['label']}\n\n"
            information += f"Copyright (C): {content['copyrights'][0]['text']}\n\n"
            information += f"Copyright (P): {content['copyrights'][1]['text']}\n\n"
            print(f"Downloading Artwork for {content['name']}")
            wget.download(content['images'][0]['url'], os.path.join(directories[7], f"{content['name']}_Album.png"))
            print("\n")
            file = codecs.open(os.path.join(directories[4], f"{content['name']}.txt"), 'w', 'utf-8')
        else:
            information += f"Artwork URL: {content['album']['images'][0]['url']}\n\n"
            information += f"Preview URL: {content['preview_url']}\n\n"
            print(f"Downloading Artwork for {content['name']}")
            wget.download(content['album']['images'][0]['url'], os.path.join(directories[7], f"{content['name']}_Track.png"))
            print("\n")
            print(f"Downloading Track Preview for {content['name']}")
            wget.download(content['preview_url'], os.path.join(directories[8], f"{content['name']}_Preview.mp3"))
            print("\n")
            file = codecs.open(os.path.join(directories[5], f"{content['name']}.txt"), 'w', 'utf-8')

        information += f"Content Availability (ISO Alpha-2 3166 Format): {content['available_markets']}\n\n"
        file.write(information)
        file.close()
        print("Finished downloading the requested contents!")
    except Exception as e:
        print(f"There was an error trying to write the requested contents\nError: {e}")
        input("\nPress any key to quit")
        quit()



# A method to read the users input for the URL and format it
def checkInput(choice):
    url = input(f"Enter in the URL of the {choice} here: ")
    try:
        beginIndex = url.rfind('/') + 1
        endIndex = url.index("?si")
        if not choice == "artist":
            url = url[beginIndex:endIndex]
        else:
            url = f"spotify:{choice}:{url[beginIndex:endIndex]}"
    except ValueError as ve:
        print(f"Please enter in a proper Spotify URL to continue!\nError: {ve}")
        quit()
    except Exception as e:
        print(f"There was an error trying to format the URL\nError: {e}")
        quit()
    return url



def removeCache():
    if os.path.exists(directories[1]):
        os.remove(directories[1])



def main():
    # Display prompt to the user and read the choice they make
    global choice  # Make a global variable to track what the user inputs so if they type "quit", the program quits
    choice = input("\nWhat would you like to get information for?\nYour options are: \"track\", \"album\", \"artist\", \"user\", and \"quit\"\n\nYour Input: ")
    choice = choice.lower()

    # Depending on what the user wants, the program will perform the task
    if choice == "track":
        url = checkInput(choice)
        try:
            track = sp.track(url)
        except Exception as e:
            print(f"There was an error trying to get the track information\nError: {e}")
            removeCache()
            input("\nPress any key to quit")
            quit()
    
        writeAndDownloadSongContents(track, False)
        # pprint.pprint(track)
        print(f"\nFinished writing all the {choice}'s information")
    elif choice == "album":
        url = checkInput(choice)
        try:
            album = sp.album(url)
        except Exception as e:
            print(f"There was an error trying to get the track information\nError: {e}")
            removeCache()
            input("\nPress any key to quit")
            quit()
    
        writeAndDownloadSongContents(album, True)
        # pprint.pprint(album)
        print(f"\nFinished writing all the {choice}'s information")
    elif choice == "artist":
        url = checkInput(choice)
        try:
            artist = sp.artist(url)
        except Exception as e:
            print(f"There was an error trying to get the artist information\nError: {e}")
            removeCache()
            input("\nPress any key to quit")
            quit()

        writeProfileContents(artist, True)
        print(f"\nFinished writing all the {choice}'s information")
    elif choice == "user":
        url = checkInput(choice)
        try:
            user = sp.user(url)
        except Exception as e:
            print(f"There was an error trying to get the user profile information\nError: {e}")
            removeCache()
            input("\nPress any key to quit")
            quit()

        writeProfileContents(user, False)
        print(f"\nFinished writing all the {choice}'s information")
    elif choice == "quit":
        print("\nQuitting program now")
        quit()
    else:
        print("\nPlease enter a valid selection to continue!")



# Append all directories to create down below
for folder in folderCache:
    directories.append(os.path.join(dirPath, folder))
for folder in folders:
    directories.append(os.path.join(exportPath, folder))

# Make the Exports folder and the subfolders when the script is run
try:
    for element in directories:
        if not os.path.exists(element):
            os.mkdir(element)
except Exception as e:
    print(f"There was an error trying to create the required folders\nError: {e}")
    c = input("\nPress any key to quit")
    quit()

print("Login to your Spotify profile when using this application. (Spotify's API does not allow un-authorized requests)")
while True:
    main()
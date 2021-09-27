# Used for general purposes (path checks, directory creation, etc.)
import os

# Used for communicating with Spotify's API (including authentication and other utilities)
import spotipy
from spotipy.oauth2 import SpotifyPKCE 
import spotipy.util

# Temporary import for debug purposes
import pprint;



# Fields that define where paths are as well as the spotify client and for repeating the program
dirPath = os.getcwd()
exportPath = os.path.join(dirPath, "Exports")
artistPath = os.path.join(exportPath, "Artists")
userPath = os.path.join(exportPath, "Users")
albumPath = os.path.join(exportPath, "Albums")
trackPath = os.path.join(exportPath, "Tracks")
cachePath = os.path.join(dirPath, ".cache")
sp = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id="72f54fa540c743268595191fc3a153d0", redirect_uri="https://webpages.uncc.edu/hquresh1/SpotifyInfoRedirect/callback/"))
choice = ""



# A method to write either user or artist information depending on what is passed in
def writeProfileContents(account, isArtist):
    try:
        # Artists have a 'name' and 'popularity' field inside the response object
        # Versus users that just have 'display_name'
        if not isArtist:
            file = open(os.path.join(userPath, f"{account['display_name']}.txt"), 'w')
            file.write(f"Display Name: {account['display_name']}\n\n")
        else:
            file = open(os.path.join(artistPath, f"{account['name']}.txt"), 'w')
            file.write(f"Name: {account['name']}\n\n")
            file.write(f"Popularity: {account['popularity']}\n\n")

        file.write(f"Followers: {account['followers']['total']}\n\n")
        file.write(f"Type: {account['type']}\n\n")
        file.write(f"ID: {account['id']}\n\n")
        file.write(f"Avatar URL: {account['images'][0]['url']}\n\n")
        file.write(f"Profile URL: {account['external_urls']['spotify']}\n\n")
        file.write(f"Profile URI: {account['uri']}\n\n")
        file.close()
    except Exception as e:
        print(f"There was an error trying to write the requested contents\nError: {e}")
        input("\nPress any key to quit")
        quit()



# A method to write track and album information depending on what is passed in
def writeSongContents(content, isAlbum):
    try:
        if not isAlbum:
            file = open(os.path.join(trackPath, f"{content['name']}.txt"), 'w')
        else:
            file = open(os.path.join(albumPath, f"{content['name']}.txt"), 'w')
        file.write(f"Name: {content['name']}\n\n")
        file.write(f"Popularity: {content['popularity']}\n\n")

        if isAlbum:
            file.write(f"Release Date: {content['release_date']}\n\n")
            file.write(f"Album Type: {content['album_type']}\n\n")
            file.write(f"Is Explicit: {content['tracks']['items'][0]['explicit']}\n\n")

        file.write(f"Type: {content['type']}\n\n")
        file.write(f"ID: {content['id']}\n\n")
        file.write(f"Artwork URL: {content['images'][0]['url']}\n\n")

        if not isAlbum:
            file.write(f"Preview URL: {content['preview_url']}\n\n")
        else:
            file.write(f"Album URI: {content['uri']}\n\n")
            file.write(f"Copyright (C): {content['copyrights'][0]['text']}\n\n")
            file.write(f"Copyright (P): {content['copyrights'][1]['text']}\n\n")

        file.write(f"Available Markets (ISO 3166-1 alpha-2 Code): {content['available_markets']}\n\n")
        file.close()
    except Exception as e:
        print(f"There was an error trying to write the requested contents\nError: {e}")
        input("\nPress any key to quit")
        quit()



# A method to read the users input for the URL and format it
def checkInput(choice):
    url = input(f"Enter URL of {choice} here: ")
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


def main():
    # Display prompt to the user and read the choice they make
    global choice  # Make a global variable to track what the user inputs so if they type "quit", the program quits
    choice = input("\nWhat would you like to get information for?\nYour options are: \"track\", \"album\", \"artist\", \"user\"\n\nYour Input: ")
    choice = choice.lower()

    # Depending on what the user wants, the program will perform the task
    if choice == "track":
        url = checkInput(choice)

        try:
            track = sp.track(url)
        except Exception as e:
            print(f"There was an error trying to get the track information\nError: {e}")
            if os.path.exists(cachePath):
                os.remove(cachePath)
            input("\nPress any key to quit")
            quit()
    
        pprint.pprint(track)
        # writeSongContents(track, False) - Temporary (researching the properties of a Track object)
    elif choice == "album":
        url = checkInput(choice)

        try:
            album = sp.album(url)
        except Exception as e:
            print(f"There was an error trying to get the track information\nError: {e}")
            if os.path.exists(cachePath):
                os.remove(cachePath)
            input("\nPress any key to quit")
            quit()
    
        writeSongContents(album, True)

        print(f"\nFinished writing all the album's information")
    elif choice == "artist":
        # Get the URL of the artist and format it into a URI
        url = checkInput(choice)
    
        # Get the artist from the URI above to obtain information for
        try:
            artist = sp.artist(url)
        except Exception as e:
            print(f"There was an error trying to get the artist information\nError: {e}")
            if os.path.exists(cachePath):
                os.remove(cachePath)
            input("\nPress any key to quit")
            quit()

        # Calls the method that will write the artist information to file
        writeProfileContents(artist, True)
    
        print(f"\nFinished writing all the artist's information")
    elif choice == "user":
        # Get the URL of the user profile and format it into a URI
        url = checkInput(choice)

        # Get the artist from the URI above to obtain information for
        try:
            user = sp.user(url)
        except Exception as e:
            print(f"There was an error trying to get the user profile information\nError: {e}")
            if os.path.exists(cachePath):
                os.remove(cachePath)
            input("\nPress any key to quit")
            quit()

        # Calls the method that will write the user information to file
        writeProfileContents(user, False)

        print(f"\nFinished writing all the user's information")
    else:
        print("\nPlease enter a valid selection to continue!")



 # Make the Exports folder and the Subfolders when the script is run
try:
    if not os.path.exists(exportPath):
        os.mkdir(exportPath)
    if not os.path.exists(artistPath):
        os.mkdir(artistPath)
    if not os.path.exists(userPath):
        os.mkdir(userPath)
    if not os.path.exists(albumPath):
        os.mkdir(albumPath)
    if not os.path.exists(trackPath):
        os.mkdir(trackPath)
except Exception as e:
    print(f"There was an error trying to create the \"Exports\" folder\nError: {e}")
    c = input("\nPress any key to quit")
    quit()

print("Login to your Spotify profile when using this application. (Spotify's API does not allow un-authorized requests)")
while not choice.lower() == "quit":
    print(choice)
    main()
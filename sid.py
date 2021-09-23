import os
import spotipy
from spotipy.oauth2 import SpotifyPKCE
import spotipy.util

dirPath = os.getcwd()
exportPath = os.path.join(dirPath, "Exports")
artistPath = os.path.join(exportPath, "Artists")
userPath = os.path.join(exportPath, "Users")
albumPath = os.path.join(exportPath, "Albums")
cachePath = os.path.join(dirPath, ".cache")
sp = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id="72f54fa540c743268595191fc3a153d0", redirect_uri="https://webpages.uncc.edu/hquresh1/SpotifyInfoRedirect/callback/"))

print("Login to your Spotify profile when using this application. (Spotify's API does not allow un-authorized requests)")

choice = input("What would you like to get information for?\nYour options are: \"track\", \"album\", \"artist\", \"user\"\n\nYour Input: ")
choice = choice.lower()

if choice == "track":
    quit() # Not implemented yet
elif choice == "album":
    quit() # Not implemented yet
elif choice == "artist":
    url = input("Enter URL of artist here: ")
    try:
        beginIndex = url.index("t/") + 2
        endIndex = url.index("?si")
        url = f"spotify:{choice}:{url[beginIndex:endIndex]}"
    except ValueError as ve:
        print(f"Please enter in a proper Spotify URL to continue!\nError: {ve}")
        quit()
    except Exception as e:
        print(f"There was an error trying to format the URL\nError: {e}")
        quit()
        
    try:
        artist = sp.artist(url)
    except Exception as e:
        print(f"There was an error trying to get the artist information\nError: {e}")
        if os.path.exists(cachePath):
            os.remove(cachePath)
        quit()

    if not os.path.exists(artistPath):
        os.mkdir(artistPath)

    file = open(os.path.join(artistPath, f"{artist['name']}.txt"), 'w')
    file.write(f"Name: {artist['name']}\n")
    file.write(f"Followers: {artist['followers']['total']}\n")
    file.write(f"Popularity: {artist['popularity']}\n")
    file.write(f"Type: {artist['type']}\n")
    file.write(f"ID: {artist['id']}\n")
    file.write(f"Artist Avatar URL: {artist['images'][0]['url']}\n")
    file.write(f"Artist Profile URL: {artist['external_urls']['spotify']}\n")
    file.write(f"Artist Profile URI: {artist['uri']}\n")
    file.close()
    
    print(f"\nFinished writing all the artist's information")
    quit()
elif choice == "user":
    url = input("Enter URL of user here: ")
    try:
        beginIndex = url.index("r/") + 2
        endIndex = url.index("?si")
        url = url[beginIndex:endIndex]
    except ValueError as ve:
        print(f"Please enter in a proper Spotify URL to continue!\nError: {ve}")
        quit()
    except Exception as e:
        print(f"There was an error trying to format the URL\nError: {e}")
        quit()

    try:
        user = sp.user(url)
    except Exception as e:
        print(f"There was an error trying to get the artist information\nError: {e}")
        if os.path.exists(cachePath):
            os.remove(cachePath)
        quit()

    if not os.path.exists(userPath):
        os.mkdir(userPath)

    file = open(os.path.join(userPath, f"{user['display_name']}.txt"), 'w')
    file.write(f"Display Name: {user['display_name']}\n")
    file.write(f"Followers: {user['followers']['total']}\n")
    file.write(f"Type: {user['type']}\n")
    file.write(f"ID: {user['id']}\n")
    file.write(f"User Avatar URL: {user['images'][0]['url']}\n")
    file.write(f"User Profile URL: {user['external_urls']['spotify']}\n")
    file.write(f"User Profile URI: {user['uri']}\n")
    file.close()

    print(f"\nFinished writing all the user's information")
    quit()

else:
    print("Please enter a valid selection to continue!")
    quit()

    

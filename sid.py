# Used for general purposes (path checks, directory creation, etc.)
import os

# Used for communicating with Spotify's API (including authentication and other utilities)
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



# A method to write either user or artist information depending on what is passed in
def writeProfileContents(account, isArtist):
    try:
        if not isArtist:
            file = open(os.path.join(userPath, f"{account['display_name']}.txt"), 'w')
            file.write(f"Display Name: {user['display_name']}\n")
        else:
            file = open(os.path.join(artistPath, f"{account['name']}.txt"), 'w')
            file.write(f"Name: {artist['name']}\n")
            file.write(f"Popularity: {artist['popularity']}\n")

        file.write(f"Followers: {account['followers']['total']}\n")
        file.write(f"Type: {account['type']}\n")
        file.write(f"ID: {account['id']}\n")
        file.write(f"Avatar URL: {account['images'][0]['url']}\n")
        file.write(f"Profile URL: {account['external_urls']['spotify']}\n")
        file.write(f"Profile URI: {account['uri']}\n")
        file.close()
    except Exception as e:
        print(f"There was an error trying to write the requested contents\nError: {e}")



# Make the Exports folder and the Subfolders when the script is run
try:
    if not os.path.exists(exportPath):
        os.mkdir(exportPath)
    if not os.path.exists(artistPath):
        os.mkdir(artistPath)
    if not os.path.exists(userPath):
        os.mkdir(userPath)
except Exception as e:
    print(f"There was an error trying to create the \"Exports\" folder\nError: {e}")
    quit()

# Display prompt to the user and read the choice they make
print("Login to your Spotify profile when using this application. (Spotify's API does not allow un-authorized requests)")

choice = input("What would you like to get information for?\nYour options are: \"track\", \"album\", \"artist\", \"user\"\n\nYour Input: ")
choice = choice.lower()

# Depending on what the user wants, the program will perform the task
if choice == "track":
    quit() # Not implemented yet
elif choice == "album":
    quit() # Not implemented yet
elif choice == "artist":
    # Get the URL of the artist and format it into a URI
    url = input("Enter URL of artist here: ")
    try:
        beginIndex = url.rfind('/') + 1
        endIndex = url.index("?si")
        url = f"spotify:{choice}:{url[beginIndex:endIndex]}"
    except ValueError as ve:
        print(f"Please enter in a proper Spotify URL to continue!\nError: {ve}")
        quit()
    except Exception as e:
        print(f"There was an error trying to format the URL\nError: {e}")
        quit()
    
    # Get the artist from the URI above to obtain information for
    try:
        artist = sp.artist(url)
    except Exception as e:
        print(f"There was an error trying to get the artist information\nError: {e}")
        if os.path.exists(cachePath):
            os.remove(cachePath)
        quit()

    # Calls the method that is responsible 
    writeProfileContents(artist, True)
    
    print(f"\nFinished writing all the artist's information")
    quit()
elif choice == "user":
    url = input("Enter URL of user here: ")
    try:
        beginIndex = url.rfind('/') + 1
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

    writeProfileContents(user, False)

    print(f"\nFinished writing all the user's information")
    quit()

else:
    print("Please enter a valid selection to continue!")

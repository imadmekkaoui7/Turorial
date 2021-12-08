import json
import requests
import base64
import re

""" These are your github credentials """

username = 'imadmekkaoui7'
token = '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'

# create a re-usable session object with the user creds in-built
gh_session = requests.Session()
gh_session.auth = (username, token)

""" The request returns the contents of the repo 
    Use can use this model : https://apt.github.com/repos/<user>/<repo name>/contents/"
"""
url = 'https://api.github.com/repos/ironhack-datalabs/scavenger/contents/'
search = json.loads(gh_session.get(url).text)


def base64ToString(b):
    """ This function decodes from base64 to string, you'll need it because the contents of files are coded in base64
        You need it to be able to read these contents as normal strings
    """
    return base64.b64decode(b).decode('utf-8')


""" This is dictionary that will contain key-value pairs in which the key is the file number 
    and the value is the word contained in each file
    
"""
joke_dict = {}

""" This loop goes through every folder in the repo """
for item in search:

    """ this condition makes sure the item is a directory and not a .gitignore file """
    if item["type"] == "dir":

        """ for each folder, I extract the url that I use to query its contents """
        url = item["url"]
        folder = json.loads(gh_session.get(url).text)

        """ This loop goes through each file in every folder """
        for file in folder:
            name = file["name"]

            """ I check if the file name contains the word 'scavenger' """
            if "scavenger" in name:

                """ I use this regular expression to extract the number from the name of the file
                    This number represents the order of each word in the final joke.
                    I then convert the result matched by the regex into an int
                """
                name = int(re.search("\d+", name).group(0))

                """ I use the file URL to query its contents"""
                url = file["url"]
                file_content = json.loads(gh_session.get(url).text)
                content = file_content["content"]
                content = base64ToString(content)

                """ Once I have the word and the int that represents its order in the joke
                    I add the pair the the dictionary 
                """
                joke_dict[name] = content.rstrip("\n")


""" 
    In this final step, I build the joke from the dictionary, I don't have to sort anything
    since the key of every key-value pair is the order of the word in the joke.
    All we need to do, is use a loop with an index that rages from 0 to the length of the dictionary
    which represents the number of words in the joke.
"""

joke = ""

for i in range(1, len(joke_dict)+1):
    joke += joke_dict[i].rstrip('\n') + " "

print(joke)

""" It might take a bit long to finish since it queries the API multiple times.
    I hope this was clear and helpful
"""









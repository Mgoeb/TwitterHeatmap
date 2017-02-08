
import json, os
from twython import TwythonStreamer

Directory = "local_directory_name"

os.chdir(Directory)


APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''




class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        try:
            if data['coordinates'] is not None:
                #print(data['text'], data['source'])
                with open('tweetsourcejsondict.json', 'a') as f:
                    f.write(json.dumps({data['id']: data['source']}))
                    f.write('\n')

        #some tweets do not have coordinates key, will skip these
        except (KeyError, AttributeError):
            pass

    def on_error(self, status_code, data):
        with open('errors.txt', 'a') as f:
            f.write('error: {0}: {1}'.format(status_code, data))



stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


USA_location = "-125.0011, 24.9493, -66.9326, 49.5904"

stream.statuses.filter(locations=USA_location)



tweets = []

for line in open('tweetslocationjsonlist.json', 'r'):
    tweets.append(json.loads(line))

latlong = []

#need to reverse longitude latitude before we load into google maps
latlong.append([[t[1], t[0]] for t in [tweet['coordinates'] for tweet in tweets]])
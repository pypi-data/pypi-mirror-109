import requests
from logging import warnings
import json
from urllib.parse import quote

class pyepisodate:
    def __init__(self):
        self.base = 'https://episodate.com'
        pass

    def search(self, showname):
        sn = quote(showname)
        url = self.base + '/api/search?q={}&page=1'.format(sn)
        r = requests.get(url)
        j = json.loads(r.text)
        res = [show['permalink'] for show in j['tv_shows']]
        if(len(res) == 0):
            print('Error: no matches found for {}'.format('showname'))
            warnings.warn('Error: no matches found for {}'.format('showname'))
            return 1
        return res

    def popular(self):
        url = self.base + '/api/most-popular?page=1'
        r = requests.get(url)
        j = json.loads(r.text)
        pshows = [show['permalink'] for show in j['tv_shows']]
        return pshows

    def show(self, showname):
        shows = self.search(showname)
        if(len(shows) > 1 and not(showname in shows)):
            #print('Error: multiple matches found for \'{}\'. Please refine your search.'.format(showname))
            warnings.warn('Error: multiple matches found for \'{}\'. Please refine your search.'.format(showname))
            #print('Matches: {}'.format(', '.join(shows)))
            warnings.warn('Matches: {}'.format(', '.join(shows)))
            return 1
        url = self.base + '/api/show-details?q={}'.format(showname)
        r = requests.get(url)
        j = json.loads(r.text)['tvShow']
        class Show():
            def __init__(self):
                self.name = j['name']
                self.description = j['description'].replace('</b>', '').replace('<b>', '')
                self.start_date = j['start_date']
                self.country = j['country']
                self.status = j['status']
                self.runtime = j['runtime']
                self.network = j['network']
                self.genres = j['genres']
                self.rating = j['rating']
                self.countdown = j['countdown']
                self.episodes = j['episodes']
        return Show()

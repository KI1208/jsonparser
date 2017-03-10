# -*- coding: utf-8 -*-

import sys

def parse_json(config):
    # Initialize array
    # Create (num of movie) * (num of column) array
    arr = []
    for i in range(len(config)):
        try:
            arr[i].append({})
        except IndexError:
            arr.append({})
        except:
            print 'Unexpected Error:',sys.exc_info()[0]

    # Populate arr
    for idx,movie in enumerate(config):
        try:
            arr[idx].update({'title': movie.get('title')})
            arr[idx].update({'rank': movie.get('info').get('rank')})
            arr[idx].update({'genres': movie.get('info').get('genres')})
            arr[idx].update({'actors': movie.get('info').get('actors')})

            if movie.get('info').get('genres') and movie.get('info').get('actors'):
                arr[idx].update({'rowspan': max(len(movie.get('info').get('genres')),len(movie.get('info').get('actors')))})
            elif not movie.get('info').get('genres') and movie.get('info').get('actors'):
                arr[idx].update({'rowspan': len(movie.get('info').get('actors'))})
            elif movie.get('info').get('genres') and not movie.get('info').get('actors'):
                arr[idx].update({'rowspan': len(movie.get('info').get('genres'))})
            else:
                arr[idx].update({'rowspan': 1})
        except:
            print 'Unexpected Error:', sys.exc_info()[0]
            pass

    return arr



import pandas as pd
from pandas.io.json import json_normalize

def venues_explore(client,lat,lng, limit=100, verbose=0, sort='popular', radius=2000, offset=1, day='any',query=''):
    '''funtion to get n-places using explore in foursquare, where n is the limit when calling the function.
    This returns a pandas dataframe with name, city ,country, lat, long, address and main category as columns
    Arguments: *client, *lat, *long, limit (defaults to 100), radius (defaults to 2000), verbose (defaults to 0), offset (defaults to 1), day (defaults to any)'''
    # create a dataframe
    df_a = pd.DataFrame(columns=['Name', 
    'City', 
    'Latitude',
    'Longitude',
    'Category',
    'Address'])
    ll=lat+','+lng
    if offset<=50:
        for i_offset in range(0,offset):
            #get venues using client https://github.com/mLewisLogic/foursquare
            venues = client.venues.explore(params={'ll':ll,
            'limit':limit, 
            'intent' : 'browse',
            'sort':sort, 
            'radius':radius, 
            'offset':i_offset,
            'day':day,
            'query':query
            })
            venues=venues['groups'][0]['items']
            df_venues = pd.DataFrame.from_dict(venues)
            df_venues['venue'][0]
            #print('limit', limit, 'sort', sort, 'radius', radius)
            for i, value in df_venues['venue'].items():
                if verbose==1:
                    print('i', i, 'name', value['name'])
                venueName=value['name']
                try:
                    venueCity=value['location']['city']
                except:
                    venueCity=''
                venueCountry=value['location']['country']
                venueLat=value['location']['lat']
                venueLng=value['location']['lng']
                venueCountry=value['location']['country']
                try:
                    venueAddress=value['location']['address']
                except:
                    venueAddress=''
                venueCategory=value['categories'][0]['name']
                df_a=df_a.append([{'Name':venueName, 
                                   'City':venueCity,
                                   'Country':venueCountry,
                                   'Latitude':venueLat,
                                   'Longitude':venueLng,
                                   'Category':venueCategory,
                                   'Address':venueAddress
                                  }])
    else:
        print('ERROR: offset value per Foursquare API is up to 50. Please use a lower value.')
    return df_a.reset_index()
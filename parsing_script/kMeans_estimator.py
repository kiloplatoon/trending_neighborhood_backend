import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter, defaultdict
import math
from IPython import embed
# from .models import Neighborhoods

def cluster_and_rank(preferences=None):
  # might refactor the preferences to accept dictionary so it's order independent
  """
  if no preferences are given, then the results are the same methodology as the original
  preferences should be in list form in this order:
  [walkscore, grocery, parks, errands, drink, shopping, culture, schools, transit, bike]
  """
  # consider changing file manipulation to django query if this is incorporated in the backend
  filename = 'zillow_city_scrapes_converted'

  with open(f'./{filename}.json') as f:
    # django query for data (add filter if cities are added):
    # data = Neighborhoods.all()
    data = json.load(f)
    walkscore = []
    grocery = []
    parks = []
    errands = []
    drink = []
    shopping = []
    culture = []
    schools = []
    transit = []
    bike = []


  for key, value in enumerate(data):
      walkscore.append(value['breakdown']['Walkability'])
      grocery.append(value['breakdown']['Groceries'])
      parks.append(value['breakdown']['Parks'])
      errands.append(value['breakdown']['Errands'])
      drink.append(value['breakdown']['Restaurants and Bars'])
      shopping.append(value['breakdown']['Shopping'])
      culture.append(value['breakdown']['Entertainment'])
      schools.append(value['breakdown']['Schools'])
      transit.append(value['breakdown']['Public Transit'])
      bike.append(value['breakdown']['Biking'])

  loc = []


  for index in range(0, len(walkscore)):
    loc.append([walkscore[index], grocery[index], parks[index], errands[index], drink[index], shopping[index], culture[index], schools[index], transit[index], bike[index]])

  # take input preferences and adjust the loc scores
  if preference != None:
    for entry_index in range(len(loc)):
      for pref_index in range(len(preference)):
        loc[entry_index][pref_index] *= preference[pref_index] 


  clustered_data = np.array(loc)

  total_clusters = 11
  clusters = KMeans(n_clusters=total_clusters).fit(clustered_data)
  cluster_centers = clusters.cluster_centers_
  cluster_labels=clusters.predict(clustered_data)

  # Compute cluster distances
  cluster_distances = []
  for center in cluster_centers:
    sum = 0
    for point in center:
      sum += (point ** 2)
    cluster_distances.append(math.sqrt(sum))

  distance_label_zip = list(zip(range(total_clusters),cluster_distances))
  distance_label_zip_sorted = sorted(distance_label_zip, key = lambda entry: entry[1])
  sorted_labels = [item[0] for item in distance_label_zip_sorted]

  for index in range(len(data)):
    data[index]['Overall Score'] = sorted_labels.index(cluster_labels[index])*10

  # output = []

  # embed()
  with open(f'./{filename}_output.json', 'w') as outfile:
      json.dump(data, outfile)
  
  return data
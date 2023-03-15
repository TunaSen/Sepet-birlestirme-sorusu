import random
import csv
import pandas as pd
from sklearn.cluster import KMeans
from geopy.distance import geodesic
import warnings




def randomOLustur(n):
    center_lat = 41.1085#Maslak konum
    center_lon = 29.0301

    with open("geocode.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["geocode", "latitude", "longitude"])
        for i in range(n):
            lat = random.uniform(center_lat - 0.02, center_lat + 0.02)
            lon = random.uniform(center_lon - 0.02, center_lon + 0.02)
            writer.writerow([f"Point {i + 1}", lat, lon])


def sepetOlustur(kumeSayisi):
    warnings.filterwarnings('ignore')
    data = pd.read_csv("geocode.csv", verbose=0)

    kmeans = KMeans(n_clusters=kumeSayisi)
    kmeans.fit(data[["longitude", "latitude"]])

    centroids = kmeans.cluster_centers_

    sepetler = [[] for _ in range(kumeSayisi)]

    for i, row in data.iterrows():
        closest_centroid_idx = kmeans.predict([[row["longitude"], row["latitude"]]])[0]
        closest_centroid = centroids[closest_centroid_idx]
        distance = geodesic((row["longitude"], row["latitude"]), closest_centroid).km
        if distance <= 1:
            sepetler[closest_centroid_idx].append({"geocode:".encode('utf-8').decode('unicode_escape'):row["geocode"],"lng".encode('utf-8').decode('unicode_escape'):row["longitude"], "lat".encode('utf-8').decode('unicode_escape'):row["latitude"]})
        else:
            print("açıkta kalan",(row["longitude"], row["latitude"]))
            return  sepetOlustur(kumeSayisi+1)


    data=[]
    for i in range(len(sepetler)):
        data.append({"bucket":{"lng":centroids[i][0],"lat":centroids[i][1]},"noktalar":sepetler[i]})

    print("Gereken Küme sayısı:",kumeSayisi)
    for i in range(len(data)):
        print(f"sepet {i}:",data[i]['bucket'])
        for j in data[i]['noktalar']:
            print("---",j)
        print()


    return data


sepetOlustur(8)
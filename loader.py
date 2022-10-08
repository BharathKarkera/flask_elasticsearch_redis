import elasticsearch
import csv

es=elasticsearch.Elasticsearch(hosts=["http://localhost:9200"])

print(f"Connected to elastic search cluster: { es.info().body['cluster_name']}")


with open("/Users/bharathraj.karkera/Downloads/elastic_search_flask-main/car_details.csv" , "r") as file_object:

    reader_object= csv.reader(file_object)

    for i , car_details_row in enumerate(reader_object):
        document={
            "name": car_details_row[0],
            "engine": car_details_row[9],
            "year": car_details_row[1],
            "price": car_details_row[2],
            }
        es.index(index="cars",document=document)


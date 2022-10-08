import flask 
import elasticsearch
import flask_cors
import json
import redis

app=flask.Flask(__name__)
app.config["DEBUG"]=True
app.config["TOKEN"]="bharathkarkera"
app.secret_key = 'bharathkarkera'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = flask_cors.CORS(app, resources={r"/search": {"origins": "http://localhost:5000"}})

redis=redis.Redis(host='localhost',port=6379)

es=elasticsearch.Elasticsearch(hosts=["http://localhost:9200"])
print(f"Connected to Elastic search cluster: { es.info().body['cluster_name'] }")

MAX_SIZE=15 

@app.route('/')
def index_path():
    redis.incr("hits")
    flask.flash(str(int(redis.get("hits")))+"th hit to the site")
    return flask.render_template("index.html")
    
    

@app.route('/display',methods=["GET"])
def display_function():
    redis.incr("hits")
    return f'Hi This is a test webserver and this is your {int(redis.get("hits"))}th visit to the website'    


@app.route('/search',methods=["GET","POST"])
@flask_cors.cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def search_fun():
    query=flask.request.args["q"].lower()
    print(query)
    words=query.split(" ")
    print(words)
    
    #https://www.cleancss.com/python-beautify/
    
    clauses_list=    [  {
                            "span_multi": {
                                "match": {
                                    "fuzzy": {
                                        "name": {
                                            "value": i,
                                            "fuzziness": "AUTO"
                                        }
                                    }
                                }
                            }
                         }
                         for i in words
                      ]    
    
    payload={
            "bool": {
                "must": [{
                    "span_near": {
                        "clauses": clauses_list , "slop": 0 , "in_order": False
                    }
                }]
            }
    }
    
    
    #127.0.0.1:5000/search?q=bmw%20xl
    print(f"payload is : {payload}")

    response= es.search(index="cars", query=payload, size=MAX_SIZE)
    print(response)
    
    car_list=[]
    for i in response['hits']['hits']:
        print(i)
        car_list.append(i['_source']['name'])
    
    search_results=tuple([result['_source']['name'] for result in response['hits']['hits']])
    print(json.dumps(search_results))

    #return { "cars": search_results }

    
    return json.dumps(search_results)

app.run(host="0.0.0.0")


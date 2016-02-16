import falcon
import json
import pymongo
import datetime
from redis import Redis
from pymongo import MongoClient
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId

MongoConfig = {
    'IP': '192.168.99.100',
    'Port': 32769
}

class JournalResource:
    
    def on_get(self, req, resp):
        """ Handles GET requests """
        if req.get_param("id"):
            # Return a particular journal
            client = MongoClient(MongoConfig['IP'], MongoConfig['Port'])
            collection = client.db.journals
            result = {'journal': collection.find_one({"_id": ObjectId(req.get_param("id"))})}
        else:
            # Return all journals
            client = MongoClient(MongoConfig['IP'], MongoConfig['Port'])
            collection = client.db.journals.find()
            result = {'journals': [i for i in collection]}
        resp.body = json.dumps(result, sort_keys=True, indent=4, default=json_util.default)

    def on_post(self, req, resp):
        """ Handles POST requests """
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Error',
                ex.message)

        try:
            # Insert a particular journal
            journal = json.loads(raw_json, encoding='utf-8')
            journal['created'] = datetime.datetime.now()
            client = MongoClient(MongoConfig['IP'], MongoConfig['Port'])
            collection = client.db.journals
            journal_id = collection.insert_one(journal).inserted_id
            resp.body = 'Successfully inserted journal with id: %s' % journal_id
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Invalid JSON',
                'Could not decode the request body. The '
                'JSON was incorrect.')

    def on_put(self, req, resp):
        """ Handles PUT requests """
        if req.get_param("id"):
            try:
                raw_json = req.stream.read()
            except Exception as ex:
                raise falcon.HTTPError(falcon.HTTP_400,
                    'Error',
                    ex.message)
            
            try:
                # Update a particular journal
                journal = json.loads(raw_json, encoding='utf-8')
                journal['updated'] = datetime.datetime.now()
                client = MongoClient(MongoConfig['IP'], MongoConfig['Port'])
                collection = client.db.journals
                result = collection.find_one_and_update({"_id": ObjectId(req.get_param("id"))}, journal)
                resp.body = json.dumps(result, sort_keys=True, indent=4, default=json_util.default)
            except ValueError:
                raise falcon.HTTPError(falcon.HTTP_400,
                                       'Invalid JSON',
                                       'Could not decode the request body. The '
                                       'JSON was incorrect.')

    def on_delete(self, req, resp):
        """ Handles DELETE requests """
        if req.get_param("id"):
            # Delete a particular journal
            client = MongoClient(MongoConfig['IP'], MongoConfig['Port'])
            collection = client.db.journals
            result = collection.find_one_and_delete({"_id": ObjectId(req.get_param("id"))})
        resp.body = json.dumps(result, sort_keys=True, indent=4, default=json_util.default)


class JournalSuggestionResource:
    
    def on_get(self, req, resp):
        """ Handles GET requests """
        if req.get_param("q"):
            # Autocomplete endpoint for the API to serve the search bar for journals
            redis = Redis(host='redis', port=6379)
            client = MongoClient(MongoConfig['IP'], MongoConfig['Port'])
            collection = client.db.journals
            result = collection.find({"title": req.get_param("q")}, {_id:0, title: 1, created: 0, updated: 0})
            jsonresult = json.dumps(result, sort_keys=True, indent=4, default=json_util.default)
            # Store the resulting JSON string in a redis key
            redis.set('autocomplete', jsonresult)
            # Tell redis we want the key "autocomplete" to expire after 60 seconds
            redis.expire('autocomplete', 60)
        resp.body = jsonresult


app = falcon.API()
app.add_route('/v1/journals', JournalResource())
app.add_route('/v1/journals/suggest', JournalSuggestionResource())








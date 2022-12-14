import requests
import json
from .models import *
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {}".format(url))
    api_key = kwargs.get("api_key")
    try:
        if api_key:
            # Get with Authentication
            response = requests.get(
                url, 
                params=kwargs, 
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', api_key)
            )
        else:
            # Get without Authentication
            response = requests.get(
                url, 
                params=kwargs, 
                headers={'Content-Type': 'application/json'},
                #auth=HTTPBasicAuth('apikey', api_key)
            )
    except:
        print("Network exception occured")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except:
        print("Network exception occured")
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request (function resides in restapis.py) with a URL parameter
    json_result = get_request(url)
    if json_result:        
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                id=dealer_doc["id"],
                city=dealer_doc["city"],
                state = dealer_doc["state"],
                st=dealer_doc["st"],
                address=dealer_doc["address"],
                zip=dealer_doc["zip"],
                lat=dealer_doc["lat"],                
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                full_name=dealer_doc["full_name"]
            )                                                
            results.append(dealer_obj)

    return results

# - Call get_request() with specified arguments
def get_dealer_by_state(url, st):
    results = []    
    # Call get_request (function resides in restapis.py) with a URL parameter
    json_result = get_request(url, st=st)    
    if json_result:
        dealer_obj = CarDealer(
                id=json_result[0]["id"],
                city=json_result[0]["city"],
                state = json_result[0]["state"],
                st=json_result[0]["st"],
                address=json_result[0]["address"],
                zip=json_result[0]["zip"],
                lat=json_result[0]["lat"],                
                long=json_result[0]["long"],
                short_name=json_result[0]["short_name"],
                full_name=json_result[0]["full_name"]
            )
        results.append(dealer_obj)  
    return results

# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request (function resides in restapis.py) with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:        
        # Get the row list in JSON as dealers
        dealer_reviews = json_result["docs"]        
        # For each dealer object
        for review in dealer_reviews:                        
            # Create a DealerReview object with values in `doc` object
            dealer_review_obj = DealerReview(
                id=review["id"],
                car_make=review["car_make"],
                car_model = review["car_model"],
                car_year=review["car_year"],
                dealership=int(review["dealership"]),
                name=review["name"],
                purchase=bool(review["purchase"]),
                purchase_date=review["purchase_date"],
                review=review["review"],
                sentiment = ""               
            )   
            print(dealer_review_obj.review)
            sentiment = analyze_review_sentiments(dealer_review_obj.review)
            if sentiment["entities"]:
                print(sentiment["entities"][0]["sentiment"]["label"]) 
            results.append(dealer_review_obj)
 
    return results
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

    nlu_instance = get_NLU_instance()
    analyse_result = nlu_instance.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2)
        )
    ).get_result()

    print(analyse_result)
    return analyse_result

def get_NLU_instance():
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator    

    api_key = "4LbDfkHy7-K7a8Pv_Uk7w8_BYxWvVJPc86XfrOjPYr4r"
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/8f1bd032-307a-4282-879d-c0b0d84ef67b"

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-12-14',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)
    return natural_language_understanding
# - Get the returned sentiment label such as Positive or Negative




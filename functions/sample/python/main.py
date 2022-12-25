"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
"""from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):    
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()} """

#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#


from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(params):

    authenticator = IAMAuthenticator('GjkIcFXVi8ZRnl1FNSHAKZKUdplrzzQnt9LQHHOhDhR6')
    client = CloudantV1(authenticator=authenticator); 
    client.set_service_url('https://987f7de7-937c-4c7d-9327-3e3ff2412d22-bluemix.cloudantnosqldb.appdomain.cloud')

    try: 
        response = client.post_find(
            db='reviews',
            selector={'dealership': int(params['dealerId'])},
        ).get_result()
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type':'application/json'}, 
            'body': response 
        }        
        
    except:  
        return { 
            'statusCode': 404, 
            'message': 'Something went wrong'
        }
"""
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(params):
    
    authenticator = IAMAuthenticator("GjkIcFXVi8ZRnl1FNSHAKZKUdplrzzQnt9LQHHOhDhR6")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://987f7de7-937c-4c7d-9327-3e3ff2412d22-bluemix.cloudantnosqldb.appdomain.cloud")
    
    try:
        response = service.post_document(db='reviews', document=params["payload"]).get_result()
        
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        
        return result
    except:
        return {
        'statusCode': 404,
        'message': 'Something went wrong'
        }
        """

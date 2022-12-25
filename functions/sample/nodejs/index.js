
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
const authenticator = new IamAuthenticator({ apikey: 'GjkIcFXVi8ZRnl1FNSHAKZKUdplrzzQnt9LQHHOhDhR6' })
const cloudant = CloudantV1.newInstance({
    authenticator: authenticator
}); 
cloudant.setServiceUrl('https://987f7de7-937c-4c7d-9327-3e3ff2412d22-bluemix.cloudantnosqldb.appdomain.cloud');

let code = 404 ;

async function main(params) {
    if(params.st) {
        // return documents of given st.
        const result = await cloudant.postFind({ 
            db: 'dealerships', 
            selector: {
                st: params.st
            }
        })  
        
        if(result.result.docs.length > 0) {
            code = 200;
        } else {
            code = 404;
        }
        
        return  {
            statusCode: code,
            headers: { 'Content-Type': 'application/json' },
            body: result.result.docs
        }
    } else if(params.dealer_id) {
        const result = await cloudant.postFind({
            db: 'dealerships',
            selector: {
                id: parseInt(params.dealer_id)
            }
        })   
        if(result.result.docs.length > 0) {
            code = 200
        } else {
            code = 404
        }
        return  {
            statusCode: code,
            headers: { 'Content-Type': 'application/json' },
            body: result.result.docs
        }
    } else {
        // return all documents
        const result = await cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 20 })                
        
        if(result.result.rows.length > 0) {
            code = 200;
        } else {
            code = 404;
        }
        
        return  {
            statusCode: code,
            headers: { 'Content-Type': 'application/json' },
            body: result.result
        }
    }
    
}

/**
 * Get all databases
 

 const { CloudantV1 } = require("@ibm-cloud/cloudant");
 const { IamAuthenticator } = require("ibm-cloud-sdk-core");
 
 function main(params) {
   const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
   const cloudant = CloudantV1.newInstance({
     authenticator: authenticator,
   });
   cloudant.setServiceUrl(params.COUCH_URL);
 
   let dbList = getDbs(cloudant);
   return { dbs: dbList };
 }
 
 function getDbs(cloudant) {
   cloudant
     .getAllDbs()
     .then((body) => {
       body.forEach((db) => {
         dbList.push(db);
       });
     })
     .catch((err) => {
       console.log(err);
     });
 }
*/


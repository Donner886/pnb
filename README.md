###  Package
We use lambda layer technology to manage the python dependency libirary those are common to all lambda function.
and those libirary a lambda function used seperately are managed by itself.

### sam hello-world documentation: 
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html


# Build all functions and layers, and their dependencies
sam build
sam deploy --guided


### AWS apigateway authenticator
we use a lambda function to provide apigateway authenticator

### Lambda event object 
1, lambda event is a json string object. 

{'type': 'TOKEN', 
'authorizationToken': 'incoming-client-token',
 'methodArn': 'arn:{partition}:execute-api:[region]:[account_id]:[restApiId]/[stage]/[method]/[resourcePath]'}





# Build all functions and layers, and their dependencies
sam build
sam deploy --guided


### AWS apigateway authenticator
we use a lambda function to provide apigateway authenticator



from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from cognito_idp_actions import CognitoIdentityProviderWrapper
import boto3,json



app=Flask(__name__)
api = Api(app)



 ##change values to properties file

# def callboto_withparameterstore_accessinfo():
#     ###CALL parameter store for credentials
#     ssm_client=boto3.client("ssm",region_name='us-east-1')
#     get_response= ssm_client.get_parameter(Name='accesscredentials',WithDecryption=True)

#     accessvalues=get_response['Parameter']['Value']
#     accessjson=json.loads(accessvalues)
#     accesskey=accessjson.get('AccessKey')
#     secretkey=accessjson.get('SecretKey')

#     print("access key is "+accesskey)
#     print("secret key is "+secretkey)
#     cognito_idp_client=boto3.client("cognito-idp",region_name="us-east-1",aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
#     return cognito_idp_client


cognito_idp_client=boto3.client("cognito-idp",region_name="us-east-1")

user_pool_id= 'us-east-1_czJvUvPXp'
client_id='6mm560q3tmtsusj5rkjhokj035'

cog_wrapper = CognitoIdentityProviderWrapper(
        cognito_idp_client, user_pool_id, client_id)


class Hello(Resource):
    def get(self): 
  
        return jsonify({'message': 'hellooo2 artisan_service is up'}) 
  
    # Corresponds to POST request 
    def post(self): 
          
        data = request.get_json()     # status code 
        return jsonify({'data': data}), 201
    
class Login():
    def loginauth():
        data= request.get_json()
        required_fields=['username','password']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            error_message = f'Missing required fields: {", ".join(missing_fields)}'
            # print('**** '+error_message)
            
            error_message={
                "error":error_message
            }
            return error_message
        
        print(f"User {data['username']} signing in")
        username=data['username']
        password=data['password']
        confirmed= cog_wrapper.start_sign_in(username,password)

        print(f"Signup Response ::: "+str(confirmed))
        # if(confirmed==True):
        #     confirmed='SUCCESS,Code Confirmed'

        return jsonify({'responseMessage':confirmed})



class ResendConfirmationCode(Resource):
    def post(self):
        data= request.get_json()
        required_fields=['username']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            error_message = f'Missing required fields: {", ".join(missing_fields)}'
            # print('**** '+error_message)
            
            error_message={
                "error":error_message
            }
            return error_message
        
        print(f"User {data['username']} resending for token")
        username=data['username']
        confirmed= cog_wrapper.resend_confirmation(username)

        print(f"Resend Signup Code Response ::: "+str(confirmed))
        # if(confirmed==True):
        #     confirmed='SUCCESS,Code Confirmed'

        return jsonify({'responseMessage':confirmed})


class SignUpCodeConfirm(Resource):
    def post(self):
        data=request.get_json()

        required_fields=['token','username']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            error_message = f'Missing required fields: {", ".join(missing_fields)}'
            # print('**** '+error_message)
            
            error_message={
                "error":error_message
            }
            return error_message
        
        print(f"User {data['username']} token {data['token']} validation ")
        username=data['username']
        token= data['token']

        confirmed=cog_wrapper.confirm_user_sign_up(username,token)

        print(f"Token Response ::: "+str(confirmed))

        #setting succesful response if signup from aws is 200
        if(confirmed==True):
            confirmed='SUCCESS,Code Confirmed'

        return jsonify({'responseMessage':confirmed})






  
class SignupCognito(Resource):
    def post(self):
        signupdata=request.get_json()

        ##check if any of the fields are not present
        required_fields = ['username', 'password', 'email','phone_number']
        missing_fields = [field for field in required_fields if field not in signupdata]

        if missing_fields:
            error_message = f'Missing required fields: {", ".join(missing_fields)}'
            print('**** '+error_message)
            
            error_message={
                "error":error_message
            }
            return error_message

        

        user_name=signupdata['username']
        password= signupdata['password']
        email=signupdata['email']
        phone_number=signupdata['phone_number']
        print(f"Username {user_name} is confirmed and ready to use.")
        # print(f"password {password} is confirmed and ready to use.")
        print(f"email {email} is confirmed and ready to use.")
        print(f"phone_number {phone_number} is confirmed and ready to use.")
        
        confirmed=cog_wrapper.sign_up_user(user_name,password,email,phone_number)
        

        print(f"Signup Response ::: "+str(confirmed))

        #setting succesful response if signup from aws is 200
        if(confirmed==200):
            confirmed='SUCCESS,check email for confirmation code'

        return jsonify({'responseMessage':confirmed})


   
# another resource to calculate the square of a number 
class Square(Resource): 
  
    def get(self, num): 
  
        return jsonify({'square': num**2}) 
        
        
        
### SIGNUP API###
# class ArtisanSignup():
    
  
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Square, '/square/<int:num>') 
api.add_resource(SignupCognito,'/signup')
api.add_resource(SignUpCodeConfirm,'/signup/confirmtoken')
api.add_resource(ResendConfirmationCode,'/signup/resendsignuptoken')
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 
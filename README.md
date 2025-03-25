# login-manager
This is my first project, so im unfamiliar with the documentation process. The idea behind this project is to get me more comfortable with writing in different places, managing files, storing in json, data protections such as hashing, and general problem solving.

The idea is for the python script to handle two primary functions. Account login validation, and account creation. Both work with an external .json file to either check existing account details to validate login, or to check account details and update the accounts list in the event the user seeks to create the account. 

the os module was used for the generation of a unique salt. The hashlib module was used for the purpose of hashing and salting the password and salt for secure storage. The re module was used for the sole purpose of password validation. The json module was used to parse, write to, and save changes to the accounts.json file. The base64 module was used to store data in the base64 format.

The directory for this project comes with a json file preloaded with a couple of example accounts for your use.

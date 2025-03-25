import json # For working with a json file directory
import os # For changing working directory and salt generation
import re # For the validation of passwords
import hashlib # For the hashing and salting of password data
import base64 # For space efficient encoding of data to database

def useage():
    useaged = None
    attempts = 0

    # Establish while loop to validate useaged 
    while useaged not in {"1", "2"}:
        # Check number of attempts for early exit
        if attempts == 5:
            return None
        # Re-query and increment attempts counter
        useaged = input("Would you like to create an account or log in? (1/2): ")
        attempts +=1
    
    return int(useaged)


def acc_creation():
    username_input = input("Enter your new username: ")
    password_input = input("Enter your new password: ")
    # password criteria using re module
    pattern = r"^(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?/~`-]).{8,}$"

    try:
        # Open database file with relative location
        with open("accounts.json", "r+") as file:
            # Access data of the file with json.load
            data = json.load(file)

            while True:
                # Iterate over every "account" in file
                for account in data["Accounts"]:
                    # Check for same username
                    if account["Username"] == username_input:
                        print("Username is taken, please try again")
                        username_input = input("Enter your new username: ")
                break

            
            while True:
                # Check if password matches criteria with re.match
                if re.match(pattern, password_input):
                    break
                else:
                    print("Password must contain atleast 8 characters, one digit, and one special character")
                    password_input = input("Enter your new password: ")
            
            hashpass, salt = hashword(password_input)
            userdata = {
                "Username": username_input,
                "Password": hashpass,
                "Salt": salt
            }
            return userdata
            

            
    except FileNotFoundError:
        return 1
    
    except json.JSONDecodeError:
        return 2
    

def hashword(password_input):
    # Create the salt using os.urandom, size 16 bytes
    salt = os.urandom(16)
    # encode the password into bytes using .encode so we can pass it to the hashing algorithm
    password_input = password_input.encode()
    # hash and salt the password
    hashpass = hashlib.pbkdf2_hmac("sha256", password_input, salt, 100000)
    # change the byte format hashpass into base64
    hashpass64 = base64.b64encode(hashpass).decode("utf-8")
    return hashpass64, base64.b64encode(salt).decode("utf-8")


def login():
    try: 
        # Access file with open method, save it as variable file
        with open("accounts.json", "r+") as file:
            # Set the data parsing function to parse file at variable data

            data = json.load(file)

            # Get username and password
            username_input = input("Enter your username: ")
            password_input = input("Enter your password: ")

            the_salt = os.urandom(16)

            i = 0

            while i < 5:
                # For every account in the Accounts json category
                for account in data["Accounts"]:

                    # Search database for username match, grab the salt for hashing
                    if account["Username"] == username_input:
                        # Decode the salt back to bytes for the hashing function
                        the_salt = base64.b64decode(account["Salt"])
                        
                        #encode password input and salt into bytes to create the hash
                        hashpass = hashlib.pbkdf2_hmac("sha256", password_input.encode(), the_salt, 100000)

                        # encode fingerprint to base 64 for validation
                        if account["Password"] == base64.b64encode(hashpass).decode("utf-8"):
                            print("Login successful")
                            return 0

                    
                # Increment external loop and print error message
                i += 1
                print("Username or password was invalid. please try again")

                # Re-query for input for next loop
                username_input = input("Enter your username: ")
                password_input = input("Enter your password: ")

            # return error code if function unfulfilled
            return 1
        
        # Go over possible errors
    except FileNotFoundError:
        print("File not found")
        return 2
    
    except json.JSONDecodeError:
        print("Could not parse accounts file. It might be corrupted.")
        return 3
    
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
        return 4
    

def upload(userdata):
    # Open file
    with open("accounts.json", "r+") as file:
        # Access entire files data
        data = json.load(file)
        
        # Append the new data onto the json file
        data["Accounts"].append(userdata)

        # reset to the top of the file
        file.seek(0)
        # "overwrite" with already existing data, just to format it properly
        json.dump(data, file, indent = 4)

        # manually save updated data to disc
        file.flush()
        
        return 0


def main():
    # set correct working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Query user for desired useage
    useaged = useage()

    # Check for error code
    if useaged == None:
        print("Error code 0")
        return
    
    elif useaged == 1:
        # Save the userdata dictionary
        userdata = acc_creation()

        # Check for error codes
        if userdata == 1:
            print("File not found")
            return 1
        elif userdata == 2:
            print("Could not parse file, data might be corrupted")
            return 2
        
        # Pass dictionary to the upload function
        upload(userdata)

    elif useaged == 2:
        logincode = login()
        # Check for error codes
        if logincode == 1:
            print("Login failed, please re-run program")
            return 1
        elif logincode == 2:
            print("File not found")
            return 2
        elif logincode == 3:
            print("Could not parse file, data might be corrupted")
            return 3
        elif logincode == 4:
            print("Unexpected error occured")
            return 4
main()

import os

#Setting up controls file as multiple errors have occured during developement
print("Controlling folder setup..")
if os.path.exists("responses") == False:
    print(os.path.exists("responses"))
    os.mkdir("responses")
    print("Creating directories...")
if os.path.exists("localWindForcast") == False:
    os.mkdir("localWindForcast")
    print("Creating directories...")
    
def deleteAll():
    print("Removing directories....")
    os.rmdir("responses")
    os.rmdir("localWindForcast")
    print("Done!")
    
print("All good! Initliazing..")
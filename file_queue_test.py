import json

tweet1 = {
    "username": "a",
    "id": 234234
}
tweet2 = {
    "username": "b",
    "id": 76766
}
tweet3 = {
    "username": "c",
    "id": 76766
}
tweet4 = {
    "username": "d",
    "id": 76766
}
tweet5 = {
    "username": "e",
    "id": 76766
}

# Add to queue
def file_queue_add(tweet):
    
    # Open file in append mode
    with open('queue_test.txt', 'a') as file:
        
        # Write tweet to file
        file.write(str(tweet) + "\n")
    

# Get then remove first line of queue
def file_queue_pop():
    
    # Load queue file in read mode
    with open('queue_test.txt', 'r') as file:
                
        # All file data
        data = file.read().splitlines(True)
        
        # Get first line
        # Replace ' with "
        # Json decoder requires "
        # Remove \n
        first_line = data[0].replace("'", "\"").replace("\n", "")
        
        # Convert to dictionary
        tweet = json.loads(first_line)
        
    # Load file again but in write mode
    with open('queue_test.txt', 'w') as file:
        
        # Write data to file without first line
        file.writelines(data[1:])

    print(tweet["username"])


#file_queue_add(tweet1)
#file_queue_add(tweet2)
#file_queue_add(tweet3)
#file_queue_add(tweet4)
#file_queue_add(tweet5)
try:
    file_queue_pop()
except Exception as e:
    print(e)
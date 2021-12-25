import json

tweet1 = {
    "username": "FinessTV",
    "id": 234234
}
tweet2 = {
    "username": "Talal",
    "id": 76766
}

def file_queue_add():
    with open('queue.txt', 'a') as file:
        file.write(str(tweet1) + "\n")
        file.write(str(tweet2) + "\n")
    
def file_queue_pop():
    
    # Load queue file in read mode
    with open('queue.txt', 'r') as file:
                
        # All file data
        data = file.read().splitlines(True)
        
        # Get first line
        # Replace ' with "
        # Json decoder requires "
        first_line = data[0].replace("'", "\"")
        
        # Convert to dictionary
        tweet = json.loads(first_line)
        
    # Load file again but in write mode
    with open('queue.txt', 'w') as file:
        
        # Write data to file without first line
        file.writelines(data[1:])

    return tweet

file_queue_pop()
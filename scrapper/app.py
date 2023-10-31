def handler(event, context):
    print(event)
    message = 'Hello'
    return { 
        'message' : message
    }

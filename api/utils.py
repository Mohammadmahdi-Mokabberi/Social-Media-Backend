import uuid

def create_random_string():
    return uuid.uuid4().hex[:5]
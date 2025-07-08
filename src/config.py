def style(path):
    with open(path, 'r') as file:
        return file.read()


URL = 'http://127.0.0.1:9097'
secret = None
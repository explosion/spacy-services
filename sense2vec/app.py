'''Serve a sense2vec model over a GET request.'''
from sense2vec_service.service import load


APP = load()


if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8000, APP)
    httpd.serve_forever()

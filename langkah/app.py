from langkah_service.server import APP, get_model

get_model('fr')


if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8001, APP)
    httpd.serve_forever()

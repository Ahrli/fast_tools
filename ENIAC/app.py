from sanic import Sanic
from api import iquant_eniac
from sanic_openapi import swagger_blueprint # openapi_blueprint
# from api import jwt_api
from sanic import response
# from sanic_cors import CORS, cross_origin
# from sanic_jwt import Initialize

app = Sanic(__name__)
app.config.API_VERSION = '1.0.0'
app.config.API_TITLE = 'Eniac'
app.config.API_DESCRIPTION = 'iQuant Eniac Server'
app.config.API_CONSUMES_CONTENT_TYPES = ['application/json']
app.config.API_PRODUCES_CONTENT_TYPES = ['*/*']
app.config['API_SCHEMES'] = ['http', 'https']

# 蓝图加载
app.blueprint(iquant_eniac)
# app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

# # jwt验证
# Initialize(app, authenticate=jwt_api.authenticate)

# # 跨域
# CORS(app, resources={r"/api/*": {"origins": "*"}})
# # CORS(app)


@app.middleware('request')
async def print_on_request(request):
    if request.method == 'OPTIONS':
        return response.json(None)


@app.middleware('response')
async def prevent_xss(request, response):
    if 'X-Error-Code' not in dict(response.headers):
        response.headers['X-Error-Code'] = 0
    # response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "X-Custom-Header,content-type"
    response.headers["Access-Control-Allow-Method"] = "POST,GET"


if __name__ == '__main__':

    app.run(host='0.0.0.0',
            port=7778,
            # debug=True
            )

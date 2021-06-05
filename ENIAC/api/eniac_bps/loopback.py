# loop 计算
from sanic.blueprints import Blueprint
# from sanic import response
# from sanic_openapi import doc
# from kafka import KafkaProducer
# import json
# from ..models import StrategyDto

loop = Blueprint('loop', url_prefix='/loop', strict_slashes=True)


# # todo 上传文件
# @loop.put('/test', stream=True)
# @doc.summary('上传文件')
# async def loop_test(request):
#     result = ''
#     while True:
#         body = await request.stream.get()
#         if body is None:
#             break
#         result += body.decode('utf-8')
#     name = loop_cls_re(result)
#     ip_module = importlib.import_module(".", f"api.btscript.{name}")
#     ip_module_cls = getattr(ip_module, "demo")
#     cls_obj = ip_module_cls()
#     ip = cls_obj.get_ip()
#     return response.text(ip)

# todo 传输json消息
# @loop.route("/calculate", methods=["POST"], version='v1', name='Dto')
# @doc.summary('回测计算')
# @doc.description('接受回测数据进行回测计算')
# @doc.consumes(StrategyDto, location='body', required=True)
# async def post_data(request):
#     rule = request.json
#     btrun.startRun(rule)
#     return response.json(
#         {'message': 'Congratulations Your Strategy, Go Fly!'},
#         headers={'X-Served-By': 'sanic'},
#         status=200
#     )

# # todo 发送消息到kafka
# @loop.route("/testbt", methods=["POST"])#, version='v1', name='Dto')
# @doc.summary('发送Kafka回测消息')
# @doc.description('发送json消息到kafka提供回测计算')
# @doc.consumes(StrategyDto, location='body', required=True)
# async def post_data(request):
#     producer = KafkaProducer(bootstrap_servers= kafkaList)
#     producer.send('back_trader', json.dumps(request.json, ensure_ascii=False).encode('utf-8'))
#     producer.close()
#     return response.json(
#         {'message': 'Strategy Success To Kafka!'},
#         headers={'X-Served-By': 'sanic'},
#         status=200
#     )
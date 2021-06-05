#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pendulum
from sanic import Blueprint
from sanic import response
from sanic_openapi import doc
from ..models import APIVALIDATION
from ..eniacutil import ApiValidation
validation = Blueprint('validation', url_prefix='/validation', strict_slashes=True)


@validation.route('/api',methods=['POST'])
@doc.summary('api验证')
@doc.consumes(APIVALIDATION,location='body', content_type='JSON',  )
async def api_validation(request):
    status,code, mg= ApiValidation(request.json)

    return response.json(
        {'status': status,
         "code": code ,
         "message": mg,
          },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )
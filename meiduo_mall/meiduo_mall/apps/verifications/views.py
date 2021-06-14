import random
from django_redis import get_redis_connection
from rest_framework.response import Response

from django.shortcuts import render

# Create your views here.
# GET/sms_code/(?P<mobile>1[3-9]\d{9}/

from rest_framework import status
from rest_framework.views import APIView

from meiduo_mall.libs.yuntongxun.sms import CCP
from verifications import constants

# 获取日志器
# import logging
# logger = logging.getLogger('django')
import logging
logger = logging.getLogger('django')


class SMSCodeView(APIView):
    def get(self, request, mobile):
        # 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)

        # 保存短信验证码,以＇mobile'为key,以＂验证码内容＂为value
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        # 使用云通讯发送短信验证码
        expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        # try:
        #     res = CCP().send_template_sms(mobile, [sms_code, expires], constants.SEND_SMS_TEMP_ID)
        # except Exception as e:
        #     logger.error('发送短信异常：%s' % e)
        #     return Response({'message': '短信发送异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        #
        # if res != 0:
        #     return Response({'message': '短信发送失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 返回应答
        return Response({'message': 'ok'})
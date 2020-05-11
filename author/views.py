from django.views import View
from django.http import JsonResponse,HttpResponse
import datetime
import json
import time


from author.models import shouquanma
from utils.getRandom import random_str


class GenerateCode(View):

    def get(self, request):
        try:
            count = request.GET.get("count")
            expire = request.GET.get("time")
            auth_list = []
            for i in range(int(count)):
                code = shouquanma()
                code.authorization_code = random_str()
                auth_list.append(code.authorization_code)
                code.expire = int(expire)
                code.save()
            return HttpResponse(json.dumps({
                "status":"ok",
                "message":"授权码生成成功",
                "codeList":auth_list
            },ensure_ascii=False),charset="utf-8")
        except Exception as e:
            return HttpResponse(json.dumps({
                "status":"false",
                "message":"请求参数不正确"

            },ensure_ascii=False))


class ActiveCode(View):

    def get(self,request):
        device_id = request.GET.get("deviceid")
        authcode = request.GET.get("authcode")
        auth_code = shouquanma.objects.filter(authorization_code=authcode)
        if (len(auth_code)):
            authCode = auth_code[0]
            deviceId = authCode.device_id
            if deviceId:
                if deviceId == device_id:
                    return HttpResponse(json.dumps({
                            "status":"false",
                            "message":"请勿重复激活"

                    },ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({
                        "status":"false",
                        "message":"此授权码已经使用，请尝试其他授权码"
                    },ensure_ascii=False))
            else:
                authCode.is_active = 1
                authCode.device_id = device_id




            authCode.active_time = datetime.datetime.now()
            authCode.expire_time = datetime.datetime.now() + datetime.timedelta(days=authCode.expire)
            authCode.save()
            return HttpResponse(json.dumps({
                "status":"ok",
                "message":"设备激活成功",
                "deviceId":device_id
            },ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({
                "status":"false",
                "message":"参数不正确或授权码不存在"

            },ensure_ascii=False))



class GetvalueTime(View):

    def get(self,request):
            authcode = request.GET.get("authcode")
            authCode = shouquanma.objects.filter(authorization_code=authcode)
            if (len(authCode)):
                auth_code = authCode[0]
                device_id = auth_code.device_id
                if device_id:

                    res = {
                        "status":"ok",
                        "expire_time":time.mktime(auth_code.expire_time.timetuple()),
                        "active_time":time.mktime(auth_code.active_time.timetuple()),
                        "expire":auth_code.expire,
                        "message":"成功获取"
                    }
                    return HttpResponse(json.dumps(res,ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({
                        "status":"false",
                        "message":"此设备未被激活，请激活后再试"

                    },ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({
                    "status":"false",
                    "message":"参数错误或无此授权码"
                },ensure_ascii=False))


class SendHeart(View):

    def get(self, request):
        authcode = request.GET.get("authcode")
        authCode = shouquanma.objects.filter(authorization_code=authcode)
        auth_all = shouquanma.objects.all()
        if (len(authCode)):
            auth_code = authCode[0]
            device_id = auth_code.device_id
            heart_time = auth_code.heart_time
            initial_time = auth_code.initial_time
            if device_id:
                if (heart_time == initial_time):
                    auth_code.heart_time = datetime.datetime.now()
                    auth_code.online = 1
                    auth_code.save()

                for i in auth_all:
                    current_time = datetime.datetime.now()
                    code_heart = i.heart_time
                    if (code_heart == i.initial_time):
                        continue
                    if (current_time-datetime.timedelta(minutes=5)<=code_heart):
                        i.online = 1
                        i.save()
                    else:
                        i.online = 0
                        i.save()

                return HttpResponse(json.dumps({
                    "status":"ok"
                },ensure_ascii=False))
            else:
                return JsonResponse({
                    "status": "false",
                    "message": "此设备未被激活，请激活后再试"

                })
        else:
            return HttpResponse(json.dumps({
                "status":"false",
                "message":"授权码不存在或参数错误"
            },ensure_ascii=False))



















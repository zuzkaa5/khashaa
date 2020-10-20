# -*-coding: utf-8 -*-
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import timedelta
import json
import requests
from khashaa.models import Coffee
# Create your views here.

#host = "https://merchant-sandbox.qpay.mn"
host = "https://merchant.qpay.mn"
@csrf_exempt
def weburlA(request):
    if request.method == 'POST':
        ver = request.POST.get('ver')
        orderid = request.POST.get('orderid')
        machid = request.POST.get('machid')
        trackno = request.POST.get('trackno')
        name = request.POST.get('name')
        price = int(int(request.POST.get('price'))/100)
        channelid = request.POST.get('channelid')
        randstr = request.POST.get('randstr')
        timestamp1 = request.POST.get('timestamp')
        sign = request.POST.get('sign')


        cof = Coffee(ver=ver, orderid=orderid, machid=machid, trackno=trackno, name=name, price=price, channelid=channelid)
        cof.randstr = randstr
        cof.timestamp = timestamp1
        cof.sign = sign
        cof.save()
        cof.torderid = cof.id
        cof.save()

        import json
        access_token = qpay_auth()
        dic = qpay_inv(cof.torderid, access_token, name, cof.price)
        cof.qpay_invoice_id = dic['invoice_id']
        cof.access_token = access_token
        cof.save()
        torderid = cof.id

        if dic:
            code = 1
            msg = 'Qpay invoice is okay'
            twocode = dic['qr_text']
        else:
            code = 0
            msg = 'Can\'t connect to Qpay'
            twocode = ''
            cof.errinfo = 'Can\'t connect to Qpay'
            cof.save()

        resjson = {
            "orderid": orderid,
            "torderid": torderid,
            "code": code,  # 0 - failure , 1 - success
            "msg": msg,
            "twocode": twocode
        }
        restext = json.dumps(resjson)
        return HttpResponse(restext, content_type='application/json')
    else:
        return HttpResponse("invalid web request. iexpo")

@csrf_exempt
def weburlC(request):
    if request.method == 'POST':

        ver = request.POST.get('ver')
        orderid = request.POST.get('orderid')
        torderid = request.POST.get('torderid')
        machid = request.POST.get('machid')
        channelid = request.POST.get('channelid')
        randstr = request.POST.get('randstr')
        timestamp1 = request.POST.get('timestamp')
        sign = request.POST.get('sign')

        coffee = Coffee.objects.get(torderid=torderid, machid=machid)
        qpay_invoice_id = coffee.qpay_invoice_id
        dic = qpay_check(qpay_invoice_id, coffee.access_token)
        #return HttpResponse(dic)
        if dic['count'] == 1:
            code = 1
            paid = dic['paid_amount']
            coffee.qprice = paid
            coffee.code = 1
            coffee.save()
            msg = ''
        else:
            code = 2
            msg = ''

        resjson = {
            'orderid': orderid,
            'torderid': torderid,
            'code': code,
            'msg': msg
        }
        restext = json.dumps(resjson)
        return HttpResponse(restext, content_type='application/json')
    else:
        return HttpResponse("invalid web request. iexpo")

@csrf_exempt
def weburlB(request):
    if request.method == 'POST':

        ver = request.POST.get('ver')
        orderid = request.POST.get('orderid')
        torderid = request.POST.get('torderid')
        machid = request.POST.get('machid')
        trackno = request.POST.get('trackno')
        status = request.POST.get('status')
        errinfo = request.POST.get('errinfo')
        randstr = request.POST.get('randstr')
        timestamp1 = request.POST.get('timestamp')
        sign = request.POST.get('sign')

        coffee = Coffee.objects.get(torderid=torderid, machid=machid)
        coffee.status = status
        if len(errinfo)>0:
            coffee.errinfo = errinfo
        coffee.save()

        resjson = {
            "orderid": orderid,
            "torderid": torderid,
            "code": "0",
            "msg": "lsdklsadlksd"
        }
        return HttpResponse(resjson)

    else:
        return HttpResponse("invalid web request. iexpo")

def check(request):
    cofs = Coffee.objects.all().order_by('-id')
    cof = cofs[0]
    #access_token = qpay_auth()
    #invid = "5af04a8a-f78e-4bec-87bc-327047bade30"
    dic = qpay_check(cof.qpay_invoice_id, cof.access_token)
    #dic = qpay_check(invid, access_token)
    return HttpResponse(dic)

def invoice(request):
    access_token = qpay_auth()
    ver = "v3"
    orderid = "293202"
    machid = "902390239023"
    trackno = "2309239032"
    name = "klsdlsdk"
    price = "999"
    channelid = "99"
    cof = Coffee(ver=ver, orderid=orderid, machid=machid, trackno=trackno, name=name, price=price, channelid=channelid)
    cof.randstr = "odslksdklsd"
    cof.timestamp = "202009221120"
    cof.sign = "sing90239023902"
    cof.save()
    cof.torderid = cof.id
    cof.save()

    import json
    access_token = qpay_auth()
    #dic = qpay_inv(cof.torderid, access_token)

    dic = qpay_inv("0005", access_token)
    test = dic['invoice_id']

    cof.qpay_invoice_id = test
    cof.access_token = access_token
    cof.save()
    return HttpResponse(test + " ::: " + dic['invoice_id'])

def authenticate(request):
    str = qpay_auth()
    return HttpResponse(str)

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def qpay_check(invnum, access_token):
    address = host + "/v2/payment/check"
    myobj = {
        "object_type": "INVOICE",
        "object_id": invnum,
        #"offset": {
        #    "page_number": 1,
        #    "page_limit" : 100
        #}
    }


    resp = requests.post(address, data=myobj,
    #resp = requests.post(address,
                         auth=BearerAuth(access_token),
                         verify=False)
    #str = json.dumps(resp)

    #f = open("/var/django/khashaa/log.txt", "a")
    #f.write(str + "\n")
    #f.close()
    if resp.status_code == 200:
        dic = resp.json()
        return dic
    else:
        return HttpResponse(resp)
        return False

def qpay_inv(torder, access_token, name = "cafe", amount = 100):

    address = host + "/v2/invoice"

    myobj = {
        "invoice_code": "COFFEETERMINAL_INVOICE",
        "sender_invoice_no": torder,
        #"invoice_receiver_code": "terminal",
        "invoice_receiver_code": "terminal",
        "invoice_description": "Cuppy drink - " + name,
        "amount": amount,
        "callback_url": "http://coffee.iexpo.mn/"
    }
    resp = requests.post(address, data=myobj,
    #resp = requests.post(address,
                         auth=BearerAuth(access_token),
                         verify=False)

    if resp.status_code == 200:
        dic = resp.json()
        return dic
    else:
        #return resp
        return False

def qpay_auth():
    address = host + "/v2/auth/token"

    #resp = requests.post(address, data=myobj,
    resp = requests.post(address,
        #auth=('COFFEE_TERMINAL', 'S123456'),
        auth=('COFFEETERMINAL_MERCHANT', 'Asd123'),
        verify=False)

#    print(resp.status_code)
#    print(resp.json())

    if resp.status_code == 200:
        dic = resp.json()
        return dic['access_token']
    else:
        return resp.status_code
        resObj = {'result_msg': 'QPAY-тэй холбогдож чадсангүй', 'result_code': 88}
        return resObj
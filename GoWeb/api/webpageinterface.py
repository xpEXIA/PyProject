# encoding=utf8
# create_time:
# python 3.6.4





from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from GoWeb.settings import logger


def pageA(request):

    logger.debug('真能用？？？？？？？')
    return render(request,
                  'pageA.html',
                  # {'time':datetime.now(),
                  #  'dota':[
                  #      {'id':'1','position':'carry','role':'luna'},
                  #      {'id':'2','position':'mid','role':'strom'},
                  #      {'id':'3','position':'surport','role':'shadowHunt'},
                  #  ]
                  #  }
                  )


def pageB(request):

    return render(request, 'pageA.html')


def aJaxTest(request):

    print(request.POST.get('title'))
    if request.POST.get('title') == 'luna':
        return HttpResponse('0')
    else:
        return HttpResponse('你个智障')

def windowclose(request):

    return render(request, 'windowclose.html')

def testAsd(x):

    return x + 1
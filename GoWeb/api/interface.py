




from django.shortcuts import render
from datetime import datetime

def pageA(request):

    return render(request,
                  'pageA.html',
                  {'name':datetime.now(),
                   'dota':[
                       {'id':'1','position':'carry','role':'luna'},
                       {'id':'2','position':'mid','role':'strom'},
                       {'id':'3','position':'surport','role':'shadowHunt'},
                   ]
                   }
                  )
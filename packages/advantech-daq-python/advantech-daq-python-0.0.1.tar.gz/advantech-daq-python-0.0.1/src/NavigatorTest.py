from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import simplejson as json
# import time
import NavigatorTest
# do=NavigatorTest.DO()
# do.Connect(u"USB-5830,BID#0")
# print("WriteByte DO:",do.WriteByte(0,255))
# print("WriteBit DO:",do.WriteBit(0,7,0))
# print("ReadByte Do:",do.ReadByte(0))
# print("ReadBit Do:",do.ReadBit(0,0))
# print("\n")
# di=NavigatorTest.DI()
# di.Connect(u"USB-5830,BID#0")
# print("ReadByte DI:",di.ReadByte(0))
# print("ReadBit DI:",di.ReadBit(0,3))
# print("AddEventChannel",di.AddEventChannel(0))
# print("AddEventChannel",di.AddEventChannel(1))
# print("SnapStart",di.SnapStart())
# time.sleep(10)
# print("SnapStop",di.SnapStop())
@csrf_exempt
def get_installed_devices(request):
    return
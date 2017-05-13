# -*- coding:utf-8 -*-


"""
======================
@version: 1.0
@author: vincentzhou
@contact: python@vip.126.com
@site: http://analytics.septnet.cn
@software: PyCharm
@file: pay.py
@time: 2017/4/28 11:32
======================
"""
from Handler import BaseHandler, ApiHTTPError
from tornado import gen
from tornado.escape import json_decode
import urllib2, random, hashlib,sys,time

reload(sys)

sys.setdefaultencoding('utf8')
class SetOrder(BaseHandler):
    def set_md5(self,string):
        mobj = hashlib.md5()
        mobj.update(string)
        signvalue = mobj.hexdigest()
        signvalue = signvalue.upper()
        return signvalue

    def XmlData(self):
        openidvalue = self.openid
        appidvalue = self.AppID  # appid
        attachvalue = self.attachvalue
        mch_idvalue = "1467218302"  # mch_id
        nonce_strvalue = self.GetRandomStr
        bodyvalue = self.body.encode('utf-8')
        out_trade_novalue = self.id
        total_feevalue = '1'#self.total_fee  # 价格
        spbill_create_ipvalue = "120.210.166.7"
        notify_urlvalue = "https://jk.jikexueche.com/api/PayResult"  # 用户回调URL地址
        trade_typevalue = "JSAPI"
        key = self.key  # 用户配置

        formatstr = 'appid=%s&attach=%s&body=%s&mch_id=%s&nonce_str=%s&notify_url=%s&openid=%s&out_trade_no=%s&spbill_create_ip=%s&total_fee=%s&trade_type=%s&key=%s' % (appidvalue, attachvalue,bodyvalue,mch_idvalue,nonce_strvalue,notify_urlvalue,openidvalue,out_trade_novalue, spbill_create_ipvalue, total_feevalue,trade_typevalue, key)
        signvalue = self.set_md5(formatstr)

        xmlstart = "<xml>\r\n"
        appid = "<appid>" + appidvalue + "</appid>\r\n"
        attach = "<attach>" + attachvalue + "</attach>\r\n"
        mch_id = "<mch_id>" + mch_idvalue + "</mch_id>\r\n"
        openid = "<openid>" + openidvalue + "</openid>\r\n"
        nonce_str = "<nonce_str>" + nonce_strvalue + "</nonce_str>\r\n"
        body = "<body>" + bodyvalue + "</body>\r\n"
        out_trade_no = "<out_trade_no>" + out_trade_novalue + "</out_trade_no>\r\n"
        total_fee = "<total_fee>" + str(total_feevalue) + "</total_fee>\r\n"
        spbill_create_ip = "<spbill_create_ip>" + spbill_create_ipvalue + "</spbill_create_ip>\r\n"
        notify_url = "<notify_url>" + notify_urlvalue + "</notify_url>\r\n"
        trade_type = "<trade_type>" + trade_typevalue + "</trade_type>\r\n"
        sign = "<sign>" + signvalue + "</sign>\r\n"
        xmlend = "</xml>"
        result = xmlstart + appid + attach+body+mch_id+nonce_str+notify_url+openid+out_trade_no+spbill_create_ip+total_fee+trade_type+sign+ xmlend
        return result.encode('utf-8')


    def Posts(self,data):
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        headers = {"Content-Type": "text/xml"}
        rep = urllib2.Request(url=url, headers=headers, data=data)
        response = urllib2.urlopen(rep)
        res = response.read()
        return res


    def post(self, *args, **kwargs):
        try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET

        self.AppID = "wxad81631247e48b3e"
        timestramp = time.time()
        timestramp_str = str(timestramp).replace(".", "")
        self.id  = "JIKEXUECHE"+timestramp_str+str(random.randint(10,100))
        self.attachvalue = "JKXC"
        self.body = self.get_json_argument("body",None)
        self.total_fee = self.get_json_argument("total_fee",1)
        self.packageid = self.get_json_argument("packageid",0)
        self.openid = self.get_json_argument("openid",None)
        self.key = "jike712YMiinoo736Rexhu1217Nan909"
        data = self.XmlData()
        result = self.Posts(data)
        response =  result
        xml2obj = {}
        root = ET.fromstring(response)
        for child_list in root.findall("*"):
            xml2obj[child_list.tag]=child_list.text
        if "prepay_id" in xml2obj.keys():
            saveresult = self.SaveOrder(self.packageid,self.openid,self.id,xml2obj['prepay_id'],int(self.total_fee)/100)
            if saveresult:
                pass
            else:
                self.writejson(json_decode(str(ApiHTTPError(10500))))
                return False
        signstr = "appId=%s&nonceStr=%s&package=prepay_id=%s&signType=MD5&timeStamp=%s&key=%s" % (self.AppID,xml2obj['nonce_str'],xml2obj['prepay_id'],timestramp_str,self.key)
        secondsign = self.set_md5(signstr)
        rep = {}
        rep['data'] = {"order_id":saveresult,"paysign":secondsign,"out_trade_no":self.id,"prepayid":xml2obj['prepay_id'],"nonceStr":xml2obj['nonce_str'],"timestramp":timestramp_str}
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    def SaveOrder(self,packageid,openId,order_code,prepay_id,order_money):
        timestramp = time.time()

        Order = self.Order()
        Order.order_packageuid = packageid
        Order.order_createtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestramp))
        Order.order_money = order_money
        Order.order_studentuid = openId
        if self.total_fee==50000:
            Order.order_type = 0
        else:
            Order.order_type = 1
        Order.order_wx_prepay_id = prepay_id
        Order.order_code = order_code
        self.DbRead.add(Order)
        self.DbRead.commit()
        Order_id = Order.order_id
        self.DbRead.close()

        if Order_id:
            result = Order_id
        else:
            result = False

        return result

class PayResult(BaseHandler):

    def get(self, *args, **kwargs):
        result = "<xml><return_code>SUCCESS</return_code><return_msg>OK</return_msg></xml>"
        self.write(result)


class PaySucess(BaseHandler):

    def post(self, *args, **kwargs):
        self.order_id = self.get_json_argument('order_id',None)

        student_order = self.DbRead.query(self.Order).filter(self.Order.order_id==self.order_id).with_lockmode("update").one()
        student_order.order_state = 1
        self.DbRead.commit()
        self.DbRead.close()
        rep = {}
        rep['data'] = "SUCESS"
        self.writejson(json_decode(str(ApiHTTPError(**rep))))
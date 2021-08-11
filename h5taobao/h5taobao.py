'''
Author: wyuye_
Date: 2021-02-07 19:35:37
Description: 淘宝H5 api 下单
'''
# -*- coding=UTF-8 -*-
from selenium import webdriver
import time
import datetime
from tkinter import *
# import tkinter as tk
import threading
import tkinter.messagebox
import requests
import json

def make_app():
    app = Tk()
    app.geometry('600x550')
    Label(app, text='cookie').place(relx=0.1, rely=0.05)
    cookieStr = StringVar()
    cookieStr.set('__jdu=161007932067378363993; areaId=15; ipLoc-djd=15-1213-3411-0; PCSYCityID=CN_330000_330100_0; pinId=WMbBIuyneyfB2zPLyCPjlLV9-x-f3wj7; pin=jd_6b7137a5797f5; unick=jd_159901sbm; _tp=K%2B8p15Yf%2Fo6OVbmpwNcWqI9c2x7OkPebbQJ8rVeoppo%3D; _pst=jd_6b7137a5797f5; user-key=8ff325fb-f180-4a93-9e79-97e9d7991cbf; shshshfpa=6e493192-242b-4ac1-6d79-f802e3867cc1-1610157195; shshshfpb=rfq77Td4qNHPLmfIBBs%2Fhug%3D%3D; unpl=V2_ZzNtbRBfQB0hX0ADeRxYBWIFEQ8RV0NGcglAUn1KD1FlUxVcclRCFnUUR1RnGV4UZwUZXkdcQBFFCEdkexhdBWUFF11DVnMlRQtGZHopXAJnAhNbSlVAFHIORFJyG1sHbwsQbXJQQxxFOHZUchhbBmUKFl9EZ0IldQFFVXkdWgxlACIWLFYOFXIIR1V9EV4GZgQUX0ReQRJ3AE5WSxldBGYCEltHXkIldg%3d%3d; __jdv=122270672|2929gou.com|t_1001374100_|tuiguang|c929ef7f3451472cb11b60777bbe3a60|1610529867922; TrackID=1xOrlW55Mlw25qbxzNFxSlXCHQ-Wqfd982fDrN16WdcASV4_tJEJ9UOn0fCtuIG2y97vdSiDYimuZNDwQi1a4CB1aV-KLiwNAr7jGJYrH-fVfNYhCLoZBeOTwQSwMS9zl; thor=D2E3A4D9314011D91C4EC8CE1265A02B24169B0325F4D7D188D29569EC08E2E807BF79EEC57788FC6882701A91F2070F89654CC0A31640890D5DAF1B177B4EE4D52DEDB8747CDE73A4453A05638F3800E07061C5A275758200FBD0EC5FABDE01EA4A4027C64CF71BA7CA3A61862DEA8DB0EBBC2F5A93643E27029A53B8DE1561E711C1964E0157AAC31D11E895A7A9CEDD35F0EFFB3358EFAE908177968F6BCF; ceshi3.com=201; shshshfp=bdc5fdf52a5174ae8d7440581319dd02; shshshsID=f10835d2d4fd85be92ddb14eab5aaacf_2_1610589145459; cn=3; __jda=122270672.161007932067378363993.1610079321.1610529868.1610589024.8; __jdc=122270672; 3AB9D23F7A4B3C9B=CH2AWTZNVCRPTFNPJQT2SZTJ5PSK7EV4TOQB7V5CCSVCUIOQ3K5ZT5S62PYV4V4YI4Z7EUXLNLKETTZBKFJ5J6WSO4; __jdb=122270672.8.161007932067378363993|8.1610589024')
    Entry(app,textvariable=cookieStr, name='cookie').place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.15)

    Label(app, text='请按照格式输入抢单时间').place(relx=0.1, rely=0.3)
    timeStr = StringVar()
    timeStr.set('2021-01-09 10:00:00')
    Entry(app, textvariable=timeStr, name='ipt').place(relx=0.1, rely=0.35, relwidth=0.3, relheight=0.1)

    Label(app, text='商品ID').place(relx=0.45, rely=0.3)
    pId = StringVar()
    # pId.set('100016799390')
    pId.set('100012043978') # 茅台
    Entry(app, textvariable=pId, name='ipt1').place(relx=0.45, rely=0.35, relwidth=0.2, relheight=0.1)

    Label(app, text='数量').place(relx=0.7, rely=0.3)
    count = StringVar()
    count.set('2')
    Entry(app, textvariable=count, name='ipt2').place(relx=0.7, rely=0.35, relwidth=0.2, relheight=0.1)

    Button(app, text='点击开始抢单', fg = "white", bg = "black", command=addToCart).place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.1)

    Text(app, name="runningText").place(relx=0.1, rely=0.65, relwidth=0.8, relheight=0.3)
    return app

def addToCart():
    cookie = app.children['cookie'].get()
    if cookie == '':
        tkinter.messagebox.showinfo('错误', '请网页登录京东，查看任一接口的cookie，填入下面')
        return
    
    headers={
        'Cookie':cookie,
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'path':'/shopping/order/submitOrder.action?',
        'origin':'https://trade.jd.com',
        'referer':'https://trade.jd.com/shopping/order/getOrderInfo.action',
        'x-requested-with':'XMLHttpRequest',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'authority':'trade.jd.com',
        'method':'post',
        'scheme':'https',
    }
    now = datetime.datetime.now()
    rid = int(now.timestamp())

    formatNow = now.strftime('%Y-%m-%d %H:%M:%S')
    setTime = app.children['ipt'].get()
    # if formatNow > setTime:
    #     tkinter.messagebox.showinfo('错误', '设置时间要超过当前时间')
    #     return


    # runningText = app.children['runningText']
    # pId = app.children['ipt1'].get()
    # count = app.children['ipt2'].get()
    # url3 = "https://marathon.jd.com/seckillnew/orderService/pc/submitOrder.action?skuId={pId}".format(pId=pId)
    # postData = '{"skuId":"100012043978","num":2,"addressId":2655536835,"yuShou":true,"isModifyAddress":false,"name":"王煜野","provinceId":15,"cityId":1213,"countyId":3410,"townId":59943,"addressDetail":"祥园路北部软件园德信北海公园4-2-1402","mobile":"159****9043","mobileKey":"e29d025a8cf3e775f285cf9cdc9800d4","email":"","postCode":"","invoiceTitle":4,"invoiceCompanyName":"","invoiceContent":1,"invoiceTaxpayerNO":"","invoiceEmail":"","invoicePhone":"159****9043","invoicePhoneKey":"e29d025a8cf3e775f285cf9cdc9800d4","invoice":true,"password":"","paymentType":4,"areaCode":"86","overseas":0,"phone":"","eid":"CH2AWTZNVCRPTFNPJQT2SZTJ5PSK7EV4TOQB7V5CCSVCUIOQ3K5ZT5S62PYV4V4YI4Z7EUXLNLKETTZBKFJ5J6WSO4","fp":"33eaf773494fe391925ae6df450d557a","token":"1ebca6b6a3cd1c0f2f53f99fa77c2795","pru":"","provinceName":"浙江","cityName":"杭州市","countyName":"拱墅区","townName":"祥符街道"}'
    # r3 = requests.post(url3,headers=headers,data =json.dumps(postData))
    # print('调用接口：' + url3)
    # print('接口回调：' + r3.text.strip())
    # print((json.loads(r3.text.strip()))['success'])
    # runningText.insert(0.0, '\n调用接口：' + url3)
    # runningText.insert(0.0, '\n接口回调：' + r3.text.strip())

    timecut = 0.01
    while True:
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if currentTime >= setTime:
            try:
                runningText = app.children['runningText']
                pId = app.children['ipt1'].get()
                count = app.children['ipt2'].get()
                

                url3 = "https://marathon.jd.com/seckillnew/orderService/pc/submitOrder.action?skuId={pId}".format(pId=pId)
                postData = '{"skuId":"100012043978","num":2,"addressId":2655536835,"yuShou":true,"isModifyAddress":false,"name":"王煜野","provinceId":15,"cityId":1213,"countyId":3410,"townId":59943,"addressDetail":"祥园路北部软件园德信北海公园4-2-1402","mobile":"159****9043","mobileKey":"e29d025a8cf3e775f285cf9cdc9800d4","email":"","postCode":"","invoiceTitle":4,"invoiceCompanyName":"","invoiceContent":1,"invoiceTaxpayerNO":"","invoiceEmail":"","invoicePhone":"159****9043","invoicePhoneKey":"e29d025a8cf3e775f285cf9cdc9800d4","invoice":true,"password":"","paymentType":4,"areaCode":"86","overseas":0,"phone":"","eid":"CH2AWTZNVCRPTFNPJQT2SZTJ5PSK7EV4TOQB7V5CCSVCUIOQ3K5ZT5S62PYV4V4YI4Z7EUXLNLKETTZBKFJ5J6WSO4","fp":"33eaf773494fe391925ae6df450d557a","token":"1ebca6b6a3cd1c0f2f53f99fa77c2795","pru":"","provinceName":"浙江","cityName":"杭州市","countyName":"拱墅区","townName":"祥符街道"}'
                r3 = requests.post(url3,headers=headers,data =json.dumps(postData))
                print('调用接口：' + url3)
                print('接口回调：' + r3.text.strip())
                runningText.insert(0.0, '\n调用接口：' + url3)
                runningText.insert(0.0, '\n接口回调：' + r3.text.strip())
                if r3.text.strip() != 'https://marathon.jd.com/koFail.html' and (json.loads(r3.text.strip()))['success'] != False:
                    runningText.insert(0.0, '\n-----------抢单成功-----------')
                    break
            except:
                time.sleep(timecut)
        time.sleep(timecut)

if __name__ == '__main__':
    app = make_app()
    app.mainloop()


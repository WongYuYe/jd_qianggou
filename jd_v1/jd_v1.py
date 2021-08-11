# 京东购物车下单
# 流程：加入购物车->确认订单->下单
# -*- coding=UTF-8 -*-
import time
import datetime
from tkinter import *
import tkinter.messagebox
import requests
import threading
import json

ApiUrls = {
    'getProductInfos':
    'https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart&appid=JDC_mall_cart&loginType=3&body={"serInfo":{"area":"15_1213_3410_59943","user-key":""},"cartExt":{"specialId":1}}',
    'addToCart':
    'https://cart.jd.com/gate.action?pid={pId}&pcount={count}&ptype=1',
    'getOrderInfo':
    'https://trade.jd.com/shopping/order/getOrderInfo.action?overseaMerge=1',
    'submitOrder':
    'https://trade.jd.com/shopping/order/submitOrder.action?overseaMerge=1&presaleStockSign=1&overseaPurchaseCookies=&vendorRemarks={vendorRemarks}&submitOrderParam.sopNotPutInvoice=true&submitOrderParam.trackID=TestTrackId&overseaMerge=1&submitOrderParam.ignorePriceChange=0&submitOrderParam.btSupport=0&submitOrderParam.eid=CH2AWTZNVCRPTFNPJQT2SZTJ5PSK7EV4TOQB7V5CCSVCUIOQ3K5ZT5S62PYV4V4YI4Z7EUXLNLKETTZBKFJ5J6WSO4&submitOrderParam.fp=33eaf773494fe391925ae6df450d557a&submitOrderParam.jxj=1'
}


def make_app():
    app = Tk()
    app.geometry('600x550')
    app.title('京东抢抢抢')
    Label(app, text='cookie').place(relx=0.1, rely=0.05)
    cookieStr = StringVar()
    cookieStr.set(
        '__jdv=76161171|direct|-|none|-|1616467314062; __jdu=1616467314053904991231; areaId=15; ipLoc-djd=15-1213-3411-0; PCSYCityID=CN_330000_330100_330106; TrackID=1KC1YnusIMLleAn7Vl1ghEwzk-Pm8ShkAPjt2S_D-jNe7tzlF1bSmLYOCVsE8m5DkPG6neG3qtcVn1-5Eg7S1WSCsdM3v_8h_5c4np2gZ0rU; thor=D2E3A4D9314011D91C4EC8CE1265A02B24169B0325F4D7D188D29569EC08E2E8BC1C6E88CB14AA5CEEF08FEF100D8E6706ACA271554CE16923F22E096A44B1AD51FF786D9FFE0F79830CD283BBEC0392B3AAF54CF4ABB6E7A2D84648AFF535D9FC1458A3E88B63CEDFB0BF38B847A45FA5CA45B3C69EF48F89DA09D430304D2D730775881852D60E8039A8485D5EA4982328DD0B6AEB0974AC1119C631F8DACF; pinId=WMbBIuyneyfB2zPLyCPjlLV9-x-f3wj7; pin=jd_6b7137a5797f5; unick=jd_159901sbm; ceshi3.com=201; _tp=K%2B8p15Yf%2Fo6OVbmpwNcWqI9c2x7OkPebbQJ8rVeoppo%3D; _pst=jd_6b7137a5797f5; user-key=63f65bb9-c6e6-4e81-be2a-6669facc2b9b; cn=4; shshshfpa=dc235a0b-dc68-a428-2453-ceb587aadd45-1616467341; shshshfpb=aZfcTfWcqGmRMOuL8DGKZtA%3D%3D; __jda=122270672.1616467314053904991231.1616467314.1616467314.1616467314.1; __jdc=122270672; shshshfp=66dd58d74796cc3e44dcb0c134c3ff20; 3AB9D23F7A4B3C9B=O2N2GZMGSDN5T36E3FCPAV3J3SPFTAXTLAEQPJWUJ6EPETJMGZCXJ2VF3LI6AP6VAYRSO6FX53CZWQU6SR3LD56CHI; __jdb=122270672.7.1616467314053904991231|1.1616467314; shshshsID=a1ae029abd523c9b54cf4e886607cf95_4_1616467373090'
    )
    Entry(app, textvariable=cookieStr, name='cookie').place(relx=0.1,
                                                            rely=0.1,
                                                            relwidth=0.8,
                                                            relheight=0.15)

    Label(app, text='请按照格式输入抢单时间').place(relx=0.1, rely=0.3)
    timeStr = StringVar()
    timeStr.set(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    Entry(app, textvariable=timeStr, name='ipt').place(relx=0.1,
                                                       rely=0.35,
                                                       relwidth=0.3,
                                                       relheight=0.1)

    Label(app, text='商品ID').place(relx=0.45, rely=0.3)
    pId = StringVar()
    # pId.set('2148924')  # 自营u盘
    # pId.set('10026120395414')  # 非自营猫粮
    pId.set('100009021265')  # 自营显卡
    # pId.set('100012043978') # 茅台
    Entry(app, textvariable=pId, name='ipt1').place(relx=0.45,
                                                    rely=0.35,
                                                    relwidth=0.2,
                                                    relheight=0.1)

    Label(app, text='数量').place(relx=0.7, rely=0.3)
    count = StringVar()
    count.set('1')
    Entry(app, textvariable=count, name='ipt2').place(relx=0.7,
                                                      rely=0.35,
                                                      relwidth=0.2,
                                                      relheight=0.1)

    Button(app, text='点击开始抢单', fg="white", bg="black",
           command=orderThread).place(relx=0.1,
                                      rely=0.5,
                                      relwidth=0.8,
                                      relheight=0.1)

    Text(app, name="runningText").place(relx=0.1,
                                        rely=0.65,
                                        relwidth=0.8,
                                        relheight=0.3)
    runningText = app.children['runningText']
    runningText.insert(0.0, '\n抢单步骤：')
    runningText.insert(
        END,
        '\n第一步：网页登录京东，查看购物车下https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart的cookie，填入cookie的输入框'
    )
    runningText.insert(END, '\n第二步：打开商品详情页，地址栏查看商品ID，填入商品ID输入框')
    runningText.insert(END, '\n第三步：若该商品已在购物车内，清空（防止限购导致抢单失败），其他购物车内商品不勾选')

    return app


def orderThread():
    th = threading.Thread(target=addToCartAndSubmit)
    th.start()


def addToCartAndSubmit():
    cookie = app.children['cookie'].get()
    if cookie == '':
        tkinter.messagebox.showinfo(
            '错误',
            '请网页登录京东，查看购物车下https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart的cookie，填入下面'
        )
        return

    # 请求头
    tradeHeaders = {
        'Cookie': cookie,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'path': '/shopping/order/submitOrder.action?',
        'origin': 'https://trade.jd.com',
        'referer': 'https://trade.jd.com/shopping/order/getOrderInfo.action',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'authority': 'trade.jd.com',
        'method': 'post',
        'scheme': 'https',
    }
    cartInfoheaders = {
        'Cookie': cookie,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'origin': 'https://cart.jd.com',
        'referer': 'https://cart.jd.com',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'authority': 'api.m.jd.com',
        'method': 'post',
        'scheme': 'https',
    }

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    setTime = app.children['ipt'].get()
    if now > setTime:
        tkinter.messagebox.showinfo('错误', '设置时间要超过当前时间')
        return

    # 轮询时间
    timeCut = 1

    while True:
        runningText = app.children['runningText']

        currentTime = datetime.datetime.now()

        if currentTime.strftime('%Y-%m-%d %H:%M:%S') >= setTime:
            try:
                pId = app.children['ipt1'].get()
                count = app.children['ipt2'].get()

                # 加入购物车，加入的商品默认勾选
                addToCartUrl = ApiUrls['addToCart'].format(pId=pId, count=count)
                addToCartRes = requests.get(addToCartUrl, headers=tradeHeaders)
                print('调用接口：' + addToCartUrl)
                runningText.insert(0.0, '\n调用接口：' + addToCartUrl + '--- √√√')

                # 查询商品信息
                pInfoApi = 'https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart&appid=JDC_mall_cart&loginType=3&body={"serInfo":{"area":"15_1213_3410_59943","user-key":""},"cartExt":{"specialId":1}}'
                pInfoRes = requests.get(pInfoApi,
                                        headers=cartInfoheaders).json()
                vendors = []
                if (pInfoRes['success']):
                    vendors = pInfoRes['resultData']['cartInfo']['vendors']

                vendorRemarks = []

                # 查找购买的商品的vendorId
                for vendor in vendors:
                    for item in vendor['sorted']:
                        if vendor['vendorId'] == 8888:
                            if str(item['item']['Id']) == pId:
                                vendorRemarks.append({
                                    "vendorId":
                                    str(vendor['vendorId']),
                                    "remark":
                                    ""
                                })
                            break
                        else:
                            for iitem in item['item']['items']:
                                if str(iitem['item']['Id']) == pId:
                                    vendorRemarks.append({
                                        "vendorId":
                                        str(vendor['vendorId']),
                                        "remark":
                                        ""
                                    })
                                break

                # 确认订单
                getOrderInfoUrl = ApiUrls['getOrderInfo']
                getOrderInfoRes = requests.get(getOrderInfoUrl, headers=tradeHeaders)
                print('调用接口：' + getOrderInfoUrl)
                runningText.insert(0.0, '\n调用接口：' + getOrderInfoUrl + '--- √√√')

                # 下单
                submitOrderUrl = ApiUrls['submitOrder'].format(vendorRemarks=json.dumps(
                    vendorRemarks, separators=(',', ':')))
                submitOrderRes = requests.get(submitOrderUrl, headers=tradeHeaders)
                print('调用接口：' + submitOrderUrl)
                runningText.insert(0.0, '\n调用接口：' + submitOrderUrl + '--- √√√')
                runningText.insert(0.0, '\n下单接口返回：' + submitOrderRes.text)
                message = ''
                if submitOrderRes.json()['orderId'] != 0:
                    message = '抢单成功'
                else:
                    message = submitOrderRes.json()['message']
                tkinter.messagebox.showinfo('提示', message)

                break
            except:
                time.sleep(timeCut)
        runningText.insert(
            0.0, '\n倒计时：' + str(
                (datetime.datetime.strptime(setTime, "%Y-%m-%d %H:%M:%S") -
                 currentTime).seconds) + '秒------' +
            currentTime.strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(timeCut)


app = make_app()
app.mainloop()

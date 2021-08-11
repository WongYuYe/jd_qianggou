# 京东购物车下单
# 流程：全选购物车->确认订单->下单
# 与v1版区别在于加入购物车步骤手动完成，再调用全选，从购物车下单
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
    'https://trade.jd.com/shopping/order/submitOrder.action?overseaMerge=1&presaleStockSign=1&overseaPurchaseCookies=&vendorRemarks={vendorRemarks}&submitOrderParam.sopNotPutInvoice=true&submitOrderParam.trackID=TestTrackId&overseaMerge=1&submitOrderParam.ignorePriceChange=0&submitOrderParam.btSupport=0&submitOrderParam.eid=CH2AWTZNVCRPTFNPJQT2SZTJ5PSK7EV4TOQB7V5CCSVCUIOQ3K5ZT5S62PYV4V4YI4Z7EUXLNLKETTZBKFJ5J6WSO4&submitOrderParam.fp=33eaf773494fe391925ae6df450d557a&submitOrderParam.jxj=1',
    'checkAllOfCart': 'https://api.m.jd.com/api?functionId=pcCart_jc_cartCheckAll&appid=JDC_mall_cart&loginType=3'
}


def make_app():
    app = Tk()
    app.geometry('600x550')
    app.title('京东抢抢抢')
    Label(app, text='cookie').place(relx=0.1, rely=0.05)
    cookieStr = StringVar()
    cookieStr.set(
        '__jdv=76161171|direct|-|none|-|1620611322701; __jdu=1620611322700641690673; areaId=15; ipLoc-djd=15-1213-3411-0; user-key=f6d6b847-c623-4072-ab34-8c1dab2b7774; PCSYCityID=CN_330000_330100_330106; shshshfpa=6d3e4977-bb95-22e2-e44e-470b57f1266e-1620611325; shshshfpb=ptRkHZJRx65qeJhfYFErV3w%3D%3D; TrackID=1jnlhLgFTe9GUNixMvoXu48JdJfLzY3keY_SDFoEcEy-Ik05FYmu81_gTASmcFWmTcaV3iQqwF0s8vDR8dmuDCK-h-AVwqVmqfchN139u-QayRl7IB7yoVWCRKpt_vFd0; thor=D2E3A4D9314011D91C4EC8CE1265A02B24169B0325F4D7D188D29569EC08E2E843E8319E0C30D6011664CD4B13F2C0598F667A01B5CFFCD93DDF2E1AB3CD924D833408E5B30ECC6254D807C4B990FCC80E77F00B38C2FC5192D008D9A840205201697E40C73CBA95E56DFA2A1639C4B15F15FA1AC9D231B5293042D76B20E65661353FA0AA7BF0D11B0AB7C198B4789C196F75EAF05F9314D7E74B431C0375D9; pinId=WMbBIuyneyfB2zPLyCPjlLV9-x-f3wj7; pin=jd_6b7137a5797f5; unick=jd_159901sbm; ceshi3.com=203; _tp=K%2B8p15Yf%2Fo6OVbmpwNcWqI9c2x7OkPebbQJ8rVeoppo%3D; _pst=jd_6b7137a5797f5; __jda=122270672.1620611322700641690673.1620611323.1620611323.1620611323.1; __jdb=122270672.5.1620611322700641690673|1.1620611323; __jdc=122270672; shshshfp=e132c1bb2bbfd9fc4fa922c4b906e459; shshshsID=dd81785766e2773bcd24ea5a2be521bd_3_1620611369900'
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
    # pId.set('2148924,10026899941091,100013490678')  # 自营u盘
    # pId.set('10026120395414')  # 非自营猫粮
    pId.set('10030436702876')  # 自营显卡
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
    runningText.insert(END, '\n第二步：手动添加商品进购物车（注意限购数量），并将商品ID，填入商品ID输入框')

    return app


def orderThread():
    th = threading.Thread(target=checkCartAndSubmit)
    th.start()


def checkCartAndSubmit():
    cookie = app.children['cookie'].get()
    if cookie == '':
        tkinter.messagebox.showinfo(
            '错误',
            '请网页登录京东，查看购物车下https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart的cookie，填入下面'
        )
        return
    
    # 全选购物车请求头
    checkCartHeaders = {
        'Cookie': cookie,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'origin': 'https://cart.jd.com',
        'referer': 'https://cart.jd.com/',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }

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

    pIds = app.children['ipt1'].get()
    # count = app.children['ipt2'].get()
    # 查询商品信息
    pInfoRes = requests.get(ApiUrls['getProductInfos'],
                            headers=cartInfoheaders).json()
    vendors = []
    if (pInfoRes['success'] and pInfoRes['resultData']['cartInfo'] is not None):
        vendors = pInfoRes['resultData']['cartInfo']['vendors']
    else:
        tkinter.messagebox.showinfo('提示', '请把商品pIds加入购物车')

    vendorRemarks = []

    # 查找购买的商品的vendorId
    for vendor in vendors:
        for item in vendor['sorted']:
            if len(item['item']['items']) > 0:
                for iitem in item['item']['items']:
                    if pIds.find(str(iitem['item']['Id'])) > -1:
                        vendorRemarks.append({
                            "vendorId":
                            str(vendor['vendorId']),
                            "remark":
                            ""
                        })
                    break
            else:
                if pIds.find(str(item['item']['Id'])) > -1:
                    vendorRemarks.append({
                        "vendorId":
                        str(vendor['vendorId']),
                        "remark":
                        ""
                    })
                break

    for vendor in vendorRemarks:
        if vendor['vendorId'] == '8888':
            del vendorRemarks[vendorRemarks.index(vendor)]
    while True:
        runningText = app.children['runningText']

        currentTime = datetime.datetime.now()

        if currentTime.strftime('%Y-%m-%d %H:%M:%S') >= setTime:
            try:
                reSubmitOrder(checkCartHeaders, tradeHeaders, vendorRemarks, runningText)

                break
            except:
                time.sleep(timeCut)
        runningText.insert(
            0.0, '\n倒计时：' + str(
                (datetime.datetime.strptime(setTime, "%Y-%m-%d %H:%M:%S") -
                 currentTime).seconds) + '秒------' +
            currentTime.strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(timeCut)

def reSubmitOrder(checkCartHeaders, tradeHeaders, vendorRemarks, runningText):
    # 全选购物车
    checkAllOfCartUrl = ApiUrls['checkAllOfCart']
    checkAllofCartRes = requests.get(checkAllOfCartUrl, headers=checkCartHeaders)
    runningText.insert(0.0, '\n全选时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    # 确认订单
    getOrderInfoUrl = ApiUrls['getOrderInfo']
    getOrderInfoRes = requests.get(getOrderInfoUrl, headers=tradeHeaders)
    runningText.insert(0.0, '\n确认订单时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    # 下单
    submitOrderUrl = ApiUrls['submitOrder'].format(vendorRemarks=json.dumps(
        vendorRemarks, separators=(',', ':')))
    submitOrderRes = requests.get(submitOrderUrl, headers=tradeHeaders)
    # runningText.insert(0.0, '\n调用接口：' + submitOrderUrl + '--- √√√')
    runningText.insert(0.0, '\n下单接口返回：' + submitOrderRes.text)
    runningText.insert(0.0, '\n下单完成时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    message = ''
    if submitOrderRes.json()['orderId'] != 0:
        message = '抢单成功'
        tkinter.messagebox.showinfo('提示', message)   
    else:
        message = submitOrderRes.json()['message']
        if message.find('无货') == -1:
            time.sleep(1)
            requests.get(ApiUrls['getProductInfos'],
                            headers=cartInfoheaders).json()
            reSubmitOrder(checkCartHeaders, tradeHeaders, vendorRemarks, runningText)
        else:
            tkinter.messagebox.showinfo('提示', message)   

app = make_app()
app.mainloop()

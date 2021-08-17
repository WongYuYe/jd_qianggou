/*
 * @Author: wyuye_
 * @Date: 2021-08-12 22:18:13
 * @Description: jd抢购node实现
 */

const qs = require('qs')

const {
  getRequestHandler,
  postRequestHandler
} = require('./request');

const { APIS, HEADERS } = require('./api')

let cookie = '__jdv=122270672|direct|-|none|-|1628774474958; __jdu=1628774474957577645315; pinId=WMbBIuyneyfB2zPLyCPjlLV9-x-f3wj7; pin=jd_6b7137a5797f5; unick=jd_159901sbm; _tp=K%2B8p15Yf%2Fo6OVbmpwNcWqI9c2x7OkPebbQJ8rVeoppo%3D; _pst=jd_6b7137a5797f5; shshshfpb=f1UVCRbjgwhb4uEANH%20tEWQ%3D%3D; shshshfpa=996cf590-336e-4f42-5fdf-68e5b430bb90-1628387648; areaId=15; ipLoc-djd=15-1213-3410-0; PCSYCityID=CN_330000_330100_330105; user-key=26d6f10b-2647-4c8e-b724-bee0ad2ede40; cn=1; __jda=122270672.1628774474957577645315.1628774475.1629125124.1629171200.8; __jdc=122270672; wlfstk_smdl=gjfvbt9k4knr0zsvdnlflb1gsn44hkey; TrackID=1InO_p3gch1LEbOFoRtzDL6_q7wNmTvRfB9LDT4vR2Et13qcPXUoZCrlveBLsnuCT94lY5aswSKnmGKAGIWci3r2IJH8ZpMMM9gyro7zqSGw; thor=D2E3A4D9314011D91C4EC8CE1265A02B24169B0325F4D7D188D29569EC08E2E8939E9C86197D20B0885FE73707CE0E5114CC384570D8E0D8365E6E811D9961981C4AA4CC26EEE5DD4B8624FF8668329714DEC854E324041B4DAC272C2A9B552FBF4B6721A18F43D9D09129FD2637C7D7A6E8F96622F334A4662E8F15226E2B7E375AEE5E547F8D1905F3C4A7AD5914B112F0CDE137D154D266F3C6E4FB7F081F; ceshi3.com=203; shshshfp=7ba836310331478aa651078f05363dc9; 3AB9D23F7A4B3C9B=IBFBLK7NB3VD5A2MPCMO247RF25U63344NRSNN2RZJVG5RW5DFITPV2VRVW6OHRVSBNQAZRDDKOP2HAMB3XE3RG2GQ; __jdb=122270672.5.1628774474957577645315|8.1629171200; shshshsID=30285c862a4ec1f6099bdfdc29d73ae3_3_1629171417050'; // JD cookie


const { pid, time, pcount, timeCut } = require('./config')

const timeStamp = +new Date(time);

const puppeteer = require('puppeteer');

const { JDLoginURL, JDCartURL } = require('./urls')

const { parseCookie, writeCookieToLocal, writeLogsToLocal } = require('./utils')

require('./DateFormat.js')

/**
 * @description: 启动puppeteer，登录京东获取cookie
 * @param {*}
 * @return {*}
 */
async function main() {
  if (!cookie) {
    const browser = await puppeteer.launch({
      headless: false,
    });
    const page = await browser.newPage();
    page.on('request', async req => {
      if (req.url() === JDCartURL) {
        cookie = parseCookie(await page.cookies());
        await afterGetCookieHandler()
      }
    });
    await page.goto(JDLoginURL);
  } else {
    await afterGetCookieHandler()
  }
}

/**
 * @description: 获取cookie后的操作
 * @param {*}
 * @return {*}
 */
function afterGetCookieHandler() {
  return new Promise(async (resolve, reject) => {
    // 本地写入cookie
    await writeCookieToLocal(cookie)

    // 判断是否存在该商品并加车
    await checkProductIsExit()

    // 统计抢购倒计时
    const afterTime = timeStamp - +new Date();
    console.log(`${afterTime / 1000}秒后执行`)
    setTimeout(async () => {
      await startOrder()
    }, afterTime)

    resolve()
  })
}



/**
 * @description: 开始下单流程，加入购物车-确认订单-提交订单
 * @param {*}
 * @return {*}
 */
function startOrder() {
  return new Promise(async (resolve, reject) => {
    // await cartCheckSingle();
    await comfirmOrder()
    const res = await submitOrder();
    const { success } = res;
    const message = success ? '成功' : '失败';
    console.log(`抢单${message}-----------√√√√√`, new Date().format('yyyy-MM-dd hh:mm:ss S'))
    writeLogsToLocal(JSON.stringify(res))
    if (!success && timeCut) {
      setTimeout(async () => {
        await reCheckAndStartOrder()
      }, timeCut)
    } else {
      resolve()
    }
  })
}

function reCheckAndStartOrder() {
  return new Promise(async (resolve, reject) => {
    const stockCode = await checkProductStockCode()
    if (stockCode === 0) {
      console.log('该商品有货，开始抢单-----------√√√√√ ')
      await startOrder()
    } else if (stockCode === 1) {
      console.log('该商品无货-----------√√√√√ ')
      setTimeout(async () => {
        await reCheckAndStartOrder()
      }, timeCut)
    } else if (stockCode === 2) {
      console.log('该商品采购中-----------√√√√√ ')
      setTimeout(async () => {
        await reCheckAndStartOrder()
      }, timeCut)
    }
  })
  
}

/**
 * @description: 检查购物车此商品状态
 * @param {*}
 * @return {*}
 */
 function checkCartProduct() {
  return new Promise(async (resolve, reject) => {
    console.log('开始检查购物车此商品状态-----------');
    const { resultData: { cartInfo: { vendors } } } = await getCurrentCart()
    const allItemArray = [];
    vendors.map(({ sorted }) => {
      sorted.map(({ item, itemType }) => {
        if (itemType === 1) {
          allItemArray.push(item)
        } else {
          item.items.map(({ item: iitem }) => {
            allItemArray.push(iitem)
          })
        }
      })
    })
    const findResult = allItemArray.find(item =>
      item.Id === pid
    )
    resolve(findResult)
  })
}


/**
 * @description: 检查购物车是否已有此商品
 * @param {*}
 * @return {*}
 */
function checkProductIsExit() {
  return new Promise(async (resolve, reject) => {
    const result = await checkCartProduct()
    if (!result) {
      console.log('无此商品，并开始加入购物车-----------')
      await addToCart()
      console.log('加入购物车成功-----------√√√√√')
    } else {
      console.log('购物车内已有此商品-----------√√√√√')
    }
    resolve()
  })
}

/**
 * @description: 监控此商品是否还有库存
 * @param {*} stockCode 0:有货 1:无货 2:采购中
 * @return {*}
 */
function checkProductStockCode() {
  return new Promise(async (resolve, reject) => {
    const { stockCode } = await checkCartProduct()
    resolve(stockCode)
  })
}
/**
 * @description: 获取购物车信息
 * @param {*}
 * @return {*}
 */
function getCurrentCart() {
  return new Promise(async (resolve, reject) => {
    const params = {
      url: APIS.getCurrentCart,
      headers: {
        Cookie: cookie,
        ...HEADERS.cart
      }
    }
    try {
      const res = await postRequestHandler(params)
      console.log('查看购物车信息-----------')
      resolve(res.json())
    } catch (error) {
      reject(error)
    }
  })
}

/**
 * @description: 加入购物车
 * @param {*}
 * @return {*}
 */
function addToCart() {
  return new Promise(async (resolve, reject) => {
    const params = {
      url: APIS.addToCart + `?pid=${pid}&pcount=${pcount}&ptype=1`,
      headers: {
        Cookie: cookie,
        ...HEADERS.cart
      }
    }
    try {
      await postRequestHandler(params)
      console.log('加入购物车-----------√√√√√')
      resolve()
    } catch (error) {
      reject(error)
    }
  })
}

/**
 * @description: 确认订单
 * @param {*}
 * @return {*}
 */
function comfirmOrder() {
  return new Promise(async (resolve, reject) => {
    const params = {
      url: APIS.getOrderInfo,
      headers: {
        Cookie: cookie,
        ...HEADERS.trade
      }
    }
    try {
      await postRequestHandler(params)
      console.log('确认订单-----------√√√√√', new Date().format('yyyy-MM-dd hh:mm:ss S'))
      resolve()
    } catch (error) {
      reject(error)
    }
  })
}

/**
 * @description: 提交订单
 * @param {*}
 * @return {*}
 */
function submitOrder() {
  return new Promise(async (resolve, reject) => {
    const params = {
      url: APIS.submitOrder,
      headers: {
        Cookie: cookie,
        ...HEADERS.trade
      }
    }
    try {
      const res = await postRequestHandler(params)
      console.log('提交订单-----------√√√√√', new Date().format('yyyy-MM-dd hh:mm:ss S'))
      resolve(res.json())
    } catch (error) {
      reject(error)
    }
  })
}

/**
 * @description: 购物车勾选单个商品
 * @param {*}
 * @return {*}
 */
function cartCheckSingle() {
  return new Promise(async (resolve, reject) => {
    const params = {
      url: APIS.cartCheckSingle + `?${qs.stringify({
        functionId: 'pcCart_jc_cartCheckSingle',
        appid: 'JDC_mall_cart',
        body: JSON.stringify({ operations: [{ TheSkus: [{ Id: pid }] }] })
      })}`,
      headers: {
        Cookie: cookie,
        ...HEADERS.cart
      }
    }
    try {
      const res = await getRequestHandler(params)
      console.log('勾选商品-----------√√√√√', new Date().format('yyyy-MM-dd hh:mm:ss S'))
      resolve(res.json())
    } catch (error) {
      reject(error)
    }
  })
}

main();

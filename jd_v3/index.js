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

let cookie = ''; // JD cookie

const { pid, time, pcount, timeCut, timeSleep } = require('./config')

const timeStamp = +new Date(time);

const puppeteer = require('puppeteer');

const { JDLoginURL, JDCartURL } = require('./urls')

const { parseCookie, writeCookieToLocal, writeLogsToLocal, sleep } = require('./utils')

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

    // 抢购时间
    console.log(`抢购时间：${time}`);

    // 抢购倒计时
    await loopAndStart(startOrder, timeSleep)

    resolve()
  })
}

/**
 * @description: 循环倒计时 
 * @param {*}
 * @return {*}
 */
function loopAndStart(cb, time) {
  return new Promise(async (resolve, reject) => {
    console.log(`倒计时：${new Date().format('yyyy-MM-dd hh:mm:ss S')}`);
    while (true) {
      if (+new Date() >= timeStamp) {
        await cb()
        break
      } else {
        await sleep(time)
        console.log(`倒计时：${new Date().format('yyyy-MM-dd hh:mm:ss S')}`);
      }
    }
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
    await cartCheckSingle();
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
    const { resultData: { cartInfo } } = await getCurrentCart()
    if(cartInfo) {
      const allItemArray = [];
      const { vendors } = cartInfo
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
    } else {
      resolve()
    }
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
      console.log('加入购物车成功-----------√√√√√')
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

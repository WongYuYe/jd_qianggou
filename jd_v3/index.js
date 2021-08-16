/*
 * @Author: wyuye_
 * @Date: 2021-08-12 22:18:13
 * @Description: jd抢购node实现
 */

const fs = require('fs')

const {
  getRequestHandler,
  postRequestHandler
} = require('./request');

const { APIS, HEADERS } = require('./api')

let cookie = ''; // JD cookie

const pid = '10021246225398', // 商品ID
  time = '2021/08/16 21:51:30', // 抢购时间
  pcount = 1; // 商品数量

const timeStamp = +new Date(time);

const puppeteer = require('puppeteer');

const { JDLoginURL, JDCartURL } = require('./urls')

const { parseCookie, writeCookieToLocal } = require('./utils')

require('./DateFormat.js')

/**
 * @description: 启动puppeteer，登录京东获取cookie
 * @param {*}
 * @return {*}
 */
async function main() {
  const browser = await puppeteer.launch({
    headless: false,
  });
  const page = await browser.newPage();
  page.on('request', async req => {
    if (req.url() === JDCartURL) {
      cookie = parseCookie(await page.cookies());
      await writeCookieToLocal(cookie)

      const afterTime = timeStamp - +new Date();
      console.log(`${afterTime}毫秒后执行`)
      setTimeout(async () => {
        await startOrder()
      }, afterTime)
    }
  });
  await page.goto(JDLoginURL);
}


/**
 * @description: 开始下单流程，加入购物车-确认订单-提交订单
 * @param {*}
 * @return {*}
 */
async function startOrder() {
  await addToCart()
  await comfirmOrder()
  await submitOrder()
}

/**
 * @description: 加入购物车
 * @param {*}
 * @return {*}
 */
async function addToCart() {
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
      console.log('加入购物车-----------√√√√√', new Date().format('yyyy-MM-dd hh:mm:ss S'))
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
async function comfirmOrder() {
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
async function submitOrder() {
  return new Promise(async (resolve, reject) => {
    const params = {
      url: APIS.submitOrder,
      headers: {
        Cookie: cookie,
        ...HEADERS.trade
      }
    }
    try {
      await postRequestHandler(params)
      console.log('提交订单-----------√√√√√', new Date().format('yyyy-MM-dd hh:mm:ss S'))
      resolve()
    } catch (error) {
      reject(error)
    }
  })
}

main();

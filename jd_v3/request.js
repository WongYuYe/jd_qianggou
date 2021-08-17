/*
 * @Author: wyuye_
 * @Date: 2021-07-21 15:09:38
 * @Description: fetch request
 */
const fetch = require('node-fetch');

/**
 * @description: GET request
 * @param {*} url
 * @param {*} cookie
 * @return {*}
 */
function getRequestHandler({ url, headers = {} }) {
  return new Promise(async (resolve, reject) => {
    await fetch(url, {
      method: 'get',
      redirect: 'manual', // 手动跟踪
      headers: {
        ...headers
      }
    }).then(res => {
      resolve(res)
    }).catch(err => {
      reject(err)
    })
  })
}
/**
 * @description: POST request
 * @param {*} url
 * @param {*} data
 * @param {*} cookie
 * @return {*}
 */
function postRequestHandler({ url, data, headers = {} }) {
  return new Promise(async (resolve, reject) => {
    await fetch(url, {
      method: 'post',
      body: data,
      redirect: 'manual', // 手动跟踪
      headers: {
        ...headers
      }
    }).then(res => {
      resolve(res)
    }).catch(err => {
      reject(err)
    })
  })
}

module.exports = {
  getRequestHandler,
  postRequestHandler
}

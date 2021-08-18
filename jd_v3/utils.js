const fs = require('fs')
const os = require('os')
let options = {
  flags: 'w', // 
  encoding: 'utf8', // utf8编码
}

let stderr = fs.createWriteStream('./log.log', options);

// 创建logger
let logger = new console.Console(stderr);
module.exports = {
  parseCookie: (cookie = []) => {
    return cookie.reduce((a, { name, value }) => {
      return a += `${name}=${value}; `
    }, '')
  },
  writeCookieToLocal: async (content) => {
    try {
      const data = fs.appendFileSync('./cookie.txt', new Date() + ': ' + content + os.EOL)
      console.log('cookie写入本地成功。')
    } catch (err) {
      console.error(err)
    }
  },
  writeLogsToLocal: async (content) => {
    try {
      logger.log(content)
      console.log('log写入本地成功。')
    } catch (err) {
      console.error(err)
    }
  },
  sleep: (time) => {
    return new Promise((resolve) => setTimeout(resolve, time));
  }
}

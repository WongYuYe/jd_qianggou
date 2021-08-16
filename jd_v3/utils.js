const fs = require('fs')
module.exports = {
  parseCookie: (cookie = []) => {
    return cookie.reduce((a, { name, value }) => {
      return a += `${name}=${value}; `
    }, '')
  },
  writeCookieToLocal: async (content) => {
    try {
      const data = fs.writeFileSync('./cookie.txt', content)
      console.log('cookie写入本地成功。')
    } catch (err) {
      console.error(err)
    }
  }
}

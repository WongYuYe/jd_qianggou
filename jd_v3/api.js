/*
 * @Author: wyuye_
 * @Date: 2021-08-12 22:33:02
 * @Description: introduce it
 * @PRO: PRO address
 * @UI: UI address
 */

module.exports = {
  APIS: {
    getProductInfos:
      'https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart&appid=JDC_mall_cart&loginType=3&body={"serInfo":{"area":"15_1213_3410_59943","user-key":""},"cartExt":{"specialId":1}}',
    addToCart:
      'https://cart.jd.com/gate.action',
    getOrderInfo:
      'https://trade.jd.com/shopping/order/getOrderInfo.action?overseaMerge=1',
    submitOrder:
      'https://trade.jd.com/shopping/order/submitOrder.action?overseaMerge=1&presaleStockSign=1&overseaPurchaseCookies=&vendorRemarks={vendorRemarks}&submitOrderParam.sopNotPutInvoice=true&submitOrderParam.trackID=TestTrackId&overseaMerge=1&submitOrderParam.ignorePriceChange=0&submitOrderParam.btSupport=0&submitOrderParam.eid=CH2AWTZNVCRPTFNPJQT2SZTJ5PSK7EV4TOQB7V5CCSVCUIOQ3K5ZT5S62PYV4V4YI4Z7EUXLNLKETTZBKFJ5J6WSO4&submitOrderParam.fp=33eaf773494fe391925ae6df450d557a&submitOrderParam.jxj=1',
    checkAllOfCart: 'https://api.m.jd.com/api?functionId=pcCart_jc_cartCheckAll&appid=JDC_mall_cart&loginType=3',
    getCurrentCart: 'https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart&appid=JDC_mall_cart&loginType=3',
    cartCheckSingle: 'https://api.m.jd.com/api',
  },
  HEADERS: {
    cart: {
      // 'Cookie': cookie,
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'origin': 'https://cart.jd.com',
      'referer': 'https://cart.jd.com/',
      'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    },
    trade: {
      // 'Cookie': cookie,
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'origin': 'https://trade.jd.com',
      'referer': 'https://trade.jd.com/shopping/order/getOrderInfo.action',
      'x-requested-with': 'XMLHttpRequest',
      'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
      'authority': 'trade.jd.com',
      'method': 'post',
      'scheme': 'https',
    }
  }
}

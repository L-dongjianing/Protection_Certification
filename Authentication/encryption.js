
function randomString(length) {
    var let_name = '0123456789abcdefghijklmnopqrstuvwxyz';
    var result = '';
    for (var i = length; i > 0; --i)
        result += let_name[Math.floor(Math.random() * let_name.length)];
    return result;
}

var rr = randomString(16)
const key = CryptoJS.enc.Utf8.parse("kr94ugk9oqaxcn80");  //十六位十六进制数作为密钥
const iv = CryptoJS.enc.Utf8.parse(rr);   //十六位十六进制数作为密钥偏移量

var Untie = {
    Decrypt:function (word) {

    let py = CryptoJS.enc.Utf8.parse(word.slice(0, 16))
    let wordss = word.slice(16)
    // let words = CryptoJS.enc.Base64.parse(wordss).toString(CryptoJS.enc.Utf8)
    let words = CryptoJS.enc.Base64.parse(wordss).toString()
    let encryptedHexStr = CryptoJS.enc.Hex.parse(words);
    let srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr);
    let decrypt = CryptoJS.AES.decrypt(srcs, key, {iv: py, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7});
    let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8).replace(/None/g, "''").replace(/'/g, '"').replace(/\\xa0/g, "\xa0").replace(/\\/g, "\xa0");
    return decryptedStr.toString();
}}
var time_su = {
    getLocalTime:function (nS)  {
        return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ');
}
}

var Dense = {   //加密
Encrypt:function (word) {
    let srcs = CryptoJS.enc.Utf8.parse(word);
    let encrypted = CryptoJS.AES.encrypt(srcs, key, {iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7});
    var tt = encrypted.ciphertext.toString().toUpperCase();
    return rr.toString() + CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(tt.toString()));
}}

// var jiami = Encrypt("测试信息测试信息测试信息测试信息测试信息测试信息")
//
// var jiemi = Decrypt(jiami)
Date.prototype.Format = function (fmt) { // author: meizz
  var o = {
    "M+": this.getMonth() + 1, // 月份
    "d+": this.getDate(), // 日
    "h+": this.getHours(), // 小时
    "m+": this.getMinutes(), // 分
    "s+": this.getSeconds(), // 秒
    "q+": Math.floor((this.getMonth() + 3) / 3), // 季度
    "S": this.getMilliseconds() // 毫秒
  };
  if (/(y+)/.test(fmt))
    fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
  for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
      return fmt;
}
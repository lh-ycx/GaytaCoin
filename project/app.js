//app.js
App({
  onLaunch: function () {
    var that=this
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        if (res.code) {
          //发起网络请求
          wx.request({
            url: 'http://39.105.109.207:5000/student/login',
            data: {
              code: res.code
            },
            method: 'POST',
            header: {
              'content-type': 'application/x-www-form-urlencoded' // 默认值
            },
            success: function (res) {
              console.log(res.data)
              that.globalData.openid=res.data.openid
              console.log(that.globalData.openid)
              var exist = res.data.exist
              if(exist == 1){
                wx.redirectTo({
                  url: '../index/index'
                })
              }
            }
          })
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    })  
  },
  globalData: {
    userInfo: null,
    openId: ''
  }
})
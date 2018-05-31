// pages/authorize/authorize.js
var app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
  
  },
  onGotUserInfo: function (e) {
    //console.log(e.detail.errMsg)
    //console.log(e.detail.userInfo)
    //console.log(e.detail.rawData)
    app.globalData.userInfo = e.detail.userInfo
    //console.log(app.globalData.userInfo)
    wx.redirectTo({
      url: '../index/index',
    })
  }
})
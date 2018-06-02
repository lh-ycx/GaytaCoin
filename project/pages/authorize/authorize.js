// pages/authorize/authorize.js
var app = getApp()
var p=0
Page({

  /**
   * 页面的初始数据
   */
  data: {
    loading:false,
    percentage:100
  },
  onGotUserInfo: function (e) {
    //console.log(e.detail.errMsg)
    //console.log(e.detail.userInfo)
    //console.log(e.detail.rawData)
    app.globalData.userInfo = e.detail.userInfo
    console.log(app.globalData.userInfo)
    this.setData({
      loading:true
    })
    var that = this
    setInterval(function () {
      p=p+5
      that.setData({
        percentage:p
      })
    }, 40)
    setTimeout(function(){
      wx.redirectTo({
        url: '../index/index',
      })
    },800)
    
  }
})
// pages/authorize/authorize.js
var app = getApp()
var p=0
Page({

  /**
   * 页面的初始数据
   */
  data: {
    loading:false,
    percentage:100,
    hasUserInfo: false
  },
  onLoad:function(){
  
  },
  onGotUserInfo: function (e) {
    //console.log(e.detail.errMsg)
    //console.log(e.detail.userInfo)
    //console.log(e.detail.rawData)
    app.globalData.userInfo = e.detail.userInfo
    console.log(app.globalData.userInfo)
    this.setData({
      hasUserInfo: true
    })
    // save to storage
    wx.setStorage({
      key: 'usrinfo',
      data: e.detail.userInfo,
    })
    
    
  },
  formSubmit: function(e){
    var that = this
    if (e.detail.value['stuName'] == '' || e.detail.value['stuId'] == ''){
      wx.showToast({
        title: '请输入姓名和学号',
        icon:"none",
        duration:1500
      })
    }
    else{
      console.log(e.detail.value['stuName'])
      console.log(e.detail.value['stuId'])
      wx.request({
        url: 'http://39.105.109.207:5000/student/complete',
        data:{
          openid:app.globalData.openid,
          stuId: e.detail.value['stuId'],
          stuName: e.detail.value['stuName'],
          avatar: app.globalData.userInfo.avatarUrl
        },
        method:"POST",
        header: {
          'content-type': 'application/json' // 默认值
        },
        success: function(res){
          console.log(res)
          that.setData({
            loading: true
          })
          
          setInterval(function () {
            p = p + 5
            that.setData({
              percentage: p
            })
          }, 40)
          setTimeout(function () {
            wx.redirectTo({
              url: '../index/index',
            })
          }, 800)
        }
      })
    }
  }
})
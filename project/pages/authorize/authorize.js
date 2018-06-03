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
  },
  formSubmit: function(e){
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
          stuName: e.detail.value['stuName']
        },
        method:"POST",
        header: {
          'content-type': 'application/json' // 默认值
        },
        success: function(res){
          console.log(res)
        }
      })
    }
  }
})
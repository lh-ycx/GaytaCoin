// pages/profile/profile.js
var app=getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},
    stuId:'',
    stuName:''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
    var that = this
    wx.getStorage({
      key: 'usrinfo',
      success: function (res) {
        that.setData({
          userInfo: res.data
        })
        //console.log(that.globalData.userInfo)
      }
    })
    console.log(this.data.userInfo)
    wx.request({
      url: 'http://39.105.109.207:5000/student/personalinfo',
      data: {
        code: app.globalData.openid
      },
      method: 'POST',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success:function(res){
        if(res.data.reponse_code==1)
          that.setData({
            stuId:res.data.stuId,
            stuName:res.data.stuName
          })
      }
    })
  },

})
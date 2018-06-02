// pages/scan/scan.js
var app=getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
  
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.scanCode({
      onlyFromCamera: true,
      success: (res) => {
        //content: res.result
        //var course=res.result;
        var timestamp = Date.parse(new Date()); 
        console.log(timestamp)
        
        wx.request({
          url: 'servername/signin/signin',
          data:{
            openId:app.globalData.openId,
            course: res.result,
            start_time:res.result["timestamp"],
            current_time:timestamp
          },
          method:"POST",
          header:{
            'content-type': 'application/json' 
          },
          success:function(res){
            console.log(res.data)
            wx.showToast({
              title: '签到成功',
              icon: 'success',
              duration: 2000
            })
            wx.redirectTo({
              url: '../index/index'
            })
          }
        })
      }
    })
  }


})
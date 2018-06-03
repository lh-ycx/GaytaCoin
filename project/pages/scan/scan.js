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
        var cur_timestamp = Date.parse(new Date()); 
        console.log(res.result)
        var res_json=JSON.parse(res.result)
        if(res_json["timestamp"] >= cur_timestamp/1000){
          wx.request({
            url: 'http://39.105.109.207:5000/student/register',
            data:{
              openid:app.globalData.openid,
              courseId: res_json["courseId"],
              timestamp:res_json["timestamp"]
            },
            method:"POST",
            header:{
              'content-type': 'application/json' 
            },
            success:function(res){
              console.log(res.data)
              //签到成功
              if(res.data.response_code==1){
                wx.showToast({
                  title: '签到成功',
                  icon: 'success',
                  duration: 2000
                })
              }
              //迟到
              else if (res.data.response_code == 0) {
                wx.showToast({
                  title: '签到晚了哦',
                  icon: 'none',
                  duration: 2000
                })
              }
              //课程不存在
              else if (res.data.response_code == -1) {
                wx.showToast({
                  title: '课程不存在！',
                  icon: 'none',
                  duration: 2000
                })
              }
              //学生不存在
              else if (res.data.response_code == -2) {
                wx.showToast({
                  title: '学生不存在！',
                  icon: 'none',
                  duration: 2000
                })
              }
            },
            complete:function(){
              wx.redirectTo({
                url: '../index/index'
              })
            }
          })
        }
        else{
          wx.showToast({
            title: '签到晚了哦',
            icon: 'none',
            duration: 2500
          })
          wx.redirectTo({
            url: '../index/index'
          })
        }
      }
    })
  }


})
// pages/mycourse/mycoures.js
var app = getApp()
var CourseList = []

Page({

  /**
   * 页面的初始数据
   */
  data: {
    course_list:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    wx.request({
      url: 'http://39.105.109.207:5000/student/course_list',
      data: {
        openid: app.globalData.openid,
      },
      method: "POST",
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        console.log(res.data);

        if (res.data[0]["response_code"] == 1) {
          that.setData({
            course_list: res.data[1]
          })
        }

      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },
  NotIn: function (newCourseName) {
    for (var i in CourseList) {
      if (newCourseName == CourseList[i]) {
        return false;
      }
    }
    return true;
  },
  
  enter_chatroom: function(event){
    console.log(event.currentTarget.dataset.course_id)
    wx.navigateTo({
      url: '../chatroom/chatroom?course_id=' + event.currentTarget.dataset.course_id + 'course_name=' + event.currentTarget.dataset.course_name,
    })
  }
})
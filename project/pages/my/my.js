// pages/my/my.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    signinlist:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.fetchData();
  },

  fetchData: function () {
    var that = this
    /*
    get data from server
    */
    wx.request({
      url: 'http://39.105.109.207:5000/student/registerinfo',
      data: {
        openid: app.globalData.openid,
      },
      method: "POST",
      header: {
        'content-type': 'application/json'
      },
      success:function(res){
        if(res.data.respose_code==1){
          that.setData({
            signinlist:res.data[1]
          })
        }
      }
    })
    this.setData({
      signinlist: [
        {
          "id": 1,
          "course": "Computer Internet",
          "time": "2018/05/25 13:00",
          "student": "Li Lei",
          "iconurl": "../../images/success.png"
        },
        {
          "id": 2,
          "course": "Computer Internet",
          "time": "2018/05/28 13:00",
          "student": "Li Lei",
          "iconurl": "../../images/success.png"
        },
        {
          "id": 3,
          "course": "Computer Internet",
          "time": "2018/05/28 13:00",
          "student": "Li Lei",
          "iconurl": "../../images/success.png"
        },
        {
          "id": 4,
          "course": "Computer Internet",
          "time": "2018/05/28 13:00",
          "student": "Li Lei",
          "iconurl": "../../images/success.png"
        },
        {
          "id": 5,
          "course": "Computer Internet",
          "time": "2018/05/28 13:00",
          "student": "Li Lei",
          "iconurl": "../../images/success.png"
        },
        {
          "id": 6,
          "course": "Computer Internet",
          "time": "2018/05/28 13:00",
          "student": "Li Lei",
          "iconurl": "../../images/success.png"
        },
        {
          "id": 7,
          "course": "Computer Internet",
          "time": "2018/05/28 13:00",
          "student": "Li Lei",
          "iconurl": "../../images/success.png"
        }
      ]
    })

  }
})
// pages/my/my.js
var app=getApp()

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
        console.log(res.data)
        if(res.data[0]["response_code"] == 1){
          for(var i=0;i<res.data[1].length;i++){
            var date = new Date(res.data[1][i]["timestamp"]*1000);
            var Y = date.getFullYear();
            //月  
            var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1);
            //日  
            var D = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
            //时  
            var h = date.getHours();
            //分  
            var m = date.getMinutes();
            date = Y + "." + M + "." + D + " " + h + ":" + m;
            res.data[1][i]["date"]=date;  
          }
          that.setData({
            signinlist:res.data[1]
          })
        }
       
      }
    })
    /*
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
*/
  }
})
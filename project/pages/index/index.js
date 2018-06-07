//index.js
//获取应用实例
var app = getApp()

Page({
  data: {
    hasUserInfo:false,
    userInfo:{},
    indexmenu: [],
  },
  //事件处理函数
  fetchData: function () {
    this.setData({
      indexmenu: [
        {
          'id':0,
          'icon': './../../images/scan1.png',
          'text': '扫码签到',
          'url': 'scan'
        },       
        {
          'id':1,
          'icon': './../../images/my1.png',
          'text': '我的签到',
          'url': 'my'
        }
      ]
    })
  },
  onLoad: function () {
    
    var that = this
    this.fetchData();
    wx.getStorage({
      key: 'usrinfo',
      success: function (res) {
        that.setData({
          userInfo: res.data,
          hasUserInfo:true
        })
        //console.log(that.globalData.userInfo)
      }
    })
    
    //console.log(this.data.userInfo)
  },
  
  nav_changeImg: function(event){
    //console.log(event['target']['id'])
    if(event['target']['id']==0){
      this.setData({
        indexmenu: [
          {
            'id': 0,
            'icon': './../../images/scan_ontap.png',
            'text': '扫码签到',
          },
          {
            'id': 1,
            'icon': './../../images/my1.png',
            'text': '我的签到',
          }
        ]
      })
      /*
      wx.navigateTo({
        url: '../scan/scan'
      })
      */
      wx.scanCode({
        onlyFromCamera: true,
        success: (res) => {
          //content: res.result
          //var course=res.result;
          var cur_timestamp = Date.parse(new Date());
          cur_timestamp = cur_timestamp / 1000;
          console.log(res.result)
          var res_json = JSON.parse(res.result)
          if (res_json["timestamp"] >= cur_timestamp) {
            wx.request({
              url: 'http://39.105.109.207:5000/student/register',
              data: {
                openid: app.globalData.openid,
                courseId: res_json["courseId"],
                timestamp: cur_timestamp
              },
              method: "POST",
              header: {
                'content-type': 'application/json'
              },
              success: function (res) {
                console.log(res.data)
                //签到成功
                if (res.data.response_code == 1) {
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
              complete: function () {
                wx.redirectTo({
                  url: '../index/index'
                })
              }
            })
          }
          else {
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
    else{
      this.setData({
        indexmenu: [
          {
            'id': 0,
            'icon': './../../images/scan1.png',
            'text': '扫码签到',
          },
          {
            'id': 1,
            'icon': './../../images/my_ontap.png',
            'text': '我的签到',
          }
        ]
      })
      wx.navigateTo({
        url: '../my/my'
      })
    }
  },
  onHide: function(){
    this.fetchData()
  },
  showStuInfo:function(){
    wx.navigateTo({
      url: '../profile/profile'
    })
  },
  onGotUserInfo: function (e) {
    app.globalData.userInfo = e.detail.userInfo
    console.log(app.globalData.userInfo)
    // save to storage
    wx.setStorage({
      key: 'usrinfo',
      data: e.detail.userInfo,
    })
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo:true
    })
  }
})

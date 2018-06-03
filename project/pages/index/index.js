//index.js
//获取应用实例
var app = getApp()

Page({
  data: {
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
          userInfo: res.data
        })
        //console.log(that.globalData.userInfo)
      }
    })
    
    console.log(this.data.userInfo)
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
      wx.navigateTo({
        url: '../scan/scan'
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
  }
})

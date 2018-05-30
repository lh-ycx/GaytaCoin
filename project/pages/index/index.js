//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    indexmenu: [],
  },
  //事件处理函数
  fetchData: function () {
    this.setData({
      indexmenu: [
        {
          'id':0,
          'icon': './../../images/scan.png',
          'text': '扫码签到',
          'url': 'scan'
        },       
        {
          'id':1,
          'icon': './../../images/my.png',
          'text': '我的签到',
          'url': 'my'
        }
      ]
    })
  },
  onLoad: function () {
    this.fetchData();
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
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
            'icon': './../../images/my.png',
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
            'icon': './../../images/scan.png',
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
  }
})

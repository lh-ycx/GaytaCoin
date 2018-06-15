//index.js
//获取应用实例
var app = getApp()
var EARTH_RADIUS = 6378.137; //地球半径
var longitude_base1 = 39.98942;
var latitude_base1 = 116.312910;
var IndexMenu = [
  {
    'id': 0,
    'icon': './../../images/scan.png',
    'text': '扫码签到',
    'url': 'scan'
  },
  {
    'id': 1,
    'icon': './../../images/my.png',
    'text': '我的签到',
    'url': 'my'
  },
  {
    'id': 2,
    'icon': './../../images/mycourse.png',
    'text': '我的课程',
    'url': 'mycourse'
  }
]

Page({
  data: {
    hasUserInfo:false,
    userInfo:{},
    indexmenu: [] 
  },
  
  //事件处理函数
  fetchData: function () {
    this.setData({
      indexmenu: [
        {
          'id': 0,
          'icon': './../../images/scan.png',
          'text': '扫码签到',
          'url': 'scan'
        },
        {
          'id': 1,
          'icon': './../../images/my.png',
          'text': '我的签到',
          'url': 'my'
        },
        {
          'id': 2,
          'icon': './../../images/mycourse.png',
          'text': '我的课程',
          'url': 'mycourse'
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
    wx.getLocation({
      type: 'gcj02', // use gcj02 which is the tencent map
      success: function (res) {
        that.setData({
          latitude: res.latitude,
          longitude: res.longitude
        })
        console.log(that.data.latitude, that.data.longitude)
      },
      fail:function(){
        wx.showToast({
          title: '请授权使用地理位置',
          icon: 'none',
          duration: 2000
        })
        
      }
    })
    var dist = this.getDistance(latitude_base1,longitude_base1, 116.310089, 39.98853)
    //console.log(dist)
  },  
  nav_changeImg: function(event){
    var that = this
    //console.log(event['target']['id'])
    if(event['target']['id']==0){
      IndexMenu[0]['icon'] = './../../images/scan_ontap.png'
      IndexMenu[1]['icon'] = './../../images/my.png'
      IndexMenu[2]['icon'] = './../../images/mycourse.png'
      this.setData({
        indexmenu: IndexMenu
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
          var longitude_base = res_json["longitude"]
          var latitude_base = res_json["latitude"]
          // if stu.location is too far from the teacher
          var distance = that.getDistance(latitude_base, longitude_base, that.data.latitude, that.data.longitude)
          if(distance > 0.15){
            console.log(distance)
            wx.showToast({
              title: '你离教室有点远哦',
              icon: 'none',
              duration: 2000
            })
          }
          // if the stu is too late to sign in
          // give 2 min error range
          else if (res_json["timestamp"] >= cur_timestamp - 120) {
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
                wx.navigateTo({
                  url: '../my/my'
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
    else if(event['target']['id']==1){
      IndexMenu[0]['icon'] = './../../images/scan.png'
      IndexMenu[1]['icon'] = './../../images/my_ontap.png'
      IndexMenu[2]['icon'] = './../../images/mycourse.png'
      this.setData({
        indexmenu: IndexMenu
      })
      wx.navigateTo({
        url: '../my/my'
      })
    }
    else {
      IndexMenu[0]['icon'] = './../../images/scan.png'
      IndexMenu[1]['icon'] = './../../images/my.png'
      IndexMenu[2]['icon'] = './../../images/mycourse_ontap.png'
      this.setData({
        indexmenu: IndexMenu
      })
      wx.navigateTo({
        url: '../mycourse/mycourse'
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
    console.log("in function")
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
  },
  rad: function(d) {
    return d * Math.PI / 180.0;
  },
  getDistance:function (lng1, lat1, lng2, lat2) {
    var radLat1 = this.rad(lat1);
    var radLat2 = this.rad(lat2);
    var a = radLat1 - radLat2;
    var b = this.rad(lng1) - this.rad(lng2);
    var s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a / 2), 2)
      + Math.cos(radLat1) * Math.cos(radLat2)
      * Math.pow(Math.sin(b / 2), 2)));
    s = s * EARTH_RADIUS;
    s = Math.round(s * 10000) / 10000;
    return s;//返回数值单位：公里
  }
})

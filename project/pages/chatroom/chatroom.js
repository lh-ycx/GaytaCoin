// pages/chatroom/chatroom.js
var app = getApp();
var timer;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    course_id: -1,
    course_name: '',
    inputPosition: 0,
    inputHeight: 0,
    input_msg:'',
    msg:[],
    openid:'',
    msg_height: 0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options)
    this.setData({
      course_id: parseInt(options.course_id),
      course_name: options.course_name,
      openid: app.globalData.openid
    })
    var that = this
    // 获取系统信息
    wx.getSystemInfo({
      success: function (res) {
        console.log(res);
        // 可使用窗口宽度、高度
        console.log('height=' + res.windowHeight);
        console.log('width=' + res.windowWidth);
        // 计算主体部分高度,单位为px
        that.setData({
          msg_height: res.windowHeight - 90
        })
      }
    })
    //console.log(app.globalData.userInfo)
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
    this.fetchData();
    this.countDown();
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    clearTimeout(timer);
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    clearTimeout(timer);
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },
  countDown: function () {
    var that = this;
    
    timer = setTimeout(function () {
      console.log("----Countdown----");
      console.log(that.data.room_id);
      that.fetchData();
      that.countDown();
    }, 1000);
    
  },
  fetchData: function () {
    var that = this;
    wx.request({
      url: 'http://39.105.109.207:5000/room/get_room',
      data: {
        room_id: parseInt(that.data.course_id)
      },
      method: 'POST',
      dataType: 'json',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) {
        console.log('success')
        console.log(res.data);
        if (res.data.response_code != 0) {
          that.setData({
            room_id: res.data[1].room_id,
            room_owner: res.data[1].owner,
            users: res.data[1].users,
            msg: res.data[1].messages,
          });
          console.log("msg:")
          console.log(that.data.msg)
        }
        else {
          wx.showModal({
            title: '',
            content: '该房间已被销毁',
            success: function (res) {
              if (res.confirm) {
                wx.switchTab({
                  url: '../index/index',
                })
              }
            }
          })
        }
        console.log('---------')
      },
      fail: function () {
        console.log('fail');
      }
    });
  },
  viewDetail: function(){
    wx.navigateTo({
      url: '../chatdetail/chatdetail?course_id='+this.data.course_id + '&course_name=' + this.data.course_name,
    })
  },
  inputMsg: function(event){
    this.setData({
      input_msg: event.detail.value
    })
    //console.log(this.data.input_msg)
  },
  handlefocus: function(event){
    //console.log(event.detail.height)
    this.setData({
      inputPosition: event.detail.height
    })
    //console.log(this.data.inputPosition)
  },
  handleblur: function(){
    this.setData({
      inputPosition: 0
    })
  },
  submitMsg: function(){
    var that = this
    if (that.data.input_msg.length == 0) {
      console.log('empty input');
      wx.showToast({
        title: '输入不能为空',
        duration: 500,
      })
      return;
    }
    console.log("openid:")
    console.log(app.globalData.openid)
    wx.request({
      url: 'http://39.105.109.207:5000/room/send_message',
      data: {
        room_id: parseInt(that.data.course_id),
        open_id: app.globalData.openid,
        message: that.data.input_msg,
      },
      dataType: 'json',
      method: 'POST',
      success: function (res) { 
        that.setData({
          input_msg: ''
        })
      },
      fail: function () {
        wx.showToast({
          title: 'fail',
          icon: 'none',
          duration: 500,
        })
      }
    })
  }
  
})
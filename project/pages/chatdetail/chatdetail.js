// pages/chatdetail/chatdetail.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    course_id: -1,
    course_name: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      course_id: options.course_id,
      course_name: options.course_name
    })
    this.fetchData();
  },
  fetchData: function(){
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
      success: function(res){
        console.log(res.data)
        if (res.data.response_code != 0) {
          that.setData({
            room_owner: res.data[1].owner,
            users: res.data[1].users,
          });
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

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  }
})
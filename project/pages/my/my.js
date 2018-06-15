// pages/my/my.js
var app=getApp()
var CourseList = []
var SigninList = []
Page({

  /**
   * 页面的初始数据
   */
  data: {
    signinlist:[],
    course_list:[],
    course_index:0
  },
  bindPickerChange: function (e) {
    this.setData({
      course_index: e.detail.value
    });
    if (this.data.course_index == 0) {
      for (var i in SigninList) {
        SigninList[i]["ifshow"] = true;
      }
    }
    else{
      for(var i in SigninList){
        if(SigninList[i]["courseName"] == this.data.course_list[this.data.course_index]){
          SigninList[i]["ifshow"] = true;
        }
        else {
          SigninList[i]["ifshow"] = false;
        }
      }
    }
    this.setData({
      signinlist:SigninList
    })
  },
  NotIn: function(newCourseName){
    for(var i in CourseList){
      if(newCourseName == CourseList[i]){
        return false;
      }
    }
    return true;
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
        console.log(res.data);
        CourseList[0] = "所有";
       
        if(res.data[0]["response_code"] == 1){
          SigninList = res.data[1];
          for(var i=0;i<SigninList.length;i++){
            var date = new Date(SigninList[i]["timestamp"]*1000);
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
            SigninList[i]["date"]=date; 
            SigninList[i]["ifshow"]=true; 
            if(that.NotIn(SigninList[i]["courseName"])){
              CourseList.push(SigninList[i]["courseName"]);
              //console.log(course_list)
            }
          }

          that.setData({
            signinlist:SigninList,
            course_list:CourseList
          })
        }
       
      }
    })
    
  }
})
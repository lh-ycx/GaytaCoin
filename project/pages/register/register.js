var util = require('../../utils/util.js');
var app = getApp();

Page({
  data: {
    showTopTips: false,
    errorMsg: ""
  },
  onLoad: function () {
    var that = this;
    wx.getSystemInfo({
      success: function (res) {
        that.setData({
          windowHeight: res.windowHeight,
          windowWidth: res.windowWidth
        })
      }
    });
  },

  formSubmit: function (e) {
    // form 表单取值，格式 e.detail.value.name(name为input中自定义name值) ；使用条件：需通过<form bindsubmit="formSubmit">与<button formType="submit">一起使用  
    var stuName = e.detail.value.stuName;
    var stuID = e.detail.value.stuID;
    var substuID = e.detail.value.substuID;
    var that = this;
    // 判断账号是否为空和判断该账号名是否被注册  
    if ("" == util.trim(stuName)) {
      util.isError("姓名不能为空", that);
      return;
    } else {
      util.clearError(that);
      /*app.ajax.req('/register/checkLoginName', {
        "loginName": account
      }, function (res) {
        if (!res) {
          util.isError("账号已经被注册过", that);
          return;
        }
      });*/
    }
    // 判断学号是否为空  
    if ("" == util.trim(stuID)) {
      util.isError("学号不能为空", that);
      return;
    } else {
      util.clearError(that);
    }
    // 两个学号必须一致  
    if (substuID != stuID) {
      util.isError("输入学号不一致", that);
      return;
    } else {
      util.clearError(that);
    }
    if(util.islegal(stuID)==null)
    {
      util.isError("请输入合法学号",that);
      return;
    }
    else
    {
      util.clearError(that);
    }
    // 验证都通过了执行注册方法  
    /*app.ajax.req('/itdragon/register', {
      "account": account,
      "password": password
    }, function (res) {
      if (true == res) {
        // 显示模态弹窗  
        wx.showModal({
          title: '注册状态',
          content: '注册成功，请点击确定登录吧',
          success: function (res) {
            if (res.confirm) {
              // 点击确定后跳转登录页面并关闭当前页面  
              wx.redirectTo({
                url: '../login/login?account=' + account + '&password?=' + password + ''
              })
            }
          }
        })
      } else {
        // 显示消息提示框  
        wx.showToast({
          title: '注册失败',
          icon: 'error',
          duration: 2000
        })
      }
    });*/
    wx.request({
      url: 'http://localhost:5000/signup', //仅为示例，并非真实的接口地址
      data: {
        'stuName': stuName,
        'stuID': stuID
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: 'POST',
      success: function (res) {
        console.log(res.data)
      }
    })
  }
})  
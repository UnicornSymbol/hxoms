$(function(){
    $.checkName=function(value,parent,msg){
        if($.trim(value) == ""){
            parent.addClass("has-error has-feedback")
            parent.append("<span id='errorinfo' class='form-control-errorinfo'>"+msg+"</span>")
            parent.append("<span id='feedback' class='glyphicon glyphicon-remove form-control-feedback'></span>")
        }
        else{
            parent.addClass("has-success has-feedback")
            parent.append("<span id='feedback' class='glyphicon glyphicon-ok form-control-feedback'></span>")
        }
    };

    $.checkPhone=function(value,parent){
        if($.trim(value) == "" || ($.trim(value) != "" && !/^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/.test($.trim(value)))){
            parent.addClass("has-error has-feedback")
            parent.append("<span id='errorinfo' class='form-control-errorinfo'>请输入正确的手机号码</span>")
            parent.append("<span id='feedback' class='glyphicon glyphicon-remove form-control-feedback'></span>")
        }
        else{
            parent.addClass("has-success has-feedback")
            parent.append("<span id='feedback' class='glyphicon glyphicon-ok form-control-feedback'></span>")
        }
    };

    $.checkEmail=function(value,parent){
        //if($.trim(value) == "" || ($.trim(value) != "" && !/.+@.+\.[a-zA-Z]{2,4}$/.test($.trim(value)))){
        if($.trim(value) == "" || ($.trim(value) != "" && !/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z]{2,63})$/.test($.trim(value)))){
            parent.addClass("has-error has-feedback")
            parent.append("<span id='errorinfo' class='form-control-errorinfo'>请输入正确的邮箱地址</span>")
            parent.append("<span id='feedback' class='glyphicon glyphicon-remove form-control-feedback'></span>")
        }
        else{
            parent.addClass("has-success has-feedback")
            parent.append("<span id='feedback' class='glyphicon glyphicon-ok form-control-feedback'></span>")
        }
    };

    //(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}\.?$)
    $.checkWebsite=function(value,parent){
        var reg = /(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}\.?$)/
        if($.trim(value) == "" || ($.trim(value) != "" && !reg.test($.trim(value)))){
            parent.addClass("has-error has-feedback")
            parent.append("<span id='errorinfo' class='form-control-errorinfo'>请输入正确的网站地址</span>")
            parent.append("<span id='feedback' class='glyphicon glyphicon-remove form-control-feedback'></span>")
        }
        else{
            parent.addClass("has-success has-feedback")
            parent.append("<span id='feedback' class='glyphicon glyphicon-ok form-control-feedback'></span>")
        }                       
    };

    $.checkIp=function(value,parent){
        parent.removeClass("has-success")
        parent.removeClass("has-error")
        var reg =  /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
        if($.trim(value) == "" || ($.trim(value) != "" && !reg.test($.trim(value)))){
            parent.addClass("has-error has-feedback")
            parent.append("<span id='errorinfo' class='form-control-errorinfo'>请输入正确的IP地址</span>")
            parent.append("<span id='feedback' class='glyphicon glyphicon-remove form-control-feedback'></span>")
        }
        else{
            parent.addClass("has-success has-feedback")
            parent.append("<span id='feedback' class='glyphicon glyphicon-ok form-control-feedback'></span>")
        }                       
    };
});

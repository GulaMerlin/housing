function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {

$('#login_form').submit(function(e){
            e.preventDefault();
            var mobile = $('#mobile').val()
            var password = $('#password').val()
            $.ajax({
               url: '/user/login/',
               data: {
               'mobile': mobile,
               'password': password
               },
               type: 'POST',
               dataType: 'json',
               success: function(data){
                   if(data.code == '7005'){
                       $('#mobile-err span').html(data.msg);
                       $("#mobile-err").show();
                   }else if(data.code == '7006'){
                       $('#password-err span').html(data.msg);
                       $("#password-err").show();
                   }else if(data.code =='200'){
                        location.href='/house/index/'
                   }
               },
               error: function(data){
                   alert('ERROR!')
               }
            })
        })

    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
    });
})
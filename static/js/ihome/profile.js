function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
$(document).ready(function(){
$.ajax({
        url:'/user/user_info/',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            $('#user-avatar').attr("src", '/static/media/User/'+data.avatar);
            $('#user-name').val(data.name);
        },
        error: function(data){
            alert('获取信息失败')
        }
    });
    $('#form-avatar').submit(function(evt){
        evt.preventDefault();
        $(this).ajaxSubmit({
            url: '/user/profile_image/',
            type: 'POST',
            dataType: 'json',
            success: function(data){
                if (data.code == 200){
                    $('#mobile-err span').text('上传成功')
                    $('#mobile-err').show()
                }else if(data.code == 7010){
                    $('#mobile-err span').text(data.msg)
                    $('#mobile-err').show()
                }
            },
            error: function(data){
                $('#mobile-err span').text('上传失败')
                    $('#mobile-err').show()
            },
        });
    });
    $('#form-name').submit(function(evt){
        evt.preventDefault();
        $(this).ajaxSubmit({
            url: '/user/profile/',
            type: 'POST',
            dataType: 'json',
            data:{'name':name},
            success: function(data){
                if (data.code == 200){
                    $('#name-err').text('修改成功')
                    $('#name-err').show()
                }else if(data.code == 7011){
                    $('#name-err').text(data.msg)
                    $('#name-err').show()
                }
            },
            error: function(data){
                $('#name-err').text('修改失败')
                $('#name-err').show()
            },
        });
    });

})


function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
$.ajax({
            url: '/user/my/',
            type: 'post',
            datatype: 'json',
            success: function(data){
                if(!data.name){
                    $('#user-name').text('并未填写用户名');
                }else{
                $('#user-name').text(data.name);
                }
                if(!data.avatar){

                } else{
                    $('#user-avatar').attr("src", '/static/media/user/'+data.avatar);
                }
                $('#user-mobile').text(data.phone)

            },
            error: function(data){
                alert('获取信息失败！')
            }
        });

});


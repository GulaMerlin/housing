$(document).ready(function(){

    $(".auth-warn").show();
    $.ajax({
        url: '/user/my_house_info/',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            if(data.code == 200){
               $.each(data.data, function(index, house){
                    $('#houses-list').append("<li><a href='/house/detail/"+ house.id +"'><div class='house-title'><h3>房屋ID:"+ house.id +" —— "+ house.title +"</h3></div><div class='house-content'><img src='/static/media/pic/"+ house.image +"'><div class='house-text'><ul><li>位于："+ house.area +"</li><li>价格：￥"+ house.price +"/晚</li><li>发布时间："+ house.create_time +"</li></ul></div></div></a></li>")
               })
            }
        },
        error: function(data){
            alert('获取房屋信息失败')
        }
    });
        $.ajax({
        url: '/user/auth_real_name/',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            if(data.code == 7013){
                $('#not_attestation').hide()
                $('#houses-list').show()
            }else if(data.code == 2){
                $('#not_attestation').show()
                $('#houses-list').hide()
            }
        }
    });

})
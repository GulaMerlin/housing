function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $('#form-auth').submit(function(evt){
        evt.preventDefault();
        var real_name = $('#real-name').val();
        var id_card = $('#id-card').val();
        $(this).ajaxSubmit({
            url: '/user/auth/',
            type: 'POST',
            dataType: 'json',
            data:{'real_name':real_name, 'id_card': id_card},
            success: function(data){
                if (data.code == 200){
                    $('#msg').text(data.msg)
                    $('#msg').show()
                }else if(data.code == 7013){
                    $('#msg').text(data.msg)
                    $('#msg').show()
                }else if(data.code == 7014){
                    $('#msg').text(data.msg)
                    $('#msg').show()
                }else if(data.code == 7015){
                    $('#msg').text(data.msg)
                    $('#msg').show()
                }
            },
            error: function(data){
                $('#msg').text('保存失败')
                $('#msg').show()
            },
        });
    });

        $.ajax({
            url: '/user/auth_real_name/',
            type: 'GET',
            dataType: 'json',
            success: function(data){
                if(data.code == 7013){
                    $('#real-name').val(data.name).attr('disabled', 'disabled')
                    $('#id-card').val(data.id_card).attr('disabled', 'disabled')
                    $('#submit').hide()
                }
            }
        });

})

//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-accept").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-accept").attr("order-id", orderId);
    });
    $(".order-reject").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-reject").attr("order-id", orderId);
    });




            $.ajax({
                url: '/order/order_status/',
                type: 'GET',
                dataType: 'json',
                success: function(data){
                    for(var i=0;i<data[1].length;i++)
                    {
                    if(data[1][i].status == 'WAIT_PAYMENT'){
                        $("#"+ data[1][i].order_id).hide();
                    }else if(data[1][i].status == 'REJECTED'){
                        $("#"+ data[1][i].order_id).hide();
                    }else{
                        $("#"+ data[1][i].order_id).show();
                    }
                    }
                },
                error: function(){
                    alert('获取订单状态失败')
                }

            })

});

    var orderId = 0
        $.ajax({
            url: '/order/lorders/',
            dataType: 'json',
            type: 'POST',
            success: function(data){
                if(data[0].code == 200){

                    for(var i=0;i<data[1].length ;i++){
                    $('.orders-list').append("<li order-id="+ data[1][i].order_id +"><div class='order-title'><h3>订单编号："+ data[1][i].order_id +"</h3><div class='fr order-operate' id="+ data[1][i].order_id +"><button type='button' class='btn btn-success order-accept' data-toggle='modal' data-target='#accept-modal' >接单</button><button type='button' class='btn btn-danger order-reject' data-toggle='modal' data-target='#reject-modal' >拒单</button></div></div><div class='order-content'><img src='/static/media/pic/"+ data[1][i].image +"'><div class='order-text'><h3>"+ data[1][i].house_title +"</h3><ul><li>创建时间："+ data[1][i].create_date +"</li><li>入住日期："+ data[1][i].begin_date +"</li><li>离开日期："+ data[1][i].end_date +"</li><li>合计金额：￥"+ data[1][i].amount +"(共"+ data[1][i].days +"晚)</li><li>订单状态：<span>"+ data[1][i].status +"</span></li><li>客户评价： "+ data[1][i].comment +"</li></ul></div></div></li>")
                    }

                    $(".order-accept").on("click", function(){
                        orderId = $(this).parents("li").attr("order-id");
                    });
                    $(".order-reject").on("click", function(){
                        orderId = $(this).parents("li").attr("order-id");
                    });

                }
            },
            error: function(){
                alert('获取订单失败')
            }
        });
            function accept(){
                $.ajax({
                    url: '/order/up_order/',
                    dataType: 'json',
                    type: 'POST',
                    data: {'lorder_id': orderId, 'code': 1},
                    success: function(data){
                        if(data.code == 200){
                            $("#"+ orderId).hide();
                        }
                    },
                    error: function(){
                        alert('获取订单失败')
                    }
                });
            };


            function reject(){
            var comment = $('#reject-reason').val()
                $.ajax({
                    url: '/order/up_order/',
                    dataType: 'json',
                    type: 'POST',
                    data: {'lorder_id': orderId, 'code': 2, 'comment': comment},
                    success: function(data){
                        if(data.code == 200){
                            $("#"+ orderId).hide();
                        }else if(data.code == 7016){
                            alert(data.msg);
                        }
                    },
                    error: function(){
                        alert('获取订单失败')
                    }
                });
            };
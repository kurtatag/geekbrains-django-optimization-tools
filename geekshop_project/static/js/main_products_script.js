window.onload = function () {

    $('body').delegate('.tab-list a', 'click', function(){
        event.preventDefault();
        var link = this.href;
        $.ajax({
            url: link,
            success: function (data) {
                $('.product-list-ajax').html(data.result);
            },
        });
    });

    $('body').delegate('.pagination a', 'click', function(){
        event.preventDefault();
        var link = this.href;
        $.ajax({
            url: link,
            success: function (data) {
                $('.product-list-ajax').html(data.result);
            },
        });
    });

}
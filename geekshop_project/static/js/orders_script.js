window.onload = function () {

    calculate_totals();


    $('.order_form').on('click', 'input[type="number"]', function () {
        calculate_totals();
    });


    $('.order_form select').change(function () {
        orderitem_num = parseInt($(this).attr("name").replace('orderitems-', '').replace('-product', ''));

        var target = $(this).closest("tr").children(".td3");
        var product_id = $(this).children("option:selected").val();
        var class_name = $(this).attr("name").replace('product', 'price');

        if (!product_id) {
            target.html(`<span class=\"${class_name}\">0</span>`);
            calculate_totals();
            return;
        }

        $.ajax({
            url: "/products/price/" + product_id + "/json/",
            success: function (data) {
                var new_price = parseFloat(data.price);
                var template = `<span class="${class_name}">
                                    ${Number(new_price).toFixed(2)}
                                </span>`;
                target.html(template);
                calculate_totals();
            },
        });

    });


    $('.formset_row').formset({
        addText: 'add new product',
        deleteText: 'delete',
        prefix: 'orderitems',
        removed: calculate_totals,
    });

}


function calculate_totals() {
    var _quantity, _price, _cost;
    var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    var order_total_quantity = 0;
    var order_total_cost = 0;

    for (var i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val()) || 0;
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.')) || 0;
        _cost = _quantity * _price;

        if (!_price) {
            continue;
        }

        if ($('input[name="orderitems-' + i + '-quantity"]').parent().parent().css("display") == 'none') {
            continue;
        }

        console.log($('.order_form select').children("option:selected").val());

        order_total_quantity += _quantity;
        order_total_cost += _cost;
    }

    $('.order_total_quantity').html(order_total_quantity.toString());
    $('.order_total_cost').html(Number(order_total_cost).toFixed(2)).toString();
}

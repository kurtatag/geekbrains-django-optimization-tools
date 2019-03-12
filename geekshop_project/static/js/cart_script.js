window.onload = function () {
    $('.minus-btn').on('click', function (e) {
        e.preventDefault();
        var $this = $(this);
        var cart_product_pk = $this.closest('div').siblings(".cart-product-id").text();
        var product_total_price = $this.closest('div').next(".total-price");
        var $input = $this.closest('div').find('input');
        var value = parseInt($input.val());

        if (value > 1) {
            value = value - 1;
        } else {
            value = 1;
        }

        $input.val(value);

        $.ajax({
            url: "/cart/edit/" + cart_product_pk + "/" + value + "/",
            success: function (data) {
                product_total_price.html("$" + data.product_price_total);
                $('#cart-price-total').text(data.cart_price_total);
                $('#cart-items-total').text(data.cart_items_total);
            },
        });

    });

    $('.plus-btn').on('click', function (e) {
        e.preventDefault();
        var $this = $(this);
        var cart_product_pk = $this.closest('div').siblings(".cart-product-id").text();
        var product_total_price = $this.closest('div').next(".total-price");
        var $input = $this.closest('div').find('input');

        var value = parseInt($input.val());

        if (value < 100) {
            value = value + 1;
        } else {
            value = 100;
        }

        $input.val(value);

        $.ajax({
            url: "/cart/edit/" + cart_product_pk + "/" + value + "/",
            success: function (data) {
                product_total_price.html("$" + data.product_price_total);
                $('#cart-price-total').text(data.cart_price_total);
                $('#cart-items-total').text(data.cart_items_total);
            },
        });
    });
}

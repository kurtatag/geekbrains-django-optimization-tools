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


    $('.dropdown-item').on('click', function(){
        var category = $(this).text();
        $('#dropdownMenuButton').text(category);

        $.ajax({
            url: `/admin/products/list/${category.toLowerCase()}/`,
            success: function (data) {
                page_refresh(data);
            },
        });

    });


    $('body').delegate('.page-link', 'click', function(){
        var page = $(this).data("val");
        var category = $('#dropdownMenuButton').text().trim().toLowerCase();

        $.ajax({
            url: `/admin/products/list/${category}/?page=${page}`,
            success: function (data) {
                page_refresh(data);
            },
        });

    });

    function page_refresh(data) {
        var products = data.products;
        var has_other_pages = data.page_info.has_other_pages;
        var has_previous = data.page_info.has_previous;
        var has_next = data.page_info.has_next;
        var page_range = data.page_info.page_range;
        var page_number = data.page_info.page_number;

        var products_element = $('#prducts-by-category');
        products_element.html("");
        for (var i = 0; i < products.length; i++) {
            if (products[i].is_active) {
                products_element.append(`<li class="list-group-item d-flex justify-content-between align-items-center">
                                    <a href="/admin/products/read/${products[i].product_id}/" class="text-dark">
                                        ${products[i].product_name}
                                    </a>
                                    <a class="btn btn-primary" href="/admin/products/read/${products[i].product_id}/" role="button">View</a>
                                </li>`);
            } else {
                products_element.append(`<li class="list-group-item d-flex justify-content-between align-items-center">
                                    <a href="/admin/products/read/${products[i].product_id}/" class="text-dark">
                                        ${products[i].product_name} <span class="badge badge-dark">Not Active</span>
                                    </a>
                                    <a class="btn btn-primary" href="/admin/products/read/${products[i].product_id}/" role="button">View</a>
                                </li>`);
            }
        }


        var pagination_element = $('.pagination');
        pagination_element.html("");
        if (!has_other_pages) {
            return 0;
        }
        if (has_previous) {
            pagination_element.append(`<li class="page-item">
                                         <a class="page-link" data-val="${page_number - 1}">&laquo;</a>
                                       </li>`);
        } else {
            pagination_element.append(`<li class="page-item disabled">
                                         <a class="page-link">&laquo;</a>
                                       </li>`);
        }

        for (var i = 0; i < page_range.length; i++) {
            if (page_number == page_range[i]) {
                pagination_element.append(`<li class="page-item active">
                                         <a class="page-link" data-val="${page_range[i]}">${page_range[i]}</a>
                                       </li>`);
            } else {
                pagination_element.append(`<li class="page-item">
                                         <a class="page-link" data-val="${page_range[i]}">${page_range[i]}</a>
                                       </li>`);
            }

        }

        if (has_next) {
            pagination_element.append(`<li class="page-item">
                                         <a class="page-link" data-val="${page_number + 1}">&raquo;</a>
                                       </li>`);
        } else {
            pagination_element.append(`<li class="page-item disabled">
                                         <a class="page-link">&raquo;</a>
                                       </li>`);
        }
    }

}

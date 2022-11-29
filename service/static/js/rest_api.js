$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_price").val(res.price);
        if (res.is_on_shelf == true) {
            $("#product_onshelf").val("true");
        } else {
            $("#product_onshelf").val("false");
        }
        $("#product_description").val(res.description);
        $("#product_likes").val(res.like_num);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_id").val("");
        $("#product_name").val("");
        $("#product_price").val("");
        $("#product_onshelf").val("");
        $("#product_description").val("");
        $("#product_likes").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    const URL = '/products'

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#product_name").val();
        let price = parseInt($("#product_price").val());
        let description = $("#product_description").val();

        let data = {
            name,
            price,
            description
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: URL,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        let productId = $('#product_id').val();
        let name = $("#product_name").val();
        let price = parseInt($("#product_price").val());
        let description = $("#product_description").val();

        let data = {
            name,
            price,
            description
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `${URL}/${productId}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        let productId = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `${URL}/${productId}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let productId = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `${URL}/${productId}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Product has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Like a Product
    // ****************************************

    $("#like-btn").click(function () {

        let productId = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `${URL}/${productId}/like`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Product has been liked!")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Dislike a Product
    // ****************************************

    $("#dislike-btn").click(function () {

        let productId = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `${URL}/${productId}/dislike`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Product has been disliked!")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Like a Product
    // ****************************************

    $("#on-shelf-btn").click(function () {

        let productId = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `${URL}/${productId}/on-shelf`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Product is now on shelf!")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Like a Product
    // ****************************************

    $("#off-shelf-btn").click(function () {

        let productId = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `${URL}/${productId}/off-shelf`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Product is now off shelf!")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#product_name").val();
        let description = $("#product_description").val();
        let price = parseInt($("#product_price").val());

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (description) {
            if (queryString.length > 0) {
                queryString += '&description=' + description
            } else {
                queryString += 'description=' + description
            }
        }
        if (price) {
            if (queryString.length > 0) {
                queryString += '&price=' + price
            } else {
                queryString += 'price=' + price
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: queryString ? `${URL}?${queryString}` : `${URL}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '<th class="col-md-3">Description</th>'
            table += '<th class="col-md-1">Like Count</th>'
            table += '<th class="col-md-1">On Shelf</th>'
            table += '</tr></thead><tbody>'
            let firstProduct = "";
            for (let i = 0; i < res.length; i++) {
                let product = res[i];
                table += `<tr id="row_${i}"><td>${product.id}</td><td>${product.name}</td><td>${product.price}</td><td>${product.description}</td><td>${product.like_num}</td><td>${product.is_on_shelf}</td></tr>`;
                if (i == 0) {
                    firstProduct = product;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

})

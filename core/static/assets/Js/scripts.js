$(document).ready(function () {
  // Add to Cart
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();
    let food_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response);
        if (response.status === "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location.href = "/login";
          });
        } else if (response.status === "Failed") {
          swal(response.message, "", "error");
        } else {
          updateCartDisplay(response, food_id);
        }
      },
    });
  });

  // Decrease Cart Quantity
  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();
    let food_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");
    let cart_id = $(this).attr("id");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response);
        if (response.status === "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location.href = "/login";
          });
        } else if (response.status === "Failed") {
          swal(response.message, "", "error");
        } else {
          updateCartDisplay(response, food_id);
          if (window.location.pathname === "/cart/") {
            removeCartItem(response.qty, cart_id);
            checkEmptyCart();
          }
        }
      },
    });
  });

  // Delete Cart Item
  $(".delete_cart").on("click", function (e) {
    e.preventDefault();
    let cart_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");

    $.ajax({
      type: "DELETE",
      url: url,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      },
      success: function (response) {
        console.log(response);
        if (response.status === "Failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          swal(response.status, response.message, "success");
          removeCartItem(0, cart_id);
          checkEmptyCart();
        }
        applyCartAmount(
          response.cart_amount["subtotal"],
          response.cart_amount["total"],
          response.cart_amount["grand_total"]
        );
      },
    });
  });

  // Add Opening Hour
  $(".add_hour").on("click", function (e) {
    e.preventDefault();
    let day = $("#id_day").val();
    let from_hour = $("#id_from_hour").val();
    let to_hour = $("#id_to_hour").val();
    let is_closed = $("#id_is_closed").prop("checked") ? "True" : "False";
    let csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    let url = $("#add_hour_url").val();

    console.log(day, from_hour, to_hour, is_closed, csrf_token);

    if (is_closed === "True" || (day !== "" && from_hour !== "" && to_hour !== "")) {
      $.ajax({
        type: "POST",
        url: url,
        data: {
          day: day,
          from_hour: from_hour,
          to_hour: to_hour,
          is_closed: is_closed,
          csrfmiddlewaretoken: csrf_token,
        },
        success: function (response) {
          if (response.status === "success") {
            let html = createHourRow(response);
            $("table tbody").append(html);
            $("#opening_hours")[0].reset();
          } else {
            swal(response.message, "", "error");
          }
        },
      });
    } else {
      swal("Please fill in all required fields");
    }
  });

  // Remove Opening Hour
  $(document).on("click", ".remove_hour", function (e) {
    e.preventDefault();
    let url = $(this).attr("data-url");

    $.ajax({
      type: "DELETE",
      url: url,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      },
      success: function (response) {
        if (response.status === "success") {
          $("#hour-" + response.id).remove();
        }
      },
    });
  });

  // Functions
  function updateCartDisplay(response, food_id) {
    $("#cart_counter").html(response.cart_counter["cart_count"]);
    $("#qty-" + food_id).html(response.qty);
    applyCartAmount(
      response.cart_amount["subtotal"],
      response.cart_amount["total"],
      response.cart_amount["grand_total"]
    );
  }

  function removeCartItem(cartItemQty, cart_id) {
    if (cartItemQty <= 0) {
      $("#cart-item-" + cart_id).remove();
    }
  }

  function checkEmptyCart() {
    let cart_counter = $("#cart_counter").html();
    if (cart_counter == 0) {
      $("#empty_cart").show();
    }
  }

  function applyCartAmount(subtotal, total, grand_total) {
    if (window.location.pathname === "/cart/") {
      $("#subtotal").html(subtotal);
      $("#total").html(total);
      $("#grand_total").html(grand_total);
    }
  }

  function createHourRow(response) {
    if (response.is_closed === "Closed") {
      return `
        <tr id="hour-${response.id}">
          <td><b>${response.day}</b></td>
          <td>Closed</td>
          <td><a href="#" class="remove_hour" data-url="/accounts/vendor/opening_hours/remove/${response.id}/">Remove</a></td>
        </tr>`;
    } else {
      return `
        <tr id="hour-${response.id}">
          <td><b>${response.day}</b></td>
          <td>${response.from_hour} - ${response.to_hour}</td>
          <td><a href="#" class="remove_hour" data-url="/accounts/vendor/opening_hours/remove/${response.id}/">Remove</a></td>
        </tr>`;
    }
  }
});

// Function to get CSRF token from cookies


$(document).ready(function () {
  // Other event handlers...

  // Delete Cart Item
  $(document).on("click", ".delete_cart", function (e) {
    e.preventDefault();
    let url = $(this).data("url");

    $.ajax({
      type: "DELETE",
      url: url,
      headers: {
        'X-CSRFToken': getCookie('csrftoken') // Ensure the CSRF token is included
      },
      success: function (response) {
        if (response.status === "success") {
          swal(response.message, "", "success");
          $("#category-" + response.id).remove(); // Remove the category from the list
          checkEmptyCart(); // Optional: Update UI if needed
        } else {
          swal(response.message, "", "error");
        }
      },
      error: function (xhr) {
        swal("An error occurred. Please try again.", "", "error");
      }
    });
  });

  // Function to get CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

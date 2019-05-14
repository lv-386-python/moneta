function eye() {
    let x = document.getElementById("id_password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
let CHOSED_ICON;


function buildForm(data){
    // build html form as string
    // Args:
    //  data(json): data about new form
    // Returns:
    //  formHTML (string) : html of form.

    let formHTML =
    `
    <form id="base_form">
    <h2>${data.name}</h2>
    <div class="form-group">
        <label>Name</label>
        <input type="text" class="form-control" id="name_field" aria-describedby="name" placeholder="Enter Name">
    </div>
    <div class="form-group">
        <label f>Currency</label>
        <select id="currency_field" class="form-control">`;

    for(let currency of data.currencies){
        formHTML += `<option value="${currency.id}">${currency.currency}</option>`
    }

    formHTML +=  `
    </select>
    </div>
    <div class="form-group">
        <label>Amount</label>
        <input type="number" class="form-control" id="amount_field" aria-describedby="amount" placeholder="Enter Amount">
    </div>
    <label>Chose image</label>
    <div class="icon-flex border rounded icon_form_choisefield">`

    for (let icon of data.icons){
        formHTML += `<div class="icon_option ${icon.css} icon_format" value="${icon.id}" id="icon_${icon.id}"/>`;
    }

    formHTML += `</div>
    <button type="submit" class="btn btn-primary btn-block">Submit</button>
    </form>`;

    return formHTML
}

$(document).on('click', '.icon_option', function (e) {
    $(CHOSED_ICON).toggleClass('icon_selected');
    $(e.target).toggleClass('icon_selected');
    CHOSED_ICON = e.target;
    console.log(CHOSED_ICON);
})


function autoFillForm(data){
    let form = $('#base_form');
    $('#name_field').val(data.name);
    $('#currency_field').val(data.currency);
    $('#amount_field').val(data.amount);
    CHOSED_ICON = document.getElementById(`icon_${data.icon}`)
    $(CHOSED_ICON).toggleClass('icon_selected');
}



// When the user clicks the button, open the modal
$(document).on('click', '#addExpend', function (e) {
    $.get("expend/create", function (data) {
        data.icons = [
            {"id": 1, "css": "coins"},
            {"id": 2, "css": "coin-9"},
            {"id": 3, "css": "credit-card-6"},
            {"id": 4, "css": "notes"},
            {"id": 5, "css": "notes-2"},
            {"id": 6, "css": "piggy-bank-1"}, {"id": 7, "css": "safebox-4"},
            {"id": 8, "css": "wallet-1"}, {"id": 9, "css": "basket"},
            {"id": 10, "css": "box-3"}, {"id": 11, "css": "cart-3"},
            {"id": 12, "css": "credit-card-3"}, {"id": 13, "css": "get-money"},
            {"id": 14, "css": "safebox-3"}, {"id": 15, "css": "stamp-1"},
            {"id": 16, "css": "stand"}, {"id": 17, "css": "store-3"},
            {"id": 18, "css": "bank"}, {"id": 19, "css": "briefcase"},
            {"id": 20, "css": "coin"}, {"id": 21, "css": "credit-card"},
            {"id": 22, "css": "credit-cards"}, {"id": 23, "css": "dollar"},
            {"id": 24, "css": "money-bag"}, {"id": 25, "css": "piggy-bank"},
            {"id": 26, "css": "profits"},
            {"id": 27, "css": "wallet"}
        ];

        data.currencies = [
            {"id": 1, "currency": "UAH"},
            {"id": 2, "currency": "GBP"},
            {"id": 3, "currency": "USD"},
            {"id": 4, "currency": "EUR"}
        ];
})
});

$(document).on('click', '#addIncome', function (e) {
    $.get("income/add/", function (data) {
        $("#modalF").html(data);
        $('#incomeForm').css("display", "flex");

    });

        data.name = 'Create Expend'
        // console.log(data)
        newForm = buildForm(data);

        $(".modal-content").html(newForm);

        CHOSED_ICON = document.getElementById('icon_1');
        $(CHOSED_ICON).toggleClass('icon_selected');
        // CHOSED_ICON = document.getElementById('icon_1');
        $('.bg-modal').css("display", "flex");

});






$(document).on('click', '#createIncomeButtom', function (e) {

    $.post("api/v1/income/", $("#createIncomeForm").serialize())
    $.post("income/add/", $("#createIncomeForm").serialize())
        .done(function (respons) {
            document.location = "/";
        })
        .fail(function (error) {
            console.error(error);
            alert('form is not valid')
        })
});

$(document).on('click', '#incomeForm', function (event) {
    if (event.target.id === "incomeForm") {
        $("#incomeForm").css("display", "none");
        $("#incomeForm").children().empty();
    }
});

// When the user clicks the button, open the Current modal
$(document).on('click', '#addCurrent', function (e) {
    $.get("current/create/", function (data) {
        $(".modal-content").html(data);
        $('.bg-modal').css("display", "flex");

    });
})

$(document).on('click', '#createCurrentButton', function (e) {

    let inputs = {};
      $("#createCurrentForm").serializeArray().forEach(function (element) {
        inputs[element.name] = element.value;
      });

    $.ajax({
        type:'POST',
        url: 'http://127.0.0.1:8000/' + 'current/create/',
        data : inputs,
        success: function(respons){
            console.log(respons);
            alert('Current was successfully created');
            document.location = "/";
            setTimeout(function () { window.close();}, 3000);
        },
        error : function (error) {
            console.error(error);
            alert('Something wrong, try one more time');
        },
    });
});


$(document).on('click', '#createCurrentForm', function (event) {
    if (event.target.id === "createCurrentForm") {
        $("#createCurrentForm").css("display", "none");
        $("#createCurrentForm").children().empty();
    }
});

///When the user press button "user profile" open user profile page
$(document).on('click', '#userSettings', function (e) {
    console.log('asa');
    $.get("user_settings/", function (data) {
        $(".modal-content").html(data);
        $('.bg-modal').css("display", "flex");

    });
})

///Close user profile when user click somewhere except form
$(document).on('click', '#userSettingsForm', function (event) {
    if (event.target.id === "userSettingsForm") {
        $(".bg-modal").css("display", "none");
        $(".modal-content").children().empty();
    }
});

$(document).on('click', '#goBack',  function (event) {
    $.get("user_settings/", function (data) {
        $(".modal-content").html(data);
    });
});

$(document).on('click', '#goBack1',  function (event) {
    $.get("user_settings/", function (data) {
        $(".bg-modal").css("display", "none");
    });
});

$(document).on('click', '#goBack2',  function (event) {
    $.get("user_settings/", function (data) {
        $(".modal-content").html(data);
    });
});

$(document).on('click', '#goBack3',  function (event) {
    $.get("user_settings/", function (data) {
        $(".modal-content").html(data);
    });
});

$(document).on('click', '#goBack4',  function (event) {
    $.get("/", function (data) {
        $(".bg-modal").css("display", "none");
    });
});

// Close popup if user press ESC button
$(document).keydown(function(e){
    if ( e.keyCode === 27 ) {
        $('.bg-modal').css("display","none");

    }
    });




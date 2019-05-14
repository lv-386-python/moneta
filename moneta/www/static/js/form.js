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
        <input required type="text" class="form-control" id="name_field"
        aria-describedby="name" placeholder="Enter Name" max_lenght="45">
    </div>
    <div class="form-group">
        <label>Currency</label>
        <select id="currency_field" class="form-control">`;

    for(let currency of data.currencies){
        formHTML += `<option value="${currency.id}">${currency.currency}</option>`
    }

    formHTML +=  `
    </select>
    </div>
    <div class="form-group">
        <label>Amount</label>
        <input required type="number" class="form-control" id="amount_field"
        aria-describedby="amount" placeholder="Enter Amount" min="0" max="1e+12">
    </div>
    <label>Choose image</label>       
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
})


function autoFillForm(data){
    $('#name_field').val(data.name);
    $('#currency_field').val(data.currency.id);
    $('#amount_field').val(data.amount);
    CHOSED_ICON = document.getElementById(`icon_${data.image.id}`)
    $(CHOSED_ICON).toggleClass('icon_selected');
}


function getInfoAndBuildForm(name,info){
    let infoForForm = {}
    infoForForm.name = name
    $.get("/api/v1/images/", function (data) {
        infoForForm.icons = data;
        $.get("/api/v1/currencies", function (data) {
            infoForForm.currencies = data;
            newForm = buildForm(infoForForm);
            $(".modal-content").html(newForm);
            if(info){
                autoFillForm(info);
            }
            else {
                CHOSED_ICON = document.getElementById('icon_1');
                $(CHOSED_ICON).toggleClass('icon_selected');
            }
            $('.bg-modal').css("display", "flex");
     });
    });
    return infoForForm;
}

// When the user clicks the button, open the modal
$(document).on('click', '#addExpend', function (e) {
    getInfoAndBuildForm('Create Expend');
    console.log('hs')

});

$(document).on('click','#editExpend', function (e){
    let shotaid = window.location.href.split('/')[4];
    $.get(`/api/v1/expend/${shotaid}/edit/`,function(data){
         getInfoAndBuildForm('Edit Expend',data);
        autoFillForm(data);
    });
    $('.bg-modal').css("display", "flex");
})


$(document).on('click', '#createIncomeButtom', function (e) {
    $.post("api/v1/income/", $("#createIncomeForm").serialize())
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
$(document).on('click', '#addCurrent', function (e)
{
    $.get("current/create/", function (data)
    {
        $("#modalC").html(data);
        $('#currentForm').css("display", "flex");
    });
})

$(document).on('click', '#createCurrentButton', function (e) {
    $.post("api/v1/current/", $("#createCurrentForm").serialize())
        .done(function (respons) {
            document.location = "/";
        })
        .fail(function (error) {
            console.error(error);
            alert('Form is not valid!')

        })
});

$(document).on('click', '#currentForm', function (event) {
    if (event.target.id === "currentForm") {
        $("#currentForm").css("display", "none");
        $("#currentForm").children().empty();
    }
});

///When the user press button "user profile" open user profile page
$(document).on('click', '#userSettings', function (e) {
    $.get("user_settings/", function (data) {
        $("#modalU").html(data);
        $('#userSettingsForm').css("display", "flex");

    });
});



// ///Close user profile when user click somewhere except form
// $(document).on('click', '.bg-modal', function (event) {
//     if (event.target.id != "base_form") {
//         $(".bg-modal").css("display", "none");
//         $(".bg-modal").children().empty();
//     }
// });

// Close popup if user press ESC button
$(document).keydown(function(e){
    if ( e.keyCode === 27 ) {
        $('.bg-modal').css("display","none");

    }
});
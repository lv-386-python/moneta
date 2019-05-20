let CHOSED_ICON;


function buildForm(data){
    // build html form as string
    // Args:
    //  data(json): data about new form
    // Returns:
    //  formHTML (string) : html of form.

    let formHTML = 
    `
    <form id="base_form" method="${data.method}" action="${data.api_url}">
    <div class="btn-group-lg d-flex justify-content-between">
        <h2>${data.name}</h2>    
        <button type="cancel" id="cancel_form" class="btn btn-outline-danger"> <i class="fas fa-times"></i> </button>
    </div>
    <div class="form-group">
        <label>Name</label>
        <input required type="text" class="form-control" id="name_field"
        aria-describedby="name" placeholder="Enter Name" maxlength="45">
    </div>
    `
    if(data.method == 'POST'){
        formHTML += ` 
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
            aria-describedby="amount" placeholder="Enter Amount" min="0" max="1e+11">
        </div>`;
    }

    formHTML += `
    <label>Choose image</label>
    <div class="icon-flex border rounded icon_form_choisefield">`   
    
    for (let icon of data.icons){
        formHTML += `<div class="icon_option ${icon.css} icon_format" title="${icon.css}" value="${icon.id}" id="icon_${icon.id}"/>`;
    }    
    
    formHTML += `</div>
    <div class="btn-group-lg d-flex justify-content-end">
        <button type="submit" class="btn login-submit">Submit</button>
    </div>
    </form>`;

    return formHTML
}


$(document).on('submit','#base_form', function(e) {
    e.preventDefault();
    
    method = $('#base_form').attr('method');
    api_url = $('#base_form').attr('action');

    let info = {
        name : $('#name_field').val(),
        image : CHOSED_ICON.getAttribute('value')    
    };

    if (method =='POST'){ 
        info.currency = document.getElementById('currency_field').value;
        info.amount = document.getElementById('amount_field').value
    }

    $.ajax({
        type: method,
        url : api_url,
        data : info,
        success: function(respons){
            $('.modal-content').html(
                `
                <div class="text-center">Success</div>
                `
            );
            setTimeout( function() {
                window.location.href = "/"
            }, 970);
        },
        error : function (error) {
            $('.modal-content').html(
                `
                <div class="text-center"> Sorry, something went wrong </div>
                `
            );

            setTimeout( function() {
                window.location.href = "/"
            }, 2000);
        },
    });    
});

$(document).on('click', '#cancel_form', function(e){
    $(".bg-modal").children().empty();
    $('.bg-modal').css("display","none");
});

$(document).on('click', '#cancel_one_level_up_form',  function (event) {
    $.get(window.location.href.split('/').slice(0, 3).join('/') + '/user_settings/', function (data) {
        $(".modal-content").html(data);
    });
});

$(document).on('click', '.icon_option', function (e) {
    $(CHOSED_ICON).toggleClass('icon_selected');
    $(e.target).toggleClass('icon_selected');
    CHOSED_ICON = e.target;
});

function autoFillForm(actualState){
    $('#name_field').val(actualState.name);
    CHOSED_ICON = document.getElementById(`icon_${actualState.image.id}`);
    $(CHOSED_ICON).toggleClass('icon_selected');
}

function getInfoAndBuildForm(name,info){
    let infoForForm = {};
    infoForForm.name = name;
    $.get("/api/v1/images/", function (data) {
        infoForForm.icons = data;
        $.get("/api/v1/currencies", function (data) {
            infoForForm.currencies = data;
            infoForForm.method = info.method;
            infoForForm.api_url = info.api_url;
            newForm = buildForm(infoForForm);
            $(".modal-content").html(newForm);
            if(info.actualState){
                autoFillForm(info.actualState);
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

$(document).keydown(function (e) {
    if (e. keyCode == 13) {
        e. preventDefault();
        return false;
    }
});

// When the user clicks the button, open the modal

// Expends
$(document).on('click', '#addExpend', function (e) {
    let info = {
        'method':'POST',
        'api_url':'/api/v1/expend/create'
    };
    getInfoAndBuildForm('Create Expend',info);
});


$(document).on('click','#editExpend', function (e){
    let expend_id = window.location.href.split('/')[4];
    let info = {
        'method':'PUT',
        'api_url':`/api/v1/expend/${expend_id}/edit/`
    };
    $.get(`/api/v1/expend/${expend_id}/edit/`,function(data){
        info.actualState = data;
        getInfoAndBuildForm('Edit Expend', info);
    });
});


// Incomes

$(document).on('click', '#addIncome', function (e) {
    let info = {
        'method':'POST',
        'api_url':'api/v1/income/create/'
    };
    getInfoAndBuildForm('Create Income',info);
});

$(document).on('click','#editIncome', function (e){
    let income_id = window.location.href.split('/')[4];
    let info = {
        'method':'PUT',
        'api_url':`/api/v1/income/${income_id}/`
    };

    $.get(`/api/v1/income/${income_id}/`,function(data){
        info.actualState = data;
        getInfoAndBuildForm('Edit Income',info);
    });
});

// CURRENT
$(document).on('click', '#addCurrent', function (e) {
    let info = {
        'method':'POST',
        'api_url':'/api/v1/current/create'
    };
    getInfoAndBuildForm('Create Current',info);
});

$(document).on('click','#editCurrent', function (e){
    let current_id = window.location.href.split('/')[4];
    let info = {
        'method':'PUT',
        'api_url':`/api/v1/current/${current_id}/edit/`
    };

    $.get(`/api/v1/current/${current_id}/edit/`,function(data){
        info.actualState = data;
        getInfoAndBuildForm('Edit Current',info);
    });
});

///When the user press button "user profile" open user profile page
$(document).on('click', '#userSettings', function (e) {
    $.get('user_settings/', function (data) {
        $('.modal-content').html(data);
        $('.bg-modal').css("display", 'flex');

    });
});

// Close popup if user press ESC button
$(document).keydown(function(e){
    if ( e.keyCode === 27 ) {
        $('.bg-modal').css("display","none");
        $(".bg-modal").children().empty();
    }
});

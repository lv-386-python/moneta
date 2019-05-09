
function buildForm(data){
    // build html form as string
    // Args:
    //  data(json): data about new form
    // Returns:
    //  formHTML (string) : html of form.

    let formHTML = `<div><form class="basic_form" id="${data.form_id}"> `;
    formHTML += `<h1>${data.form_name}</h1>`;
    for(const inputField of data.fields){
        let newInput = '<div class="form-group">';
        newInput += `<label>${inputField.label}</label>`;
        newInput += `<input class="form-control" type="${inputField.type}" value="${inputField.value}">`;
        newInput += '</div>';
        formHTML += newInput;
    }
    formHTML += '<button type="submit" class="btn btn-primary">Submit</button>';
    formHTML += ' </form></div>';
    return formHTML
}


// When the user clicks the button, open the modal
$(document).on('click', '#addExpend', function (e) {
    // data = {
    //     'form_id':'test_form_id',
    //     'form_name':'Test form',
    //     'fields':[
    //         {'label':'test_label 1', 'type':'text','value':'lorem'},
    //         {'label':'test_label 2', 'type':'text','value':'ipsum'},
    //         {'label':'test_label 3', 'type':'text','value':'dolor'},
    //         {'label':'test_label 4', 'type':'text','value':'sit'},
    //         {'label':'test_label 5', 'type':'text','value':'amen'},
    //     ]
    // }
    $.get("expend/create", function (data) {       
        console.log(data);
        newForm = buildForm(data);
        $("#modalF").html(newForm);
        $('#incomeForm').css("display", "flex");
    });

})





// When the user clicks the button, open the modal
$(document).on('click', '#addIncome', function (e) {
    $.get("income/add/", function (data) {
        $("#modalF").html(data);
        $('#incomeForm').css("display", "flex");

    });

})


// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == 'bg-modal') {
        modal.style.display = "none";
    }
}


$(document).on('click', '#createIncomeButtom', function (e) {

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
})

///Close user profile when user click somewhere except form
$(document).on('click', '#userSettingsForm', function (event) {
    if (event.target.id === "userSettingsForm") {
        $("#userSettingsForm").css("display", "none");
        $("#userSettingsForm").children().empty();
    }
});

// Close popup if user press ESC button
$(document).keydown(function(e){
    if ( e.keyCode === 27 ) {
        $(incomeForm).css("display","none");
        $(currentForm).css("display","none");
        $(expendForm).css("display","none");
    }
});

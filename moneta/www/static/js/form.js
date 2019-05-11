// Get the modal

// When the user clicks the button, open the modal
$(document).on('click', '#addIncome', function (e) {
    $.get("income/add/", function (data) {
        $(".modal-content").html(data);
        $('.bg-modal').css("display", "flex");

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
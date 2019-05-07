// Get the modal

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


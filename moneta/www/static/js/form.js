// Get the modal
let modal = document.getElementsByClassName('bg-modal');

// Get the button that opens the modal
let btn = document.getElementsByClassName("add");
// When the user clicks the button, open the modal
btn.onclick = function () {
    modal.style.display = "flex";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == 'bg-modal') {
        modal.style.display = "none";
    }
}

$(document).on('submit', '#income', function (e) {
    e.preventDefault();
    const form = document.getElementById("income");
    const image_id = form["image"].value;
    const currency = form["currency"].value;
    const name = form['name'].value;
    const amount = form['amount'].value;
    const csrfmiddlewaretoken = form['csrfmiddlewaretoken'].value;

    $.ajax({
        type: 'POST',
        url: '/',
        data: {
            name: name,
            amount: amount,
            image: image_id,
            currency: currency,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        success: function (response) {
            $('.modal-content').html(
                `
                <h3>Created successfully</h3>             
                <a href="/"> <h4>go back </h4> </a>
                `);

        },
        error: function (error) {
            console.error(error);
            alert('form is not valid')
        },
    });
});

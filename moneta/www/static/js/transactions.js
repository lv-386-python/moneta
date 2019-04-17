const fills = document.querySelectorAll('.fill')


//Fill  Listeners
for (const fill of fills){
 fill.addEventListener('dragstart',dragStart);
 fill.addEventListener('dragend',dragEnd);
 fill.addEventListener('dragover',dragOver);
 fill.addEventListener('dragenter',dragEnter);
 fill.addEventListener('dragleave',dragLeave);
 fill.addEventListener('drop',dragDrop);
}


// drag Functions

let FROM;
let TRANSACTION;

function dragStart(e) {
    e.dataTransfer.setData('text/plain', 'anything');
    FROM  = this.value;
    console.log('start');
    this.className += ' hold';

    setTimeout(() => (this.className = 'invisible'), 0)
}

function dragEnd(){
  console.log('end');
  this.className = ' buttonn';
  this.className += ' fill';
}

function dragOver(e){
  e.preventDefault();
  console.log('over');
};

function dragEnter(e){
  e.preventDefault();
  console.log('enter');
  this.className += " hovered";
};

function dragLeave(){

  console.log('leave');
  this.className = ' buttonn';
  this.className += ' fill';
};

function dragDrop(e){
  if(e.preventDefault) { e.preventDefault(); }
  if(e.stopPropagation) { e.stopPropagation(); }
  console.log('drop');
  this.className = ' buttonn';
  this.className += ' fill';
  let TO = this.value;
  TRANSACTION = {
      from:FROM,
      to: TO
  };
  setTimeout(()=>{
    const modalForm = document.querySelector('.bg-modal');
    modalForm.style.display = 'flex';
  },133);
  return false;
};

$(document).on('submit','#transaction-form', function (e) {
    e.preventDefault();
    TRANSACTION.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    let amount = document.getElementById('amount_of_transaction').value;
    TRANSACTION.amount = Number(amount);
    // console.log(TRANSACTION)
    $.ajax({
        type:'POST',
        url : window.location.href,
        data : TRANSACTION,
        success: function(response){
            $('.modal-content').html(
                `
                <h2>Your transaction was submitted</h2>             
                <a href="/"> <strong>go back </strong> </a>
                `);
        },
        error : function (error) {
            console.error(error)
        },
    });
});

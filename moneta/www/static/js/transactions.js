const drag_items = document.querySelectorAll('.drag_item')


//Fill  Listeners
for (const drag_item of drag_items){
 drag_item.addEventListener('dragstart',dragStart);
 drag_item.addEventListener('dragend',dragEnd);
 drag_item.addEventListener('dragover',dragOver);
 drag_item.addEventListener('dragenter',dragEnter);
 drag_item.addEventListener('dragleave',dragLeave);
 drag_item.addEventListener('drop',dragDrop);
}

// variables for storing transaction data
let FROM, TO;
let HOWERED = {};
let TRANSACTION;


// drag Functions

function dragStart(e) {
    e.dataTransfer.setData('text/plain', 'anything');
    FROM  = this;
    FROM.className = 'test';
    console.log(FROM);
    // console.log('start');

    // setTimeout(() => (this.className = 'invisible'), 0)
}

function dragEnd(){
  // console.log('end');
}

function dragOver(e){
  e.preventDefault();
  console.log('over');
}

function dragEnter(e){
  e.preventDefault();
  HOWERED.prevClass = this.getAttribute('class');
  this.className += ' hovered';
  console.log('enter');
}

function dragLeave(){
  this.className = HOWERED.prevClass;
  console.log('leave');
}

function dragDrop(e){
  if(e.preventDefault) { e.preventDefault(); }
  if(e.stopPropagation) { e.stopPropagation(); }
  // console.log('drop');

  console.log(this.getAttribute('class'));
  TO = this;
  console.log(TO);
  TRANSACTION = {
      from:FROM,
      to: TO
  };
  setTimeout(()=>{
    const modalForm = document.querySelector('.bg-modal');
    modalForm.style.display = 'flex';
  },133);
  return false;
}

function cancelForm(){
    const modalForm = document.querySelector('.bg-modal');
    modalForm.style.display = 'none';
}

$(document).on('submit','#transaction-form', function (e) {
    e.preventDefault();
    TRANSACTION.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    let amount_from = document.getElementById('amount_from').value;
    let amount_to = document.getElementById('amount_to').value;
    TRANSACTION.amount_from = Number(amount_from);
    TRANSACTION.amount_to = Number(amount_to);

    $.ajax({
        type:'POST',
        url :'transaction/',
        data : TRANSACTION,
        success: function(response){
            $('.modal-content').html(
                `
                <h2>Your transaction was submitted</h2>             
                <a href="/"> <h3>go back </h3> </a>
                `);
        },
        error : function (error) {
            console.error(error)
        },
    });
});

String.prototype.replaceAll = function(search, replacement) {
  var target = this;
  return target.replace(new RegExp(search, 'g'), replacement);
};


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
let HOWERED;
let TRANSACTION = {};

// drag Functions
function dragStart(e) {
    e.dataTransfer.setData('text/plain', 'anything');
    FROM  = this;
    FROM.data = `{ "id" : ${FROM.getAttribute('value')}, "type": "${FROM.getAttribute('name')}" } `;
    FROM.prevClass = this.className;
    this.className += ' hold'

}


function dragEnd(){
  FROM.className = FROM.prevClass;

}


function dragOver(e){
  e.preventDefault();

}


function dragEnter(e){
  e.preventDefault();
  HOWERED = this.className;
  this.className += ' hovered';

}


function dragLeave(){
  this.className = HOWERED;

}


function dragDrop(e){
  if(e.preventDefault) { e.preventDefault(); }
  if(e.stopPropagation) { e.stopPropagation(); }
  this.className = HOWERED;
  TO = this;


  TO.data = `{ "id": ${TO.getAttribute('value')}, "type": "${TO.getAttribute('name')}"} `;
  if (FROM  == TO) { return false};
  if (FROM.getAttribute('name')=='expend') {return false};
  if (TO.getAttribute('name')=='income'){return false};
  if (TO.getAttribute('name')=='income'){return false};

  // TRANSACTION = {
  //     from:FROM.data,
  //     to:TO.data
  // };

  
  
  let availableSources = [], availableTargets = [];

  $.get('api/v1/income/', function(incomes){
    let incomeArray = incomes; 

    $.get('api/v1/current/', function(currents){
      let availableSources = incomeArray.concat(currents);
      let currentsArray = currents;
  
      $.get('api/v1/expend/', function(expends){
        let availableTargets = currentsArray.concat(expends);
        
        $('.modal-content').html(buildTransactionForm(availableSources,availableTargets));

        let from_id = FROM.getAttribute('value');
        let to_id = TO.getAttribute('value');
        
        $("#from_field").val(from_id);
        $("#to_field").val(to_id);

        $('.bg-modal').css("display", "flex");
      })
    })
  })

  return false;
}




function buildTransactionForm(availableSources,availableTargets){
  let formHTML = ` 
  <form id="transaction-form">
  <div class="btn-group-lg d-flex justify-content-between">
      <h2>New Transaction</h2>    
      <button type="cancel" id="cancel_form" class="btn btn-outline-danger"> <i class="fas fa-times"></i> </button>
  </div> `
  
  //Select root of transaction
  formHTML += '<div class="form-group"><label>From</label> <select id="from_field" class="form-control">';
  for(let from of availableSources){
    formHTML += `<option value="${from.id}">${from.name}</option>`;
  }
  formHTML += '</select></div>';
  
  //Select target of transaction
  formHTML += '<div class="form-group"><label>To</label> <select id="to_field" class="form-control">';
  for(let to of availableTargets){
    formHTML += `<option value="${to.id}">${to.name}</option>`;
  }
  formHTML += '</select></div>';

  formHTML += `
  <div class="form-group">
      <label>How much are you taking from</label>
      <input required type="number" class="form-control" id="from_amount_field"
      aria-describedby="To" placeholder="amount from" >
  </div>
  <div class="form-group">
      <label>How much are you putting in</label>
      <input required type="number" class="form-control" id="to_amount_field"
      aria-describedby="To" placeholder="amount to">
  </div>
  <div class="btn-group-lg d-flex justify-content-end">
      <button type="submit" class="btn login-submit">Submit</button>
  </div>
  </form>`;

  return formHTML;
}

function cancelForm(){
    const modalForm = document.querySelector('.bg-modal');
    modalForm.style.display = 'none';
}

$(document).on('submit','#transaction-form', function (e) {
    e.preventDefault();
    let amount_from = document.getElementById('from_amount_field').value;
    let amount_to = document.getElementById('to_amount_field').value;
    TRANSACTION.amount_from = Number(amount_from);
    TRANSACTION.amount_to = Number(amount_to);

    TRANSACTION['type_from'] = FROM.getAttribute('name');
    TRANSACTION['type_to'] = TO.getAttribute('name');
    
    TRANSACTION['id_from'] = $('#from_field').val();
    TRANSACTION['id_to'] = $('#to_field').val();

    console.log(TRANSACTION);
    $.ajax({
        type:'POST',
        url :'transaction/',
        data : TRANSACTION,
        success: function(response){
            $('.modal-content').html(
                `
                <h2>Your transaction was submitted</h2>             
                `);
        },
        error : function (error) {
            console.error(error)
        },
    });
});

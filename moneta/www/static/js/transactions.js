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
let TRANSACTION;


// drag Functions

function dragStart(e) {
    e.dataTransfer.setData('text/plain', 'anything');
    FROM  = this;
    FROM.data = FROM.getAttribute('value');
    FROM.data =  `${FROM.data.slice(0,-1)}, "type": "${FROM.getAttribute('name')}" } `;
    FROM.prevClass = this.className;
    this.className += ' hold'
    // console.log('start');

}

function dragEnd(){
  FROM.className = FROM.prevClass;
  // console.log('end');
}

function dragOver(e){
  e.preventDefault();
//  console.log('over');
}

function dragEnter(e){
  e.preventDefault();
  // let saveClass = () => {
  //   HOWERED.initClass = this.className;
  // };
  // let promiseSvaClass = saveClass();
  // let makeHowered = promiseSvaClass.then(this.className += ' hovered');
  // makeHowered();
  // console.log(this.className);
  HOWERED = this.className;
//  console.log(HOWERED);
  this.className += ' hovered';


//  console.log('enter');
}

function dragLeave(){
  this.className = HOWERED;
  // console.log('leave');
}

function dragDrop(e){
  if(e.preventDefault) { e.preventDefault(); }
  if(e.stopPropagation) { e.stopPropagation(); }
  // console.log('drop');
  this.className = HOWERED;
  TO = this;
  TO.data = TO.getAttribute('value');

  TO.data = `${TO.data.slice(0,-1)}, "type": "${TO.getAttribute('name')}"} `;
  if (FROM  == TO) { return false};
  if (FROM.getAttribute('name')=='expend') {return false};
  if (TO.getAttribute('name')=='income'){return false};
  TRANSACTION = {
      from:FROM.data,
      to:TO.data
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
                
                <a href="/"> go back  </a>
                `);
        },
        error : function (error) {
            console.error(error)
        },
    });
});

function deleteTransaction(id, type){
  console.log(id, type);
  console.log(window.location.origin);
  let inputs= {};
  inputs['type'] = type;
  inputs['id'] = id;
  console.log('inputs', inputs);
    $.ajax({
        type: 'POST',
        url : window.location.origin + '/api/v1/transaction/cancel/',
        data : inputs,
        success: function(response){
          console.log(response);
          location.href =window.location.href;
        },
        error : function (error) {           
            console.error(error);
        },
    }); 
};

function addTransactions(json){   
 console.log("is", json);  
 var htmlTransactions = "";
  var json_keys = Object.keys(json);
  if (json_keys.length < 1){ 
    htmlTransactions += `You don't have any transactions. Please, make first one. ` }
    else { 
  for (i = json_keys.length-1;i>=0;i--)
    {      
      var transactionDate = new Date(json[i].create_time * 1000);
      let dateFormatted = transactionDate.getDate() + "." + (transactionDate.getMonth() + 1) + "." + transactionDate.getFullYear()
  dateStr = dateFormatted.toLocaleString();
    htmlTransactions += ` 
    ${json[i].name_from}  &#8594; ${json[i].name_to} <span class="text-secondary">  ${json[i].amount_change} </span> ${dateStr}`;
    if (i==json_keys.length-1){
   htmlTransactions += `<button style="width: 5%; background-color:#F7F7F7; color:#dc3545; display:inline-block;margin-bottom: 6px;margin-left: 5px;" type="cancel" onclick="deleteTransaction(${json[i].id}, '${json[i].type}')" class="btn btn-outline-danger"> 
    <i class="fas fa-times"></i> </button>`}
   htmlTransactions += ` <hr> `;
    }}
 return htmlTransactions;
}

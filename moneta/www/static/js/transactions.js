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



function makeTable(htmlStr){
   $("#transactionTable").html(htmlStr);
    $("#transactionTable").DataTable({
    "bInfo": false, 
    dom: 'Bfrtip',
       buttons: [
            {
                 text: 'New',   
                 attr:  {                
                id: 'createNewTransaction'
                        }                 
            },
            {text: 'Delete last',
            attr:  {                
                id: 'deleteLastTransaction'
            }
          }]
    });
}

function makeNotOwnerTable(htmlStr){
   $("#transactionTable").html(htmlStr);
    $("#transactionTable").DataTable({
    "bInfo": false, 
    "language": {
                  "emptyTable": "Sorry, you haven't any transaction. Please, make first one. "},  
    dom: 'Bfrtip',
    buttons: [
            {
              text: 'New',   
              attr:  {id: 'createNewTransaction'}           
            }
          ]
    });
}


function makeEmptyTable(htmlStr){
   $("#transactionTable").html(htmlStr);
    $("#transactionTable").DataTable({
    "bInfo": false, 
    "language": {
                  "emptyTable": "Sorry, you haven't any transaction. Please, make first one. "},
    "bFilter": false ,
    "bPaginate": false,
    dom: 'Bfrtip',
    buttons: [
            {
              text: 'New',   
              attr:  {id: 'createNewTransaction'}           
            }
          ]
    });
}


 $(document).on("click","#deleteLastTransaction",function() {    
    let instance_id = window.location.href.split('/')[4];
    let instance = window.location.href.split('/')[3];
$.when(
    $.getJSON(window.location.origin + `/api/v1/${instance}/${instance_id}/transaction/get`)
).done( function(json) {
  var json_keys = Object.keys(json);
  console.log(json_keys.length-1);
  let inputs= {};
  inputs['type'] = json[json_keys.length-1].type;
  inputs['id'] = json[json_keys.length-1].id;
    $.ajax({
        type: 'POST',
        url : window.location.origin + '/api/v1/transaction/cancel',
        data : inputs,
        success: function(response){
          console.log(response);
          location.href = window.location.href;
        },
        error : function (error) {           
            console.error(error);
        },
    }); 
     });
  });

function emptyJson(){
  var htmlTransactions = `
  <thead>
    <tr>
        <th>From</th>
        <th>To</th>
        <th>Amount</th>
        <th>Currency</th>
        <th>Date</th>                
    </tr>
  </thead>
  `;
return htmlTransactions;
}


function showTransactions(json){    
var htmlTransactions = `
                        <thead>
                            <tr>
                                <th>From</th>
                                <th>To</th>
                                <th>Amount</th>
                                <th>Currency</th>
                                <th>Date</th>                
                            </tr>
                        </thead>
                         <tbody>`;
var json_keys = Object.keys(json);
  for (i = json_keys.length-1;i>=0;i--)
    {      
      var transactionDate = new Date(json[i].create_time * 1000);
      let dateFormatted = transactionDate.getFullYear() + "/" + (transactionDate.getMonth() + 1) + "/" +  transactionDate.getDate() ;
    dateStr = dateFormatted.toLocaleString();//dateFormatted.
    htmlTransactions += `                      
                      <tr>
                        <th>${json[i].name_from}</th> 
                        <th>${json[i].name_to}</th> 
                         <th>${json[i].amount_change}</th> 
                         <th>${json[i].currency_to}</th> 
                         <th>${dateStr}</th> 
                         </tr>
                        `;}
                        htmlTransactions+=`</tbody>`;
 return htmlTransactions;
}

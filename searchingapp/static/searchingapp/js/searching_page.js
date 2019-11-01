$( function() {
    $( "#search-id" ).autocomplete({
      source: "/search/",
      minLength:2,
    });
  });
  var frm = $('#search-form');
  frm.submit(function () {
        var search_input = $("#search-id").val()
        $.ajax({
            type: frm.attr('method'),
            url: '/searchAction/?word='+search_input,
            data: {},
            success: function (data) {
                responceHandler(data,search_input);
            },
            error: function(data) {
                noDataFound();
            }
        });
        return false;
    });

function responceHandler(data,search_input){
  var term = search_input;
  term = term.replace(/(\s+)/,"(<[^>]+>)*$1(<[^>]+>)*");
  var pattern = new RegExp("("+term+")", "gi");
  if(data.found){
    dataFound()
    $('#search_result_ol').empty()
    var dataList = data.result;
    for( var index in dataList){
      var data = dataList[index]
      var li_str = '<li>'+data.replace(pattern, "<strong>$1</strong>")+'</li>';
      $('#search_result_ol').append(li_str)
    }
  }else{
    noDataFound()
  }
}
function dataFound(){
  $('#search_result_ol').show()
  $('#search_result_not_found').hide()
}

function noDataFound(){
  $('#search_result_ol').hide()
  $('#search_result_not_found').show()
}
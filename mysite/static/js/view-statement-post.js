$(document).on('submit','#date-range',function(e){
    e.preventDefault();
    $.ajax({
        type:'POST',
        url:'',
        data:
        {
            start_date:$("#start-date").val(),
            end_date:$("#end-date").val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        }//,
        // success:function(){
        //       alert('Saved');
        //         }
        })
    });

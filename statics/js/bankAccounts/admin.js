$(document).ready(function(){
    //$('select').selectpicker();
    console.log("DOCUMENT READY")
    $('#idAccForm').submit(function(){
        console.log("SUBMIT FORM")
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type:$(this).attr('method'),
            data:$(this).serialize(),
            success:function(response){
                console.log("Success: "+response)
                if(response.errors){
                    console.log("FORMERRORES: "+JSON.stringify(response.errors))
                    document.getElementById('idAccFormErrors').innerHTML = "<font color='red'>"+response.errors.__all__+"</font>";
                }else{
                    console.log("No FORMERRORES")
                    window.location.href = response.redirectUrl;
                }
            },
            error:function(response){
                console.log("ERROR: "+response);
            },
        })
    })
})

//$('select').selectpicker();
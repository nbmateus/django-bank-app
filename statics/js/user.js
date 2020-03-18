$(document).ready(function(){
    
    $('#idTransactionForm').submit(function(){
        event.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            data: $(this).serialize(),
            success: function (response) {
                if(response.errors){
                    if (response.errors.rAccNumber){
                        document.getElementById('idTransactionErrors').innerHTML ="<font color='red'>"+response.errors.rAccNumber+"</font>";
                    }else{
                        document.getElementById('idTransactionErrors').innerHTML ="<font color='red'>"+response.errors.__all__+"</font>";
                    }
                    
                }else{
                    window.location.href = response.redirectUrl;
                    //document.getElementById('idTransactionErrors').innerHTML ="<font color='green'>Transaccion realizada con exito.</font>";
                }
            },
            error: function (response) {
                console.log("Error: " + response)
            }
        });

    })

})
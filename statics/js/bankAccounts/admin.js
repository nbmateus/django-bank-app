$(document).ready(function(){
    //$('select').selectpicker();
    
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
                    //window.location.href = response.redirectUrl;
                    document.getElementById('idTransactionErrors').innerHTML ="<font color='green'>Transaccion realizada con exito.</font>";

                }
            },
            error: function (response) {
                console.log("Error: " + response)
            }
        });

    })
    
    $('#idDepositForm').submit(function(){
        event.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            data: $(this).serialize(),
            success: function (response) {
                console.log("Response: "+JSON.stringify(response))
                if(response.errors && response.errors.amount){
                        document.getElementById('idDepositErrors').innerHTML ="<font color='red'>"+response.errors.amount+"</font>";  
                }else{
                    //window.location.href = response.redirectUrl;
                    document.getElementById('idDepositErrors').innerHTML ="<font color='green'>"+response.message+"</font>";
                }
            },
            error: function (response) {
                console.log("Error: " + response)
            }
        });
    })

    $('#idExtractionForm').submit(function(){
        event.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            data: $(this).serialize(),
            success: function (response) {
                console.log("Response: "+JSON.stringify(response))
                if(response.errors && response.errors.amount){
                        document.getElementById('idExtractionErrors').innerHTML ="<font color='red'>"+response.errors.amount+"</font>";  
                }else{
                    //window.location.href = response.redirectUrl;
                    document.getElementById('idExtractionErrors').innerHTML ="<font color='green'>"+response.message+"</font>";
                }
            },
            error: function (response) {
                console.log("Error: " + response)
            }
        });
    })


    //////IMPORT ACCOUNTS LIST HTML
    $.ajax({
        url: "/home/myAccounts/",
        type: 'GET',
        data: $(this).serialize(),
        success: function (response) {
            console.log("RESPONSE: "+response)
            document.getElementById("idMyAccounts").innerHTML = response
        },
        error: function (response) {
            console.log("Error: " + response)
        }
    });

    //////IMPORT ACTIONS LIST HTML
    $.ajax({
        url: "/home/actionslog/",
        type: 'GET',
        data: $(this).serialize(),
        success: function (response) {
            console.log("RESPONSE: "+response)
            document.getElementById("idMovimientos").innerHTML = response
        },
        error: function (response) {
            console.log("Error: " + response)
        }
    });

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
$(document).ready(function(){
    var loginForm = $("#idLoginForm")
    var regForm = $("#idRegForm")
    
    loginForm.submit(function(){
        event.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            data: $(this).serialize(),
            success: function (response) {      
                if(response.errors){
                    document.getElementById('idLogFormErrors').innerHTML ="<font color='red'>"+response.errors.__all__+"</font>";
                }else{
                    window.location.href = response.redirectUrl;
                }
            },
            error: function (response) {
                console.log("Error: " + response)
            }
        });

    })

    regForm.submit(function(){
        event.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            data: $(this).serialize(),
            success: function (response) { 
                if(response.errors){
                    if(response.errors.email){
                        document.getElementById('idRegFormErrors').innerHTML ="<font color='red'>"+response.errors.email+"</font>";
                    }else if(response.errors.password2){
                        document.getElementById('idRegFormErrors').innerHTML ="<font color='red'>"+response.errors.password2+"</font>";
                    }else if(response.errors){
                        document.getElementById('idRegFormErrors').innerHTML ="<font color='red'>Undefined error.</font>";
                    }
                }  
                else{
                    window.location.href = response.redirectUrl;
                }
            },
            error: function (response) {
                console.log("Error: " + response)
            }
        });      
    })

})

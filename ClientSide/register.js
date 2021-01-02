var url = "localhost";
var port = 3000;

$(document).ready(()=>{

    $("#register").click(()=>{
    $("#loginErr").hide();
    var user = $("#username").val()
    var pass = $("#password").val()
    var age = $("#age").val()
    var gender = $('input[name="gender"]:checked').val();

    if (user.length == 0 || pass .length == 0) {
        $("#loginErr").html("Username and password can not be empty! enter data in those fields and try again");
        $("#loginErr").show();
    }
    else if (!(age <= 99 || age >= 0)) {
        $("#loginErr").html("Please enter a valid age between 0-99 and try again!");
        $("#loginErr").show();
    }
    else if (gender == undefined) {
        $("#loginErr").html("Please select your gender and register");
        $("#loginErr").show();
    } else {
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            url: "http://"+url+":"+port+'/users?user=' + user + '&pass=' + pass + '&gender=' + gender + '&age=' + age,
            success: function (data) {
                console.log(data)
                if (data && data.uid){
                    window.location = "./MainMenu.html?uid="+data.uid+"&user="+user
                }
                else{
                    $("#loginErr").html("Problem connecting to the serv, please try again...");
                    $("#loginErr").show();
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $("#loginErr").html("Problem connecting to the server, please try again...");
                $("#loginErr").show();
            }
        });
    }
    });
});


var url = "localhost";
var port = 3000;

$(document).ready(()=>{

    $("#register").click(()=>{
    $("#registerErr").hide();
    var user = $("#username").val()
    var pass = $("#password").val()
    var age = $("#age").val()
    var gender = $('input[name="gender"]:checked').val();

    if (user.length == 0 || pass .length == 0) {
        $("#registerErr").html("Username and password can not be empty! enter data in those fields and try again");
        $("#registerErr").show();
    }
    else if (age == "") {
        $("#registerErr").html("Please enter a valid date!");
        $("#registerErr").show();
    }
    else if (gender == undefined) {
        $("#registerErr").html("Please select your gender and register");
        $("#registerErr").show();
    } else {
        var current_date = new Date()
        var one_hundred_and_twenty_years_ago = new Date();
        one_hundred_and_twenty_years_ago.setFullYear(one_hundred_and_twenty_years_ago.getFullYear() - 120);
        var age_date = new Date(age)
        if (current_date < age_date || one_hundred_and_twenty_years_ago > age_date) {
            $("#registerErr").html("Please enter a valid birth date!");
            $("#registerErr").show();
        } else {
            $.ajax({
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                url: "http://"+url+":"+port+'/users?user=' + user + '&pass=' + pass + '&gender=' + gender + '&age=' + age,
                success: function (data) {
                    data = JSON.parse(data)
                    if ((typeof data[0]) != 'string') {
                        window.location = "./MainMenu.html?uid="+data.uid+"&user="+user
                    }
                    else {
                        $("#registerErr").html(data[0]);
                        $("#registerErr").show();
                    }
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    $("#registerErr").html("Problem connecting to the server, please try again...");
                    $("#registerErr").show();
                }
            });
        }
    }
    });
});


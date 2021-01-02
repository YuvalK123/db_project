var username;
var uid;
var points = 0;
var mistakes = 5;
var wordOrg;
var word;
var url = "localhost";
var port = 3000;
var selectedPosition;
var correctCount=0;
var hiddenLen = 0;
var hints = [];
var hintCount = 0;
var wLen;
var hiddenWord;
var letterOptions = new Array(parseInt(26));;
var isWin = false;

$("#Mis").html(mistakes);

$(document).ready(()=>{

    $("#register").click(()=>{
    $("#loginErr").hide();
    var user = $("#username").val()
    var pass = $("#password").val()
    var age = $("#age").val()
    var gender = $('input[name="gender"]:checked').val();

    console.log(user)
    console.log(pass)
    console.log(age)
    console.log(gender)
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
    }

    var jasonObj = {
        "user": user,
        "pass": pass,
        "age": age,
        "gender": gender
    };

    $.ajax({
        type: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/users',
        data: JSON.stringify(jsonObj)
        success: function (data) {
            data = JSON.parse(data)
            if (data && data.uid){
               window.location = "/MainMenu.html?uid="+data.uid+"&user="+user
            }
            else{
                $("#loginErr").html("Problem connceting to the serv, please try again...");
                $("#loginErr").show();
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#loginErr").html("Problem connceting to the server, please try again...");
            $("#loginErr").show();
        }
    });
});


});


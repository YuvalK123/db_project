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

    $("#login").click(()=>{
    $("#loginErr").hide();
    var user = $("#username").val()
    var pass = $("#password").val()
    $.ajax({ 
        type: 'GET', 
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/users?user='+user+'&pass='+pass, 
        success: function (data) {
            data = JSON.parse(data)
            if (data && data.uid){
                if(data.uid == "-1"){
                    $("#loginErr").html("Username or password is incorrect, please try again...");
                    $("#loginErr").show();
                }
                else{
                    var query= "/MainMenu.html?uid="+data.uid+"&user="+user;
                    if(data.admin == true){
                        query+="&admin=true"
                    }
                    window.location = query
                }
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

$("#register").click(()=>{
        window.location = "./register.html"
});

}); 



var url = "localhost";
var port = 3000;

$(document).ready(()=>{
    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/bestScores/',
        success: function (data) {
//            if (data && data.uid){
//                window.location = "./MainMenu.html?uid="+data.uid+"&user="+user
//            }
//            else{
//                $("#loginErr").html("Problem connecting to the serv, please try again...");
//                $("#loginErr").show();
//            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#loginErr").html("Problem connecting to the server, please try again...");
            $("#loginErr").show();
        }
    });
}


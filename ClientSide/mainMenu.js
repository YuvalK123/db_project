var url = "localhost";
var port = 3000;
$(document).ready(()=>{
    var oldGame;
    var uid = $.urlParam("uid")
     if(uid == null){
         window.location = "./"
     }
    var admin = $.urlParam("admin")
    var user = $.urlParam("user")
    if(admin & admin == "1"){
        $("#admin").show();
    }
    $("#welcome").html("Welcome "+user+"!");

    $.ajax({ 
        type: 'GET', 
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/getgame?uid='+uid, 
        success: function (data) {
            if(data && data != "null"){
                $("#resbtn").show();
                oldGame = data;
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Problem connecting to the server, please try again...");
        }  
    });

    $("#newbtn").click(()=>{
        window.location = "./Game.html?uid="+uid+"&user="+user+"&admin="+admin
    });

    
    $("#resbtn").click(()=>{
        window.location = "./Game.html?uid="+uid+"&user="+user+"&old=1"+"&admin="+admin
    });


    $("#logoutbtn").click(()=>{
        window.location = "./index.html"
    });

    $("#scoresbtn").click(()=>{
        window.location = "./ScoresTable.html?uid="+uid+"&user="+user+"&admin="+admin
    });

    
    $("#editbtn").click(()=>{
        window.location = "./EditProfile.html?uid="+uid+"&user="+user+"&admin="+admin
    });

    $("#locationsbtn").click(()=>{
        window.location = "./Locations.html?uid="+uid+"&user="+user+"&admin="+admin
    });

    $("#adminBtn").click(()=>{
        window.location = "./Admin.html?uid="+uid+"&user="+user+"&admin="+admin
    });


});




$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}

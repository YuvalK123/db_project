var url = "localhost";
var port = 3000;

$(document).ready(()=>{
     var prev_user
     var prev_pass
     var user
     var pass
     var uid = $.urlParam("uid")
     if(uid == null){
         window.location = "./"
     }
    var admin = $.urlParam("admin")
    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/update_user?uid=' + uid,
        success: function (data) {
            if(data.length != undefined) {
                data = JSON.parse(data)
                $('#username').val(data[0])
                prev_user = data[0]
                $('#password').val(data[1])
                prev_pass = data[1]
                $('#age').val(data[2])
                if (data[3] == 'f') {
                    $("#female").prop("checked", true);
                } else {
                    $("#male").prop("checked", true);
                }
            } else {
                $("#updateMsg").html("Problem connecting to the serv, please try again...");
                $("#updateMsg").show();
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#updateMsg").html("Problem connecting to the server, please try again...");
            $("#updateMsg").show();
        }
    });

    $("#save").click(()=>{
    $("#updateMsg").hide();
    user = $("#username").val()
    pass = $("#password").val()

    if (user.length == 0 || pass .length == 0) {
        $("#updateMsg").html("Username and password can not be empty! enter data in those fields and try again");
        $("#updateMsg").show();
    } else if (prev_user != user || prev_pass != pass){
        var my_url
        if (prev_user != user && prev_pass != pass) {
            my_url = "http://"+url+":"+port+'/update_user?uid=' + uid +'&username=' + user + '&pass=' + pass
        } else if (prev_user != user) {
            my_url = "http://"+url+":"+port+'/update_user?uid=' + uid +'&username=' + user
        } else {
            my_url = "http://"+url+":"+port+'/update_user?uid=' + uid +'&pass=' + pass
        }
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            url: my_url,
            success: function (data) {
                console.log(data)
                if (data > 0){
                    prev_user = user
                    prev_pass = pass
                    $("#updateMsg").html("Your changes were successfully saved!");
                }
                else{
                    $("#updateMsg").html("Your changes were not saved, please try again...");
                }
                $("#updateMsg").show();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $("#updateMsg").html("Problem connecting to the server, please try again...");
                $("#updateMsg").show();
            }
        });
    }
    $("#updateMsg").html("You need to make some changes first..");
    $("#updateMsg").show();
    });

    $("#menu").click(()=>{
        if (user == undefined) {
            user = $.urlParam("user")
        }
        window.location = "./MainMenu.html?uid="+uid+"&user="+user+"&admin="+admin
    });
});

$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}
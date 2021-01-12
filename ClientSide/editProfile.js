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
    // gets the data on the user from the database
    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/update_user?uid=' + uid,
        success: function (data) {
            // enters the data into the fields
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
                // shows that was a problem in server
                $("#updateMsg").html("Problem connecting to the serv, please try again...");
                $("#updateMsg").show();
            }
        },
        // something went wrong with the server
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#updateMsg").html("Problem connecting to the server, please try again...");
            $("#updateMsg").show();
        }
    });

    // we save the changes that the user entered to his data
    $("#save").click(()=>{
    $("#updateMsg").hide();
    user = $("#username").val()
    pass = $("#password").val()

    // checks if there is data inside the fields username and password
    if (user.length == 0 || pass .length == 0) {
        $("#updateMsg").html("Username and password can not be empty! enter data in those fields and try again");
        $("#updateMsg").show();
    }
    // checks if at least in one of the fields was a change
    else if (prev_user != user || prev_pass != pass){
        var my_url
        // change in both fields
        if (prev_user != user && prev_pass != pass) {
            my_url = "http://"+url+":"+port+'/update_user?uid=' + uid +'&username=' + user + '&pass=' + pass
        }
        // checks if change only in username
        else if (prev_user != user) {
            my_url = "http://"+url+":"+port+'/update_user?uid=' + uid +'&username=' + user
        }
        // change only in password
        else {
            my_url = "http://"+url+":"+port+'/update_user?uid=' + uid +'&pass=' + pass
        }
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            url: my_url,
            success: function (data) {
                // positive number means that the operation was a success
                if (data > 0){
                    prev_user = user
                    prev_pass = pass
                    $("#updateMsg").html("Your changes were successfully saved!");
                }
                // failure, could not save the changes
                else{
                    $("#updateMsg").html("Your changes were not saved, please try again...");
                }
                $("#updateMsg").show();
            },
            // something went wrong in the server.
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $("#updateMsg").html("Problem connecting to the server, please try again...");
                $("#updateMsg").show();
            }
        });
    }
    // no change was made in the user's data
    else {
        $("#updateMsg").html("You need to make some changes first..");
        $("#updateMsg").show();
    }
    });

    // returns to main menu page.
    $("#menu").click(()=>{
        if (user == undefined) {
            user = $.urlParam("user")
        }
        window.location = "./MainMenu.html?uid="+uid+"&user="+user+"&admin="+admin
    });
});

// function responsible to add to list checked genres and return the list.
$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}
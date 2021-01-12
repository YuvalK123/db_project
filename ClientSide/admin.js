var url = "localhost";
var port = 3000;

$(document).ready(()=>{
    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/admin/best_score',
        success: function (data) {
            // shows to user the highest score
            $("#highestScore").text(data)
        },
        // something went wrong with the request
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#adminErr").html("Problem connecting to the server, please try again...");
            $("#adminErr").show();
        }
    });

    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/admin/quantity_of_gamers',
        success: function (data) {
            // shows to user the number of players
            $("#playersNum").text(data)
        },
        // something went wrong with the request
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#adminErr").html("Problem connecting to the server, please try again...");
            $("#adminErr").show();
        }
    });

    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/admin/age_statistics',
        success: function (data) {
            // shows to user the age statistics
            $("#ageStatistics").text(data)
        },
        // something went wrong with the request
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#adminErr").html("Problem connecting to the server, please try again...");
            $("#adminErr").show();
        }
    });

    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/admin/gender',
        success: function (data) {
            // shows to user the gender statistics
            $("#genderStatistics").text(data)
        },
        // something went wrong with the request
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#adminErr").html("Problem connecting to the server, please try again...");
            $("#adminErr").show();
        }
    });

    // gets parameters for url
    var uid = $.urlParam("uid")
    var user = $.urlParam("user")
    var admin = $.urlParam("admin")
    // returns to main menu page
    $("#menu").click(()=>{
        window.location = "./MainMenu.html?uid="+uid+"&user="+user+"&admin="+admin
    });
    // takes the user to the page where he can add information to database.
    $("#addData").click(()=>{
        window.location = "./AddData.html?uid="+uid+"&user="+user+"&admin="+admin
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
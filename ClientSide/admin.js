var url = "localhost";
var port = 3000;

$(document).ready(()=>{
    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/admin/best_score',
        success: function (data) {
            $("#highestScore").text(data)

            $.ajax({
                type: 'GET',
                contentType: "application/json; charset=utf-8",
                url: "http://"+url+":"+port+'/admin/quantity_of_gamers',
                success: function (data) {
                    $("#playersNum").text(data)

                    $.ajax({
                        type: 'GET',
                        contentType: "application/json; charset=utf-8",
                        url: "http://"+url+":"+port+'/admin/age_statistics',
                        success: function (data) {
                            $("#ageStatistics").text(data)

                            $.ajax({
                                type: 'GET',
                                contentType: "application/json; charset=utf-8",
                                url: "http://"+url+":"+port+'/admin/gender',
                                success: function (data) {
                                    $("#genderStatistics").text(data)
                                },
                                error: function(XMLHttpRequest, textStatus, errorThrown) {
                                    $("#adminErr").html("Problem connecting to the server, please try again...");
                                    $("#adminErr").show();
                                }
                            });
                        },
                        error: function(XMLHttpRequest, textStatus, errorThrown) {
                            $("#adminErr").html("Problem connecting to the server, please try again...");
                            $("#adminErr").show();
                        }
                    });
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    $("#adminErr").html("Problem connecting to the server, please try again...");
                    $("#adminErr").show();
                }
            });
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#adminErr").html("Problem connecting to the server, please try again...");
            $("#adminErr").show();
        }
    });

    $("#menu").click(()=>{
        var uid = $.urlParam("uid")
        var user = $.urlParam("user")
        var admin = $.urlParam("admin")
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
var url = "localhost";
var port = 3000;

$(document).ready(()=>{
    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/get_genres',
        success: function (data) {
            data = JSON.parse(data)
            for (let i = 0; i < Math.floor(data.length/2); i++) {
                addCheckbox(data[i], i, 1);
            }
            for (let i = Math.floor(data.length/2); i < data.length; i++){
                addCheckbox(data[i], i, 2);
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#addDataMsg").html("Problem connecting to the server, please try again...");
            $("#addDataMsg").show();
        }
    });

    $("#save").click(()=>{
        $("#addDataMsg").hide();
        var name = $("#name").val()
        var born_in = $("#bornIn").val()
        var died_in = $("#diedIn").val()
        var movie = $("#movie").val()
        var role = $('input[name="role"]:checked').val()
        var gender = $('input[name="gender"]:checked').val()
        // checks the genres checked and adds to list
        var genres = get_selected_checkboxes_array()
        var obj = {
            "name": name,
            "bornin": born_in,
            "diedin": died_in,
            "gender": gender,
            "movie": movie,
            "genres": genres,
            "job": role
        };
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: obj,
            url: "http://"+url+":"+port+'/add_person',
            success: function (data) {
                $("#addDataMsg").html(data);
                $("#addDataMsg").show();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $("#addDataMsg").html("Problem connecting to the server, please try again...");
                $("#addDataMsg").show();
            }
        });

    });

    $("#back").click(()=>{
        var uid = $.urlParam("uid")
        var user = $.urlParam("user")
        var admin = $.urlParam("admin")
        window.location = "./Admin.html?uid="+uid+"&user="+user+"&admin="+admin
    });
});

function addCheckbox(name, index, numberContainer) {
    var containerName = "#genreContainer" + numberContainer
   var container = $(containerName);

   $('<input />', { type: 'checkbox', id: 'genre'+index, value: name }).appendTo(container);
   $('<label />', { 'for': 'genre'+index, text: name }).appendTo(container);
   $('<br >').appendTo(container)
}

$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}
function get_selected_checkboxes_array(){
    var ch_list=[]
    $("input:checkbox[type=checkbox]:checked").each(function(){
        ch_list.push($(this).val());
    });
    return ch_list;
}

//name='+name+"&gender="+gender+"&bornin="+born_in+"&diedin"+died_in+"&movie="+movie+"&genres="+genres+"&job="+role
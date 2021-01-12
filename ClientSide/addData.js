var url = "localhost";
var port = 3000;

$(document).ready(()=>{
    // sending request to server to get list of genres that are in the dataset.
    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/get_genres',
        success: function (data) {
            data = JSON.parse(data)
            // creates first column of the genres
            for (let i = 0; i < Math.floor(data.length/2); i++) {
                addCheckbox(data[i], i, 1);
            }
            // creates second list of genres
            for (let i = Math.floor(data.length/2); i < data.length; i++){
                addCheckbox(data[i], i, 2);
            }
        },
        // on failure, shows message to the user
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#addDataMsg").html("Problem connecting to the server, please try again...");
            $("#addDataMsg").show();
        }
    });

    // adds data when clicking the save button
    $("#save").click(()=>{
        $("#addDataMsg").hide();
        // gets all the values from the fields
        var name = $("#name").val()
        var born_in = $("#bornIn").val()
        var died_in = $("#diedIn").val()
        var movie = $("#movie").val()
        var role = $('input[name="role"]:checked').val()
        var gender = $('input[name="gender"]:checked').val()
        // checks the genres that are checked and adds to list
        var genres = get_selected_checkboxes_array()
        if (gender == undefined) {
            gender = ""
        }
        if (role == undefined) {
            role = ""
        }
        // creates object that will become a json object, so we can pass it to server
        var obj = {
            "name": name,
            "bornin": born_in,
            "diedin": died_in,
            "gender": gender,
            "movie": movie,
            "genres": genres,
            "job": role
        };
        // sending post request to server so it can add the data to the database
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify(obj),
            url: "http://"+url+":"+port+'/add_person',
            success: function (data) {
                // the server returns a string that explains to the user what happened
                if ((typeof data[0]) == 'string') {
                    $("#addDataMsg").html(data[0]);
                    $("#addDataMsg").show();
                } else {
                    // server sent a number, connection problem.
                    $("#addDataMsg").html("Problem connecting to the server, please try again...");
                    $("#addDataMsg").show();
                }
            },
            // something went wrong with the request.
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $("#addDataMsg").html("Problem connecting to the server, please try again...");
                $("#addDataMsg").show();
            }
        });

    });

    // when clicking the button we return to the main menu page
    $("#back").click(()=>{
        var uid = $.urlParam("uid")
        var user = $.urlParam("user")
        var admin = $.urlParam("admin")
        window.location = "./Admin.html?uid="+uid+"&user="+user+"&admin="+admin
    });
});

// the function responsible to create checkboxes and add them to html page for the genres.
function addCheckbox(name, index, numberContainer) {
    var containerName = "#genreContainer" + numberContainer
   var container = $(containerName);

   $('<input />', { type: 'checkbox', id: 'genre'+index, value: name }).appendTo(container);
   $('<label />', { 'for': 'genre'+index, text: name }).appendTo(container);
   $('<br >').appendTo(container)
}

// helps us to know the parameters that exists in our url
$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}

// function responsible to add to list checked genres and return the list.
function get_selected_checkboxes_array(){
    var ch_list=[]
    $("input:checkbox[type=checkbox]:checked").each(function(){
        ch_list.push($(this).val());
    });
    return ch_list;
}


var url = "localhost";
var port = 3000;

$(document).ready(()=>{
    var person = $.urlParam("person");
    $("#nameActor").html(person)
    data = {"gender": "m", "actedIn": [], "directed": [{"The Congres": ["Foreign", "Drama", "Animation"]}, {"Made in Israel": ["History", "War", "Family", "Crime"]}, {"Saint Clar": ["Horror", "Western"]}, {"Waltz with Bashir": ["War", "Foreign", "Crime"]}]}

    acted = data.actedIn
    directed = data.directed
    gender = data.gender

    for (var t=0;t<acted.length;t++){
        $("#movies").append("<p style=\"font-size: 18px;\">&#9675; "+Object.keys(acted[t])+" - as Actor - </p>")
    }
    for (var t=0;t<directed.length;t++){
        $("#movies").append("<p style=\"font-size: 18px;\">&#9675; <b>"+Object.keys(directed[t])+"</b> - as Director - "+directed[t][Object.keys(directed[t])].join(",")+"</p>")
    }

    // $.ajax({ 
    //     type: 'GET', 
    //     contentType: "application/json; charset=utf-8",
    //     url: "http://"+url+":"+port+'/movies?person='+person, 
    //     success: function (data) {
    //         if(data && data != "null"){
    //             $("#resbtn").show();
    //             oldGame = data;
    //         }
    //     },
    //     error: function(XMLHttpRequest, textStatus, errorThrown) {

    //     }  
    // });
})


$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}

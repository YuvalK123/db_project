var url = "localhost";
var port = 3000;

$(document).ready(()=>{
    var person = $.urlParam("person");
    $("#nameActor").html(person)
    $.ajax({ 
        type: 'GET', 
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/movies?person='+person, 
        success: function (data) {
            if(data && data != "null"){
                $("#resbtn").show();
                oldGame = data;
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {

        }  
    });
})


$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}

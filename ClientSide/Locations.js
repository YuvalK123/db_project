var url = "localhost";
var port = 3000;
var fetchIndex = 0;
var maxCount = 0;
$(document).ready(()=>{
    var uid = $.urlParam("uid")
     if(uid == null){
         window.location = "./"
     }
    var user = $.urlParam("user")
    $("#welcome").html("Welcome "+user+"!");

    $(document).on("click",".loc",(ev)=>{
        wordOrg = $(ev.target).html()
        $.ajax({ 
            type: 'GET', 
            contentType: "application/json; charset=utf-8",
            url: "http://"+url+":"+port+"/get_people?country="+wordOrg, 
            
            success: function (data) {
                $("#city").html(wordOrg)
                $("#dataModal").modal("show");                                
                data = JSON.parse(data)

                dataModelParser(data);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
    
            }  
        });
    })

        $("#showallborn").click((ev) => {
        if ($(ev.target).html().includes("show all")) {
            for (var k = 5; k < born.length; k++) {
                $("#borninfo").append("<a target='_blank' href='/ClientSide/MoviesByPerson.html?person="+born[k]+"'>" + born[k] + "</a><br>");
            }
            $(ev.target).html("show less");
        }
        else {
            $("#borninfo").empty();
            for (var k = 0; k < Math.min(born.length, 5); k++) {
                $("#borninfo").append("<a target='_blank' href='/ClientSide/MoviesByPerson.html?person="+born[k]+"'>" + born[k] + "</a><br>");
            }
            $(ev.target).html("show all");
        }
    });

    $("#showalldied").click((ev) => {
        if ($(ev.target).html().includes("show all")) {
            for (var k = 5; k < died.length; k++) {
                $("#diedinfo").append("<a target='_blank' href='/ClientSide/MoviesByPerson.html?person="+died[k]+"'>" + died[k] + "</a><br>");
            }
            $(ev.target).html("show less");
        }
        else {
            $("#diedinfo").empty();
            for (var k = 0; k < Math.min(died.length, 5); k++) {
                $("#diedinfo").append("<a target='_blank' href='/ClientSide/MoviesByPerson.html?person="+died[k]+"'>" + died[k] + "</a><br>");
            }
            $(ev.target).html("show all");
        }
    });

    $("#showallrests").click((ev) => {

        if ($(ev.target).html().includes("show all")) {

            for (var k = 5; k < rests.length; k++) {
                $("#restsinfo").append("<span>" + rests[k][0] + "</span><a target='_blank' href='https://www.google.co.il/maps/place/"+rests[k][1]+","+rests[k][2]+"'>  Location on Google Maps, </a><a target='_blank' href='"+rests[k][3]+"'>  Restaurant Website</a><br>");
            }
            $(ev.target).html("show less");
        }
        else {
            console.log("In else")
            $("#restsinfo").empty();
            for (var k = 0; k < Math.min(rests.length, 5); k++) {
                 $("#restsinfo").append("<span>" + rests[k][0] + "</span><a target='_blank' href='https://www.google.co.il/maps/place/"+rests[k][1]+","+rests[k][2]+"'>  Location on Google Maps, </a><a target='_blank' href='"+rests[k][3]+"'>  Restaurant Website</a><br>");
            }
            $(ev.target).html("show all");
        }
    });

    $("#showMore").click(()=>{
        if(fetchIndex+50 < maxCount){
            $.ajax({ 
                type: 'GET', 
                contentType: "application/json; charset=utf-8",
                url: "http://"+url+":"+port+'/user_country?uid='+uid+"&range="+fetchIndex+","+(fetchIndex+50), 
                success: function (data) {
                    if(data){
                        data = JSON.parse(data)
                        var count = data.count;
                        fetchIndex +=50
                        data = data.locations.split(",")
                        for (var t=0;t<data.length;t++){
                            $("#locations").append("<p style=\"font-size: 18px;\">&#9675; <b ><a href='#' class='loc' style='color:white'>"+data[t]+"</a></b></p>");
                        }
                    }
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
        
                }  
            });
        
        }

    });
    

    $.ajax({ 
        type: 'GET', 
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/user_country?uid='+uid, 
        success: function (data) {
            if(data){
                data = JSON.parse(data)
                
                fetchIndex = 50;
                maxCount = data.count;
                if(maxCount > 50){
                    $("#showMore").show()
                }
                else{
                    $("#showMore").hide()
                }
                data = data.locations.split(",")
                for (var t=0;t<data.length;t++){
                    $("#locations").append("<p style=\"font-size: 18px;\">&#9675; <b ><a href='#' class='loc' style='color:white'>"+data[t]+"</a></b></p>");
                }
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {

        }  
    });

    $("#menu").click(()=>{
        var admin = $.urlParam("admin")
        window.location = "./MainMenu.html?uid="+uid+"&user="+user+"&admin="+admin
    });

});


function dataModelParser(data) {

    $("#borninfo").empty()
    $("#diedinfo").empty()
    $("#restsinfo").empty()
    $("#showallborn").show();
    $("#showalldied").show();
    $("#showallrests").show();
    $("#showallborn").html("show all");
    $("#showalldied").html("show all");
    $("#showallrests").html("show all");


    info = data;
    info.born = info.born ? info.born : "";
    born = info.born.split(",");
    if (info.born.length > 0) {
        $("#bornSpan").show();
        for (var k = 0; k < Math.min(born.length, 5); k++) {
            $("#borninfo").append("<a target='_blank' href='/ClientSide/MoviesByPerson.html?person="+born[k]+"'>" + born[k] + "</a><br>");
            $("#bornSpan").show();
        }
    }
    else {
        $("#bornSpan").hide();
    }


    info.died = info.died ? info.died : "";
    died = info.died.split(",");
    if (info.died.length > 0) {
            $("#diedSpan").show();
        for (var k = 0; k < Math.min(died.length, 5); k++) {
            $("#diedinfo").append("<a target='_blank' href='/ClientSide/MoviesByPerson.html?person="+died[k]+"'>" + died[k] + "</a><br>");  
        }
    }
    else {
        $("#diedSpan").hide();
    }

    info.rests = info.rests ? info.rests : "";
    rests = info.rests.split(",");
    if (info.rests.length > 0) {
            $("#restsSpan").show();
        for (var k = 0; k < rests.length; k++) {
            rests[k] = rests[k].split(";")
        }
        for (var k = 0; k < Math.min(rests.length, 5); k++) {
            $("#restsinfo").append("<span>" + rests[k][0] + "</span><a target='_blank' href='https://www.google.co.il/maps/place/"+rests[k][1]+","+rests[k][2]+"'>  Location on Google Maps, </a><a target='_blank' href='"+rests[k][3]+"'>  Restaurant Website</a><br>");
        }
    }
    else {
        $("#restsSpan").hide();
    }

    if (born.length < 5) {
        $("#showallborn").hide();
    }

    if (died.length < 5) {
        $("#showalldied").hide();
    }

    if (rests.length < 5) {
        $("#showallrests").hide();
    }

    count = info.restsCount;
    if(count > 0){
        $("#restsCount").html("There are "+ count +" restaurants in the city of "+wordOrg+"!" )
    }
    $("#dataModal").modal("show");
}



$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}

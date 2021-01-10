var wordOrg;
var word;
var wLen;
var url = "localhost";
var port = 3000;
var mistakes;
var uid;
var user;
var old;
var points = 0;
var letterOptions = new Array(parseInt(26));; 
var letters = new Set();
var gid;
var info;
var born;
var died;
var hintsLeft;
var usedHints=0;
var hints = []
var hintsindex = 0;

$(document).ready(()=>{

    admin = $.urlParam("admin")
    $('#dataModal').modal({
        backdrop: 'static',
        keyboard: false,
        show: false
    })
    uid = $.urlParam("uid")
     if(uid == null){
         window.location = "./"
     }
    user = $.urlParam("user")
    old = $.urlParam("old")
    admin = $.urlParam("admin")
    $("#welcome").html("Welcome "+ user+"!" )
    if(old != null){
        $.ajax({ 
            type: 'GET', 
            contentType: "application/json; charset=utf-8",
            url: "http://"+url+":"+port+'/getgame?uid='+uid, 
            success: function (data) {
                data = JSON.parse(data)
                if(data){
                    oldGame = data;
                    gid = oldGame.gid
                    hintsLeft = oldGame.hints

                    $("#hintsCountInfo").html(hintsLeft)
                    $("#Mis").html(oldGame.strikes);
                    mistakes = oldGame.strikes
                    points = oldGame.score
                    $("#points").html("Points: "+oldGame.score);
                    if(!oldGame.curr_country){
                        getNewWord(false);
                    }
                    else{
                        if(oldGame.letters){
                            templetters = oldGame.letters.split(",")
                        }
                        else{
                            templetters = []
                            oldGame.letters = []
                        }
                        for (var t = 0;t<templetters.length;t++){
                            letters.add(templetters[t]);
                        }
                        wordOrg = oldGame.curr_country;
                        word = wordOrg.toLowerCase();
                        wLen = word.length
                        hiddenWord = new Array(wLen);
                        getHints(false)
                        for(var i=0;i<wLen;i++){
                            if(oldGame.letters.includes(word[i])){
                                hiddenWord[i]=[word[i],word[i]];
                            }
                            else{
                                hiddenWord[i]=["_",word[i]];
                            }
                        }
                        for(var i=0;i<wLen;i++){
                            if(hiddenWord[i][1]==" "||hiddenWord[i][1]=="-"||hiddenWord[i][1]=="_"){
                                $("#word").append("<span id='"+i+"' class='btn' style='background-color:white;color:black;margin-right:10px;width:70px;margin-bottom:10px' disabled>"+hiddenWord[i][1]+"</span>")
                            }
                            else{
                                $("#word").append("<span id='"+i+"' class='btn wordLettes' style=';background-color:white;color:black;margin-right:10px;width:70px;margin-bottom:10px'>"+hiddenWord[i][0]+"</span>")
                                if(hiddenWord[i][0]!="_"){
                                    $("#"+i).removeClass("colored");
                                    $("#"+i).addClass("good");
                                    $("#"+i).attr("disabled","disabled");
                                }
                            }
                        }
                        var alphabet = "abcdefghijklmnopqrstuvwxyz"
                        for(var i=0;i<26;i++){
                            letterOptions[i] = alphabet[i]
                        }
                        letterOptions = shuffle(letterOptions)
                        for(var i=0;i<26;i++){
                            if(!oldGame.letters.includes(letterOptions[i])){
                                if(word.includes(letterOptions[i]) && admin =="1"){
                                    $("#lettersOption").append("<button class='btn LettersOp goodLetter' style='color:black;margin-right:10px;width:50px;margin-bottom:10px'>"+letterOptions[i]+"</button>")
                                }
                                else{
                                    $("#lettersOption").append("<button class='btn LettersOp' style='color:black;margin-right:10px;width:50px;margin-bottom:10px'>"+letterOptions[i]+"</button>")
                                }
                            }
                        }
                    }
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
    
            }  
        });
    }
    else{
        mistakes = 5;
        points = 0;
        hintsLeft = 3;
        $("#hintsCountInfo").html(hintsLeft)
        $("#Mis").html(mistakes);
        $("#points").html("Points: "+points)
        getNewWord(true);
    }

    function getHints(isNew){
        var newVal;
        if(isNew){
            newVal = "true"
        }
        else{
            newVal = "false"
        }
        $.ajax({ 
            type: 'GET', 
            contentType: "application/json; charset=utf-8",
            url: "http://"+url+":"+port+'/hint?country='+wordOrg+'&user='+uid+'&new='+newVal,
            success: function (data) {
                data = JSON.parse(data)
                hints = data;
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
    
            }  
        });
    }

    function getNewWord(isNew){
        let addition;
        if(isNew == true){
            addition = "newgame"
        }
        else{
            addition = "get_country"
        }
        $.ajax({ 
            type: 'GET', 
            contentType: "application/json; charset=utf-8",
            url: "http://"+url+":"+port+'/'+addition+'?uid='+uid,
            success: function (data) {
                var english = /^[A-Za-z0-9]*$/;
                if (!english.test(data) ) {
                    getNewWord(isNew);
                    return;
                }
                wordOrg = data;
                word = wordOrg.toLowerCase();
                wLen = word.length
                hiddenWord = new Array(wLen);
                getHints(isNew)
                for(var i=0;i<wLen;i++){
                    hiddenWord[i]=["_",word[i]];
                }
                for(var i=0;i<wLen;i++){
                    if(hiddenWord[i][1]==" "||hiddenWord[i][1]=="-"||hiddenWord[i][1]=="_"||hiddenWord[i][1]==","){
                        $("#word").append("<span id='"+i+"' class='btn' style='background-color:white;color:black;margin-right:10px;width:70px;margin-bottom:10px' disabled>"+hiddenWord[i][1]+"</span>")
                    }
                    else{
                        $("#word").append("<span id='"+i+"' class='btn wordLettes' style=';background-color:white;color:black;margin-right:10px;width:70px;margin-bottom:10px'>"+hiddenWord[i][0]+"</span>")
                    }
                }
                var alphabet = "abcdefghijklmnopqrstuvwxyz"
                for(var i=0;i<26;i++){
                    letterOptions[i] = alphabet[i]
                }
                letterOptions = shuffle(letterOptions)
        
                for(var i=0;i<26;i++){
                    if(word.includes(letterOptions[i])  && admin =="1" ){
                        $("#lettersOption").append("<button class='btn LettersOp goodLetter' style='color:black;margin-right:10px;width:50px;margin-bottom:10px'>"+letterOptions[i]+"</button>")
                    }
                    else{
                        $("#lettersOption").append("<button class='btn LettersOp' style='color:black;margin-right:10px;width:50px;margin-bottom:10px'>"+letterOptions[i]+"</button>")
                    }
                    
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
            }  
        });
    }

    $("#menu").click(()=>{
        window.location = "./MainMenu.html?uid="+uid+"&user="+user+"&admin="+admin
    });
    
  $(document).on('click',".LettersOp",(event)=>{
    $(".LettersOp").removeClass("coloredBlue");
    $(event.target).addClass("coloredBlue")
    wrongFlag = true;
    for(var i=0;i<hiddenWord.length;i++){
        if($(event.target).text() == hiddenWord[i][1]){
            letters.add(hiddenWord[i][1])
            points+=15;
            $("#points").html("Points: "+points)
            wrongFlag = false;
            $("#"+i).text(wordOrg[i])
            $("#"+i).removeClass("colored");
            $("#"+i).addClass("good");
            $("#"+i).attr("disabled","disabled");
            $(event.target).remove();
            if(checkWin()){
                isWin = true;
                $.ajax({ 
                    type: 'POST', 
                        contentType : "application/x-www-form-urlencoded;charset=UTF-8",
                        dataType : 'json',
                        data : {
                            'country':"0",
                            'countries':wordOrg,
                            'letters':Array.from([]).join(','),
                            'strikes':mistakes,
                            'score':points,
                            'uid':uid,
                            'hints':(usedHints+1)
                        },
                    url: "http://"+url+":"+port+"/savegame", 
                    success: function (data) {
                        gid = data;            
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
            
                    }  
                });
                $.ajax({ 
                    type: 'GET', 
                    contentType: "application/json; charset=utf-8",
                    url: "http://"+url+":"+port+"/get_people?country="+wordOrg, 
                    success: function (data) {
                        data = JSON.parse(data)
                        $("#next").show();
                        $("#city").html(wordOrg)
                        $("#dataModal").modal("show");
                        
                        $("#modTitle").html("You Won! The Answer was " + wordOrg);

                        dataModelParser(data);

                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
            
                    }  
                });

            }
        }
    }
    if(wrongFlag){
        $("#next").hide();
        alert("Wrong letter! " + (--mistakes) +" mistaked left");
        $("#Mis").html(mistakes);
        $("#save").trigger("click");
        if(mistakes <= 0){
            if(gid){
                $.ajax({ 
                    type: 'GET', 
                    contentType: "application/json; charset=utf-8",
                    url: "http://"+url+":"+port+"/gameover?gid="+gid,
                    success: function (data) {

                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
            
                    }  
                });
            }
        

        $.ajax({ 
            type: 'GET', 
            contentType: "application/json; charset=utf-8",
            url: "http://"+url+":"+port+"/get_people?country="+wordOrg, 
            
            success: function (data) {
                $("#city").html(wordOrg)
                $("#dataModal").modal("show");
                
                $("#modTitle").html("You Lost! The Answer was " + wordOrg);
                data = JSON.parse(data)

                dataModelParser(data);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
    
            }  
        });
        }
        
    }
  });

  $("#next").click(()=>{
      if(admin == "1"){
        window.location = "./Game.html?uid="+uid+"&user="+user+"&old=1&admin=1"
      }
      else{
        window.location = "./Game.html?uid="+uid+"&user="+user+"&old=1"
      }
      
  });

  $("#hint").click(()=>{
      if(hintsLeft>0){
          hintsLeft--;
          usedHints--;
          $("#hintsCountInfo").html(hintsLeft)
           alert(hints[hintsindex%hints.length])
           hintsindex++
          $("#save").trigger("click");
      }
      else{
        alert("No More Hints Left!");
      }
    });

    $("#mainmenu").click(()=>{
        var uid = $.urlParam("uid")
        var user = $.urlParam("user")
        var admin = $.urlParam("admin")
        window.location = "./MainMenu.html?uid="+uid+"&user="+user+"&admin="+admin
    });


  $("#save").click(()=>{
    $.ajax({ 
        type: 'POST', 
            contentType : "application/x-www-form-urlencoded;charset=UTF-8",
            dataType : 'json',
            data : {
                'country':wordOrg,
                'countries':wordOrg,
                'letters':Array.from(letters).join(','),
                'strikes':mistakes,
                'score':points,
                'uid':uid,
                'hints':usedHints
            },
        url: "http://"+url+":"+port+"/savegame", 
        success: function (data) {
            gid = data;
            usedHints = 0;
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {

        }  
    });
  });  
});







$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}

function dataModelParser(data) {
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
        for (var k = 0; k < rests.length; k++) {
            rests[k] = rests[k].split(":")
        }
        for (var k = 0; k < Math.min(rests.length, 5); k++) {
            $("#restsinfo").append("<span>" + rests[k][0] + "</span><a target='_blank' href='https://www.google.co.il/maps/place/"+rests[k][1]+","+rests[k][2]+"'>  Location on Google Maps</a><br>");
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
                $("#restsinfo").append("<span>" + rests[k][0] + "</span><a target='_blank' href='https://www.google.co.il/maps/place/"+rests[k][1]+","+rests[k][2]+"'>  Location on Google Maps</a><br>");    
            }
            $(ev.target).html("show less");
        }
        else {
            $("#restsinfo").empty();
            for (var k = 0; k < Math.min(rests.length, 5); k++) {
                $("#restsinfo").append("<span>" + rests[k][0] + "</span><a target='_blank' href='https://www.google.co.il/maps/place/"+rests[k][1]+","+rests[k][2]+"'>  Location on Google Maps</a><br>");
    
            }
            $(ev.target).html("show all");
        }
    });
    $("#dataModal").modal("show");
}

function checkWin(){
    for(var i=0;i<$(".wordLettes").length;i++){
        if(!($($(".wordLettes")[i]).hasClass("good"))){
            return false;
        }
    }
    return true;
}

function shuffle(array) {
    let counter = array.length;

    // While there are elements in the array
    while (counter > 0) {
        // Pick a random index
        let index = Math.floor(Math.random() * counter);

        // Decrease counter by 1
        counter--;

        // And swap the last element with it
        let temp = array[counter];
        array[counter] = array[index];
        array[index] = temp;
    }
    return array;
}



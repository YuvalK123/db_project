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

    // fetching the get parameters
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
    // check if the game is a resume game or new game
    if(old != null){
        // getting the old game from the server using ajax
        $.ajax({ 
            type: 'GET', 
            contentType: "application/json; charset=utf-8",
            url: "http://"+url+":"+port+'/getgame?uid='+uid, 
            success: function (data) {
                data = JSON.parse(data)
                if(data){
                    oldGame = data;
                    // saving all the old game data
                    gid = oldGame.gid
                    hintsLeft = oldGame.hints
                    // setting the divs for the info to the user about hint and mistakes
                    $("#hintsCountInfo").html(hintsLeft)
                    $("#Mis").html(oldGame.strikes);
                    mistakes = oldGame.strikes
                    // drawing the hangman figure
                    drawHangman(5-mistakes)
                    points = oldGame.score
                    $("#points").html("Points: "+oldGame.score);
                    // checking if its a new level or middle of a level
                    if(!oldGame.curr_country){
                        getNewWord(false);
                    }
                    else{
                        // loading the game word and used letters
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
                        // saving the empty letter and good letter
                        for(var i=0;i<wLen;i++){
                            if(oldGame.letters.includes(word[i])){
                                hiddenWord[i]=[word[i],word[i]];
                            }
                            else{
                                hiddenWord[i]=["_",word[i]];
                            }
                        }
                        // putting the word empty letters on the screen.
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
                        // putting all the alphabet on the screen for the user expect already gussed letters
                        var alphabet = "abcdefghijklmnopqrstuvwxyz"
                        for(var i=0;i<26;i++){
                            letterOptions[i] = alphabet[i]
                        }
                        letterOptions = shuffle(letterOptions)
                        for(var i=0;i<26;i++){
                            if(!oldGame.letters.includes(letterOptions[i])){
                                // id admin showing the right letters.
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
                 alert("Problem connecting to the server, please try again...");
            }  
        });
    }
    else{
        // setting the default value for the new game
        mistakes = 5;
        drawHangman(5-mistakes)
        points = 0;
        hintsLeft = 3;
        $("#hintsCountInfo").html(hintsLeft)
        $("#Mis").html(mistakes);
        $("#points").html("Points: "+points)
        getNewWord(true);
    }

    function drawHangman(mistakes){
        // setting the figure according to the mistakes made.
        switch(mistakes) {
            case 0:
                $("#hang").attr("src","./images/0mis.png")
                break;
            case 1:
                $("#hang").attr("src","./images/1mis.png")
                break;
            case 2:
                $("#hang").attr("src","./images/2mis.png")
                break;
            case 3:
                $("#hang").attr("src","./images/3mis.png")
                break;
            case 4:
                $("#hang").attr("src","./images/4mis.png")
                break;
            case 5:
                $("#hang").attr("src","./images/5mis.png")
                break;
            default:
                 $("#hang").attr("src","./images/0mis.png")
                break;
          }
    
    }

    function getHints(isNew){
        // getting the hints from the server.
        var newVal;
        if(isNew){
            // if its a new game
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
                // saving the recived hints incaase the user asks for them.
                data = JSON.parse(data)
                hints = data;
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                     alert("Problem connecting to the server, please try again...");
            }  
        });
    }

    function getNewWord(isNew){
        // checking if its a new game
        let addition;
        if(isNew == true){
            addition = "newgame"
        }
        else{
            addition = "get_country"
        }
        // getiing the country to guess.
        $.ajax({ 
            type: 'GET', 
            contentType: "application/json; charset=utf-8",
            url: "http://"+url+":"+port+'/'+addition+'?uid='+uid,
            success: function (data) {
                // checking if there is a word not in english (checked in the server and in the database as well)
                var english = /^[A-Za-z0-9]*$/;
                if (!english.test(data) ) {
                    getNewWord(isNew);
                    return;
                }
                // setting the word
                wordOrg = data;
                word = wordOrg.toLowerCase();
                wLen = word.length
                hiddenWord = new Array(wLen);
                getHints(isNew)
                for(var i=0;i<wLen;i++){
                    hiddenWord[i]=["_",word[i]];
                }
                // setting the letters to guess
                for(var i=0;i<wLen;i++){
                    if(hiddenWord[i][1]==" "||hiddenWord[i][1]=="-"||hiddenWord[i][1]=="_"||hiddenWord[i][1]==","){
                        $("#word").append("<span id='"+i+"' class='btn' style='background-color:white;color:black;margin-right:10px;width:70px;margin-bottom:10px' disabled>"+hiddenWord[i][1]+"</span>")
                    }
                    else{
                        $("#word").append("<span id='"+i+"' class='btn wordLettes' style=';background-color:white;color:black;margin-right:10px;width:70px;margin-bottom:10px'>"+hiddenWord[i][0]+"</span>")
                    }
                }
                // feeling all the alphabet letters.
                var alphabet = "abcdefghijklmnopqrstuvwxyz"
                for(var i=0;i<26;i++){
                    letterOptions[i] = alphabet[i]
                }
                letterOptions = shuffle(letterOptions)
        
                for(var i=0;i<26;i++){
                    // if admin then showing the right letters.
                    if(word.includes(letterOptions[i])  && admin =="1" ){
                        $("#lettersOption").append("<button class='btn LettersOp goodLetter' style='color:black;margin-right:10px;width:50px;margin-bottom:10px'>"+letterOptions[i]+"</button>")
                    }
                    else{
                        $("#lettersOption").append("<button class='btn LettersOp' style='color:black;margin-right:10px;width:50px;margin-bottom:10px'>"+letterOptions[i]+"</button>")
                    }
                    
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                             alert("Problem connecting to the server, please try again...");
            }  
        });
    }
    // back to main menu
    $("#menu").click(()=>{
        window.location = "./MainMenu.html?uid="+uid+"&user="+user+"&admin="+admin
    });

    // when a letter is cliked
  $(document).on('click',".LettersOp",(event)=>{
    $(".LettersOp").removeClass("coloredBlue");
    $(event.target).hide()
    wrongFlag = true;
    // checking if the letter match anywhere
    for(var i=0;i<hiddenWord.length;i++){
        if($(event.target).text() == hiddenWord[i][1]){
            // if the letter match adding points and coloring the letter in the word
            letters.add(hiddenWord[i][1])
            points+=15;
            $("#points").html("Points: "+points)
            wrongFlag = false;
            $("#"+i).text(wordOrg[i])
            $("#"+i).removeClass("colored");
            $("#"+i).addClass("good");
            $("#"+i).attr("disabled","disabled");
            $(event.target).remove();
            // checking if there are more letters to guses.
            if(checkWin()){
                isWin = true;
                // saveing the game.
                $.ajax({ 
                    type: 'POST', 
                        contentType : "application/x-www-form-urlencoded;charset=UTF-8",
                        dataType : 'json',
                        data : {
                            'country':"0",
                            'countries':wordOrg,
                            'letters':Array.from([]).join(','),
                            'strikes':mistakes+1,
                            'score':+points+100,
                            'uid':uid,
                            'hints':(usedHints+1)
                        },
                    url: "http://"+url+":"+port+"/savegame", 
                    success: function (data) {
                        gid = data;            
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                             alert("Problem connecting to the server, please try again...");
                    }  
                });
                // getting the data about the city.
                $.ajax({ 
                    type: 'GET', 
                    contentType: "application/json; charset=utf-8",
                    url: "http://"+url+":"+port+"/get_people?country="+wordOrg, 
                    success: function (data) {
                        data = JSON.parse(data)
                        // showing the data screen
                        $("#next").show();
                        $("#city").html(wordOrg)
                        $("#dataModal").modal("show");
                        
                        $("#modTitle").html("You Won! The Answer was " + wordOrg);

                        dataModelParser(data);

                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                        alert("Problem connecting to the server, please try again...");
                    }  
                });

            }
        }
    }
    // the the letter dosen't match anywhere.
    if(wrongFlag){
        // updating the shown mistakes
        $("#next").hide();
        alert("Wrong letter! " + (--mistakes) +" mistaked left");
        $("#Mis").html(mistakes);
        // drawing the updated figure.
        drawHangman(5-mistakes)
        // saving the game.
        $("#save").trigger("click");
        // if the game is lost
        if(mistakes <= 0){
            if(gid){
                // deleting the actice game from the database
                $.ajax({ 
                    type: 'GET', 
                    contentType: "application/json; charset=utf-8",
                    url: "http://"+url+":"+port+"/gameover?gid="+gid,
                    success: function (data) {

                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                        alert("Problem connecting to the server, please try again...");
                    }  
                });
            }
        
           // showing data about the city.
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
                  alert("Problem connecting to the server, please try again...");
            }  
        });
        }
        
    }
  });
    // going to the next level if admin continue to be admin.
  $("#next").click(()=>{
      if(admin == "1"){
        window.location = "./Game.html?uid="+uid+"&user="+user+"&old=1&admin=1"
      }
      else{
        window.location = "./Game.html?uid="+uid+"&user="+user+"&old=1"
      }
      
  });

    // getting hint
  $("#hint").click(()=>{
      if(hintsLeft>0){
          hintsLeft--;
          usedHints--;
          $("#hintsCountInfo").html(hintsLeft)
           alert(hints[hintsindex%hints.length])
           hintsindex++
           // saving the game with updated hint.
          $("#save").trigger("click");
      }
      else{
        alert("No More Hints Left!");
      }
    });
    // back to main menu
    $("#mainmenu").click(()=>{
        var uid = $.urlParam("uid")
        var user = $.urlParam("user")
        var admin = $.urlParam("admin")
        window.location = "./MainMenu.html?uid="+uid+"&user="+user+"&admin="+admin
    });

    // saveing the game
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
                        alert("Problem connecting to the server, please try again...");
        }  
    });
  });  
});






// to get the parameters.
$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}

// parsing the data about the city.
function dataModelParser(data) {
    info = data;
    info.born = info.born ? info.born : "";
    born = info.born.split(",");
    // showing who was born here.
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

    // showing who died here.
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

    // showing the resturnas in the city.
    info.rests = info.rests ? info.rests : "";
    rests = info.rests.split(",");
    if (info.rests.length > 0) {
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

    // option to show more data if available.
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

    // when you click the show more button loading more data, when click show less showing only few data.
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

    // when you click the show more button loading more data, when click show less showing only few data.
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

    // when you click the show more button loading more data, when click show less showing only few data.
    $("#showallrests").click((ev) => {
        if ($(ev.target).html().includes("show all")) {
            for (var k = 5; k < rests.length; k++) {
                $("#restsinfo").append("<span>" + rests[k][0] + "</span><a target='_blank' href='https://www.google.co.il/maps/place/"+rests[k][1]+","+rests[k][2]+"'>  Location on Google Maps, </a><a target='_blank' href='"+rests[k][3]+"'>  Restaurant Website</a><br>");
            }
            $(ev.target).html("show less");
        }
        else {
            $("#restsinfo").empty();
            for (var k = 0; k < Math.min(rests.length, 5); k++) {
                $("#restsinfo").append("<span>" + rests[k][0] + "</span><a target='_blank' href='https://www.google.co.il/maps/place/"+rests[k][1]+","+rests[k][2]+"'>  Location on Google Maps, </a><a target='_blank' href='"+rests[k][3]+"'>  Restaurant Website</a><br>");
    
            }
            $(ev.target).html("show all");
        }
    });
    $("#dataModal").modal("show");
}

// cecking if no more letters to guess.
function checkWin(){
    for(var i=0;i<$(".wordLettes").length;i++){
        if(!($($(".wordLettes")[i]).hasClass("good"))){
            return false;
        }
    }
    return true;
}

// to shuffle the alphabet
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



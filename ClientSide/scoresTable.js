var url = "localhost";
var port = 3000;

$(document).ready(()=>{
    $.ajax({
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: "http://"+url+":"+port+'/bestScores',
        success: function (data) {
            data = JSON.parse(data)
            var table = $('<table>').addClass('table table-borderless')
            // headings
            heading_row = $('<thead>')
            heading_row.append($('<th>').addClass('text-center').text('num'))
            heading_row.append($('<th>').addClass('text-center').text('username'))
            heading_row.append($('<th>').addClass('text-center').text('score'))
            heading_row.append($('<th>').addClass('text-center').text('date time'))
            table.append(heading_row)
            t_body = $('<tbody>')
            for (let row = 0; row < data.length; row++) {
                var curr_row = $('<tr>')
                curr_row.append($('<th>').addClass('text-center').text(row + 1))
                for (let col = 0; col < data[row].length; col++) {
                    console.log(data[row][col])
                    curr_row.append($('<td>').addClass('text-center').text(data[row][col]))
                }
                t_body.append(curr_row);
            }
            table.append(t_body)
            $('#table').append(table);
            console.log(10)

        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#loginErr").html("Problem connecting to the server, please try again...");
            $("#loginErr").show();
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
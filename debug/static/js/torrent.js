$(document).ready(function(){

    console.log('jQuery successfully loaded!');

    var r = 'None';

    $('button.btn-xs.btn-success').click( function (e){
        console.log('queue download button clicked')

        var $item = $(this).closest("tr")   // Finds the closest row <tr> 
                           .find(".info_hash")     // Gets a descendent with class="nr"
                           .text();         // Retrieves the text within <td>
        console.log($item)

        $.post('/torrent/add', {'info_hash': $item}).done(function(result){
                console.log("Response: " + result + "\n");
        });
        e.preventDefault();
    });

});
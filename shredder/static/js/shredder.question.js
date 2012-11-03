$(document).ready(function() {
    $('input#id_tag_list').attr("readonly",true);
    $('div.tag_cloud').click(function() {
        var array = [];
        val = $('input#id_tag_list').val();
        if(val){
            array = val.split(',');
        }
        text = $.trim($(this).text());
        pos = array.indexOf(text);
        if(~pos){
            array.splice(pos, 1);
        }
        else{
            array.push(text);
        }
        $('input#id_tag_list').val(array.join(','));
    });
});

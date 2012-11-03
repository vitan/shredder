$(document).ready(function(){

    $(".dropdown").dropdown();

    if($(".tree").length){
    $(".table tr:even").addClass("tr-even");
    $(".table td").mouseover(function(){
        $(this).parent().addClass("change-tr").mouseout(function(){
		$(this).removeClass("change-tr");
	})
    })
    $(".table td:nth-child(1)").addClass("pass");
    $(".table tr:last").addClass("last");
     /*   $(".tree").resizable({
            handles:"e",
            maxWidth:600,
            minWidth:300,
            alsoResize:'.content'
         });
        $(".tree").resize(function(){
	        var treewidth = $(".tree").width();
            $(".content").width(1180 -treewidth);
        })*/
    }
})

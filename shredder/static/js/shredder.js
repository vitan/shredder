$(document).ready(function() {
    shredder.init.main();
});

shredder.init = {
	main: function(){
	      if(shredder.ui.exists('form.share-question-form')){
		      shredder.ui.readonly('input#id_tag_list');
		      shredder.ui.tagCloud();
	      }
	      if(shredder.ui.exists('#id_question_list')){
		      shredder.ui.questionListDisplay();
		      shredder.ui.readonly('input#id_tag_list');
		      shredder.ui.tagCloud();
		      shredder.ui.displayFormToggle();
		      shredder.form.submitToggle();
	      }
        },
}

shredder.form = {
	submitToggle: function(){
		$('form.review-question-form').live('submit', function(){
            var obj = $(this);
		    var form_container = obj.parent().find(".form-post-part");
		    var question_container = obj.parent().parent().find(".question");
		    var url = obj.attr("action");
		    var data = obj.serialize();
		    shredder.ajax.post(url, data, function(response){
			    if(shredder.ajax.isSuccessful(response.rc)){
                    shredder.ui.fieldFill(-1, form_container);
                    obj.parent().hide();
                    obj.parent().parent('div').find('.question-display').show();
                    return true;
			    }
			    else{
                    //TODO (weizhou) form error display
				    alert(response);
			    }
		    });
		    return false;
	       });
        },
}

shredder.ui = {
	exists: function(selector) {
		return ($(selector).length > 0);
	},
	questionListDisplay: function(){
	     var divForm = $('div.form-post-part');
         //TODO (weizhou) args: index is invalid now.
	     divForm.each(this.fieldFill);
	},
    fieldFill: function(index, divObj){
         var divDisplay = $(divObj).parent().parent().parent().find('div.question-display');
         var span = $(divObj).find("span.question-field");
         span.each(function(){
             var id = $(this).attr('id');
             var val = null;
             var child = $(this).find('>:first-child');
             val = child.val();
             if (child.prop("tagName") == "SELECT"){
                 val = $(this).find('>:first-child option:selected').text();
             }
             divDisplay.find('span#'+id).text(val);
         });
    },
	readonly: function(selector) {
	    $(selector).attr("readonly",true);
        },
	tagCloud: function(){
	    $('div.tag-cloud').click(function() {
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
	},
	displayFormToggle: function(){
	    $('input.js-question-review-button').click(function(){
		    $(this).parent().hide();
		    $(this).parent().parent('div').find('.review-form').show();
	    });
	    $('input.js-question-form-cancel').click(function(){
		    $(this).parent().parent().hide();
		    $(this).parent().parent().parent('div').find('.question-display').show();
	    });
        },
}
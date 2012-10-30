$(document).ready(function() {
    shredder.init.main();
});

shredder.init = {
	main: function(){
	      if(shredder.ui.exists('form.share-question-form')){
		      shredder.ui.readonly('input#id_tag_list');
		      shredder.ui.type_checked('input#id_type_0');
		      shredder.ui.objective_choice_display();
		      shredder.ui.tagCloud();
	      }
	      if(shredder.ui.exists('#id_question_list')){
		      shredder.ui.questionListDisplay();
		      shredder.ui.readonly('input#id_tag_list');
		      shredder.ui.tagCloud();
		      shredder.ui.displayFormToggle();
		      shredder.form.reviewSubmitToggle();
	      }
	      if(shredder.ui.exists('form.generate-questionnaire-form')){
		      shredder.ui.readonly('input#id_tag_list');
		      shredder.ui.tagCloud();
		      shredder.form.generateSubmitToggle();
	      }
        },
}

shredder.form = {
	reviewSubmitToggle: function(){
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
	generateSubmitToggle: function(){
		$('form.generate-questionnaire-form').live('submit', function(){
		    var obj = $(this);
		    var form_container = obj.parent().find(".form-post-part");
		    var questionnaire_container = obj.parent().parent().find("div.generated-questionnaire");
		    var url = obj.attr("action");
		    var data = obj.serialize();
		    shredder.ajax.post(url, data, function(response){
			    if(shredder.ajax.isSuccessful(response.rc)){
				    var html = [];
				    $.each(response.data.items, function(index, value){
					    var span = '<div><span order="'+index+'" id="id_'+value.pk+'">'+value.desc+'</span></div>'; 
					    html.push(span);
				    });
				    questionnaire_container.html(html.join(''));
				    return true;
			    }
			    else{
				    //TODO (weizhou) form error display
				    ;
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

	     select_val = child.find('option:selected').text();
	     radio_val = child.find('input[type=radio]:checked').parent().text();

             val = select_val||radio_val||child.val();
             divDisplay.find('span#'+id).text(val);
	   });
	},
	readonly: function(selector) {
	    $(selector).attr("readonly",true);
        },
	type_checked: function(selector) {
	    $(selector).attr("checked", true);
        },
	objective_choice_display: function() {
	   $('#id_hide_choice').attr('disabled', 'disabled');
	   $('input[type="radio"]').change(function(){
		   var checkbox = $(this).find('input[type="checkbox"]');
		   checkbox.attr('checked', !checkbox.attr('checked'));

		   var col_is_answer = $('.choice-config');
		   if(col_is_answer.hasClass('hidden')){
			   col_is_answer.removeClass('hidden');
		   }
		   else{
			   col_is_answer.addClass('hidden');
		   }
	   });
	   $('#id_show_choice').click(function(){
		   var choice_num = parseInt($('#id_choice_set-MAX_NUM_FORMS').val())||0;
		   var choice_total = $('#id_choice_set-TOTAL_FORMS').val();

		   choice_num = choice_num + 1;
		   $('#id_choice_set-MAX_NUM_FORMS').val(choice_num);
		   $('#id_choice_set-'+choice_num+'-description').parent().parent().removeClass('hidden');

		   $("#id_hide_choice").removeAttr("disabled");
		   if(choice_num+1 == choice_total) {
			   $(this).attr("disabled", "disabled");
		   }
	   });
	   $('#id_hide_choice').click(function(){
		   var choice_num = parseInt($('#id_choice_set-MAX_NUM_FORMS').val())||0;
		   var choice_total = $('#id_choice_set-TOTAL_FORMS').val();

		   $('#id_choice_set-'+choice_num+'-description').parent().parent().addClass('hidden');
		   choice_num = choice_num-1;
		   $('#id_choice_set-MAX_NUM_FORMS').val(choice_num);

		   $("#id_show_choice").removeAttr("disabled");
		   if(choice_num == 0){
			   $(this).attr("disabled", "disabled");
		   }
	   });
       },
	tagCloud: function(){
	    $('div.tag-cloud').click(function() {
		var array = [];
		val = $(this).parent().parent().find('input#id_tag_list').val();
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
		$(this).parent().parent().find('input#id_tag_list').val(array.join(','));
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

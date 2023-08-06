jQuery(document).on("submit","form.form_validation",function(e){
	var num = 0;
	jQuery(".error_message").remove();	
	jQuery(this).find(".c_required").each(function(){
	if((jQuery(this).val()).trim() == ""){ num++; jQuery(this).after("<p class='error_message'>Please fill required field!</p>");}
	});
	if(num != 0){
	e.preventDefault();
	}
});

jQuery(document).ready(function(){
jQuery(document).on("change","select.page_visible",function(){
	if(jQuery(this).val() == "afterlogin"){
		jQuery("div.page_accesslevel").show();
	}else{
		jQuery("div.page_accesslevel").hide();
	}

});

/** reset password Link **/
	var abrt ="";
	var ajaxURL ="/dj-admin/forgot-password-submit";
	jQuery(document).on("submit","form.form-forgot",function(){
		  
			jQuery(".error_message").remove();
			jQuery(".message_show").remove();
			var obj = jQuery(this);
			obj.after("<p class='message_show'>Please wait..</p>");
		 if(abrt){ abrt.abort();}
			var email=obj.find("#forgotemail").val();
			if(email==""){ jQuery(".message_show").remove(); obj.find("#forgotemail").focus(); return false;}
			abrt=jQuery.ajax({
				url:ajaxURL,
				dataType:'json',
				data:{email:email},
				success:function(resp){
					jQuery(".message_show").remove();
					if(resp.value=="Email does not exists.."){
							obj.after("<p class='error_message'>Your email does not exists</p>");
					}else{
						obj.find("#forgotemail").val('');
						jQuery("body").addClass("popup-on");
						jQuery(".forget-passwrod-message").show();
						jQuery("html,body").animate({scrollTop:0},'slow');
					}	
				},
				error:function(resp){
				
				}
			});
	})
	
		/** Submit Setting options **/
		var ajaxOptionURL ="/dj-admin/options/submit";
		jQuery(document).on("submit","form.submit_options",function(){
			  if(abrt){ abrt.abort();}
			  jQuery(".option_message").remove();
			  var obj = jQuery(this);
				abrt=jQuery.ajax({
					url:ajaxOptionURL,
					type:'post',
					dataType:'json',
					data:jQuery(this).serialize(),
					success:function(data,textStatus,statusCode){
							obj.find("input[type='submit']").before("<p class='option_message'>Successfully Updated <p>");
							setTimeout(function(){jQuery(".option_message").remove();},3000);
					},
					error:function(data,textStatus,statusCode){
					
					}
				});
			
		});
	jQuery(document).on("click",".popup_close",function(){
		jQuery("body").removeClass("popup-on");
		jQuery(".forget-passwrod-message").hide();
		jQuery("html,body").animate({scrollTop:jQuery("a").offset().top},'slow');
	});	
});


jQuery(document).on("click",".RecordDeleteClass", function (e) {
	  var id = jQuery(this).attr("rel");
	  jQuery("div#deleteBox input[name='record_id']").val(id);
	});
function getval(sel)
{
	if(sel.value=="1"){
	jQuery(".license").css("display", "block");	
	jQuery('.license input[type=text]').addClass('c_required');
	jQuery('.license input[type=file]').addClass('c_required');
	}else{
	jQuery(".license").css("display", "none");
	jQuery('.license input[type=text]').removeClass('c_required');
	jQuery('.license input[type=file]').removeClass('c_required');
	}
}



jQuery(document).ready(function() {
	if(jQuery("#usertype").val()=="1"){
	jQuery(".license").css("display", "block");	
	/* jQuery('.license input[type=text]').addClass('c_required');
	jQuery('.license input[type=file]').addClass('c_required'); */
	}else{
	jQuery(".license").css("display", "none");
	/* jQuery('.license input[type=text]').removeClass('c_required');
	jQuery('.license input[type=file]').removeClass('c_required');	 */
		
	}
});


function isPassword(pass) {
  
	  
	  // Validate length
	  if(pass.length >= 6) {
		isvalidpass = true;
	  } else {
		isvalidpass = false;
	  }
	  return isvalidpass ;
  }
  
jQuery(".password").on("blur",function (event) {
	var passwordtxt = jQuery(this).val();
	if (jQuery(this).parents(".control").find(".error_message").length > 0){
			jQuery(this).parents(".control").find(".error_message").remove();
		}
	if(!isPassword(passwordtxt) && passwordtxt!=""){jQuery(this).parents(".control").append("<p class='error_message'>Password must contain at least 6 or more characters</p>");  
	num = num+1;
	obj = jQuery(this);
	}
	else
	{
		if(num>0)
			num = num - 1 ;
		else
			num = 0 ;
	}	
});  
jQuery(document).ready(function(){
	jQuery(document).on("keyup",".get_page_title",function(){
		var title = jQuery(this).val();
		jQuery(".set_page_title").val(convertToSlug(title));
	});
	
});

function convertToSlug(Text)
{
    return Text
        .toLowerCase()
        .replace(/[^\w ]+/g,'')
        .replace(/ +/g,'-')
        ;
}
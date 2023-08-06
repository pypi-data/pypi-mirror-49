var formUpload;
jQuery(document).ready(function(){
if(jQuery('.post_editor').length > 0){
		jQuery('.post_editor').jqte();
	}
var abrt ="";
var ajaxURLForMedia ="/dj-admin/media-ajax-load";
	var textItem = 1;
	jQuery(".media_lib_list").on("scroll",function(){
		  if(jQuery(".popbox_paging").length > 0){
		  var bottom_pos = parseInt(jQuery(".media_lib_list").height())-parseInt(jQuery(".media_lib_list").scrollTop());
		   if(jQuery(this).scrollTop() + jQuery(this).innerHeight() >= jQuery(this)[0].scrollHeight) {
		   textItem = textItem + 1 ;
		   if (textItem > parseInt(jQuery(".popbox_paging").data("id"))) { return false;}
		   var obj = jQuery(".popbox_paging .paginate_button.active").next(".paginate_button");
		   jQuery(".popbox_paging .paginate_button").removeClass('active');
		   obj.addClass("active");
			console.log(textItem);
			if(abrt){ abrt.abort();}
			abrt=jQuery.ajax({
				url:ajaxURLForMedia+"/"+textItem,
				success:function(data,textStatus,statusCode){
						jQuery(".media_lib_list").append(data);
						jQuery("input[name='box_scroll_page']").val(textItem);
				},
				error:function(data,textStatus,statusCode){
				
				}
			});
		
		   }
		   }
	});

jQuery(document).on('click','.choose_upload_file_btn',function(){
		jQuery("input[name='ajax_file']").trigger('click');
});
jQuery(document).on('click','button.upload_image',function(){
		jQuery(".form_ajax_bg,.form_ajax_popup_box").show();
		formUpload=jQuery(this).parent("div.upload_image");
		jQuery(".form_ajax_popup_box").attr('data-field',formUpload);
});
jQuery(document).on('click','.media_lib_list .attach_thumb',function(){
	jQuery('.media_lib_list .attach_thumb').removeClass("selected");
	jQuery(this).addClass("selected");
	jQuery(".selected_image_name").html(jQuery(this).find(".attach_filename").html());
});
jQuery(document).on('click','img.upload_img',function(){
	var ok =confirm('Are you sure!');
	if(ok==true){
	jQuery(this).parent("div.upload_image").find("input").val('');
	jQuery(this).remove();
	}
});
var ajaxURLForMediaDelete="/dj-admin/media/delete"
jQuery(document).on('click','i.fa.fa-trash.delete_media_file',function(){
	var ok =confirm('Are you sure!');
		if(ok==true){
			jQuery(this).parents("li.attach_thumb").remove();
		var id = jQuery(this).data("id");
		if(abrt){ abrt.abort();}
			abrt=jQuery.ajax({
				url:ajaxURLForMediaDelete+"/"+id,
				success:function(data,textStatus,statusCode){
					
				},
				error:function(data,textStatus,statusCode){
				
				}
			});
	}
});

jQuery(document).on('click','.insert_uploaded_image',function(){
	if(jQuery('.media_lib_list .attach_thumb.selected').length > 0){
		formUpload.find("input").val(jQuery('.media_lib_list .attach_thumb.selected').data("id"));
		formUpload.find("img").remove();
		formUpload.prepend("<img src='"+jQuery('.media_lib_list .attach_thumb.selected img').attr("src")+"' class='upload_img' title='click and remove it'/>");
		jQuery('.media_lib_list .attach_thumb').removeClass("selected");
		jQuery('.form_ajax_bg, .form_ajax_popup_box').hide();
		jQuery(".form_ajax_popup_box").removeAttr("data-field");
		return ;
	}
	alert("Please select image");
});
jQuery(document).on('click','.form_ajax_bg',function(){
		jQuery('.form_ajax_bg, .form_ajax_popup_box').hide();
		jQuery(".form_ajax_popup_box").removeAttr("data-field");
});

jQuery(document).on('change','#AjaxFileinput',function(){
	var url=jQuery('#AjaxformSubmit').attr('action');
    ajaxFormSubmit(url,'#AjaxformSubmit',function(output){
		
		
		
    })	
});	
});

function ajaxFormSubmit(url, form, callback) {
    var formData = new FormData($(form)[0]);
	jQuery(".img_preview").show();
	jQuery(".cerror").remove();
    jQuery.ajax({
        url: url,
        type: 'POST',
        data: formData,
        beforeSend: function() {
            // do some loading options
        },
        success: function(data) {
        	jQuery(".img_preview").hide();
			if(data=="Invalid file type"){alert(data);}
			else{
			jQuery(".img_preview").after('<span class="alert alert-success cerror">File has been uploaded successfully</span>');
			jQuery('#AjaxFileinput').val('');
			setTimeout(function(){jQuery(".cerror").remove();},2500);
			
			if(data.length > 0 && data!="error"){
			data = '<li class="attach_thumb" data-id="'+data+'"><img src="'+data+'" class="im-responsive"/><i class="fa fa-trash delete_media_file" data-id=""></i><span class="attach_filename">'+data+'</span></li>';
			jQuery("div#media_all_image ul.media_lib_list").prepend(data);
			}else{
				alert("Something went wrong.Please try again.");
				
			}
			}
        },
 
        complete: function() {
            // success alerts
        },
 
        error: function(xhr, status, error) {
            alert(xhr.responseText);
        },
        cache: false,
        contentType: false,
        processData: false
 
    });
 
}



jQuery(window).on("load",function () {
	setTimeout(function(){
		if(jQuery("#menu--edit").length > 0){
			jQuery("#btnReload").trigger("click");
		}
	},400);
});
jQuery(document).ready(function () {
				
			   /* =============== DEMO =============== */
                // menu items
                var arrayjson = [];
                // icon picker options
                var iconPickerOptions = {searchText: "Buscar...", labelHeader: "{0}/{1}"};
                // sortable list options
                var sortableListOptions = {
                    placeholderCss: {'background-color': "#cccccc"}
                };

                var editor = new MenuEditor('myEditor', {listOptions: sortableListOptions, iconPicker: iconPickerOptions});
                editor.setForm(jQuery('#frmEdit'));
                editor.setUpdateButton(jQuery('#btnUpdate'));
                var abrt="";
				jQuery(document).on('click','#btnOutput',function () {
                    var str = editor.getString();
                    jQuery("#out").text(str);
					 if(abrt){ abrt.abort();}
					abrt=jQuery.ajax({
						 url:jQuery(".menu--submit--form").attr("action"),
						 type:'post',
						 dataType:'json',
						 data:jQuery(".menu--submit--form").serialize(),
						 success:function(data,textStatus,statusCode){
							window.location="/dj-admin/menus";	
						  },
						 error:function(data,textStatus,statusCode){
							
						 }
						});
                });
				jQuery(document).on('click','#btnUpdate',function(){
                    editor.update();
                });
				jQuery(document).on('click','#btnAdd',function(){
                    editor.add();
                });
				jQuery(document).on('click','#btnReload',function(){
				     editor.setData(jQuery("#out").text());
                });

                /* ====================================== */

               
            });
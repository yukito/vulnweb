$('#article').load(location.pathname.replace(/group/g, "article"))

function editArticle(indicator){
   article = $(indicator).html();
   $('#article').load(location.pathname.replace(/group/g, "article"), function(){
      $.get('/get_token', function(token){
         edit_form = '\
                  <form action="' + location.pathname.replace(/group/g, "edit") + '" method="post" class="form-horizonal">\
                  <div class="form-group">\
                     <textarea rows="3" class="form-control" id="InputTextarea" name="post_detail">' + article + '</textarea>\
                  </div>\
                  <input type="hidden" name="article_id" value="' + indicator + '">\
                  <input type="hidden" name="_csrf_token" value="' + token + '">\
                  <input type="submit" class="btn btn-default" value="Save">\
                  <input type="button" class="btn btn-default" value="Cancel" onclick="javascript:cancelEdit()"></form>';
         $(indicator).html(edit_form);
      });
   });
}

function cancelEdit(){
   $('#article').load(location.pathname.replace(/group/g, "article"))
}

function deleteArticle(indicator){
   $.get('/get_token', function(token){
      $.post(location.pathname.replace(/group/g, "delete"), {"article_id": indicator, "_csrf_token": token}, function(){
         $('#article').load(location.pathname.replace(/group/g, "article"));
      });
   });
}

function showDeleteArticle(indicator){
   $(indicator).show()
}

function hideDeleteArticle(indicator){
   $(indicator).hide()
}

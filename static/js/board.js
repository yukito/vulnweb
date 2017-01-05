$('#article').load(location.pathname.replace(/group/g, "article"))

function editArticle(indicator){
   $('#article').load(location.pathname.replace(/group/g, "article"), function(){
      article = $(indicator).html();
      console.log(article);
      $(indicator).html('<form action="" method="post" class="form-horizonal"><div class="form-group"><textarea rows="3" class="form-control" id="InputTextarea" name="post_detail">' + article + '</textarea></div><small><input type="submit" class="btn btn-default" value="Save"></small></form>');
   });
}

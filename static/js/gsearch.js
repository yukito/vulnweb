function searchGroup(){
   $.get('/get_token', function(token){
      $.post('/search/group', {"search_word": $('#SearchWord').val(), "_csrf_token": token}, function(result){
         $('#search_result').html(result);
      });
   });
}

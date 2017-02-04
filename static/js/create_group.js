function add_member(){
   name = $("#InputGroupMember").val();
   $.get('/check_user?username=' + name, function(response){
      if(response == "True"){
         $("#GroupMembers").html($("#GroupMembers").html()+'<option value="' + name + '">' +name + '</option>');
         $("#GroupMembersParam").val($("#GroupMembersParam").val()+' ' + name);
         $("#InputGroupMember").val("");
      }else{
         $("#alertMessage").html('<div class="alert alert-warning" role="alert">No such user</div>');
      }
   });
}

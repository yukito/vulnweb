function add_member(){
   name = $("#InputGroupMember").val();
   $("#GroupMembers").html($("#GroupMembers").html()+'<option value="' + name + '">' +name + '</option>');
   $("#GroupMembersParam").val($("#GroupMembersParam").val()+' ' + name);
   $("#InputGroupMember").val("");
}

$("#input-pass").submit(function(){
  if ($("#InputPassword").val() != $("#ConfirmPassword").val()) {
    $("#NotMatch").show();
    return false;
  } else {
    $("#input-pass").submit();
  }
});
var xhr_res = new XMLHttpRequest();
xhr_res.onreadystatechange = function()
{
    if( this.readyState == 4 && this.status == 200 )
    {
        if( this.response )
        {
            alert( this.response );
        }
    }
}

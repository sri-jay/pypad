$("#save").click(function(){

	var code = editor.getSession().getDocument().getValue();
	var unique_hash = document.getElementById("#hash");
	var email = document.getElementById("#email");
	var comments = document.getElementById("#comments");

	$.ajax({
		url : "http://dry-springs-9524.herokuapp.com/save",
		type : "POST",
		data : {CODE : code,HASH:unique_hash,EMAIL;email,COMMENTS:comments},
		success : function(reply){
			if(reply['STATUS'] != 'TRUE'){
				alert("Failer to enter data to DB");
			}
			else
			{
				console.log("Done");
			}

		}
	});


});
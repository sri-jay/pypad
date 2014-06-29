$("#run").click(function(){

	$.ajax({
		url : "http://127.0.0.1:5000/run",
		type : "POST",
		data : editor.getSession().getDocument().getValue(),
		success : function(reply){

			console.log(reply);
		}
	});

});

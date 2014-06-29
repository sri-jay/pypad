$(document).ready(function(){

	/*Create Editor*/
	var editor = ace.edit("editor");
	editor.setTheme("ace/theme/monokai");
	editor.getSession().setMode("ace/mode/python");
	editor.setFontSize(18);
	editor.getSession().getDocument().insertLines(0,["# Type Code here","print 'Hello, World!'"]);

	$("#run").click(function(){
		$.ajax({
			url : "http://dry-springs-9524.herokuapp.com/run",
			type : "POST",
			data : {code : editor.getSession().getDocument().getValue()},
			success : function(reply){

				var OUTPUTS = "<div class='STDOUT'>"+reply["STDOUT"]+"</div>" +
				"<div class='STDERR'>"+reply["STDERR"]+"</div>";

				$("#output").append(OUTPUTS);
			}
		});
	});

});
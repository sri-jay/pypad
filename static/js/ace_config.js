$(document).ready(function(){

	/*Create Editor*/
	var editor = ace.edit("editor");
	editor.setTheme("ace/theme/monokai");
	editor.getSession().setMode("ace/mode/python");
	editor.setFontSize(14);
	editor.getSession().getDocument().insertLines(0,["# Type Code here","print 'Hello, World!'"]);


	var stdout = ace.edit("stdout");
	stdout.setTheme("ace/theme/terminal");
	stdout.getSession().setMode("ace/mode/Plain Text");
	stdout.setFontSize(14);
	stdout.setReadOnly(true);
	var pos = 0;

	function outf(text) { 
	    var mypre = document.getElementById("stdout"); 
	    text = text.split("\n").filter(function(e){return e;});
	    stdout.getSession().getDocument().insertLines(pos,text);
	    pos += text.length;
	}

	function builtinRead(x) {
	    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
	            throw "File not found: '" + x + "'";
	    return Sk.builtinFiles["files"][x];
	}

	$("#run").click(function(){

		var code = editor.getSession().getDocument().getValue();
		var output = $("#stdout");
		Sk.pre = "stdout";
		Sk.canvas = "stdcanvas";

		Sk.configure({output:outf, read:builtinRead}); 
		try {
		  eval(Sk.importMainWithBody("<stdin>",false,code)); 
		}
		catch(e) {
		   alert(e.toString())
		}
	});

	$(function() {
	    $('a[href*=#]:not([href=#])').click(function() {
	        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
	             var target = $(this.hash);
	             target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
	             if (target.length) {
	             $('html,body').animate({
	             scrollTop: target.offset().top,
	             scrollLeft: target.offset().left,
	            }, 250);
	            return false;
	            }
	        }
	    }); 
	});

	$("#toggle_sidebar").click(function (){
		console.log("clicked");
		$('#sidebar').sidebar('toggle')
	}); 


	$("#save").click(function(){
		var code = editor.getSession().getDocument().getAllLines().toString();
		var unique_hash = $("#hash").val();
		var email = $("#email").val();
		var comments = $("#comments").val();

		if(email == "jon@email.net")
		{
			alert("Enter Your Email Id please");
			return;
		}

		$(this).removeClass("blue");
		$(this).addClass("orange");
		$(this).html('<i id="status" class="loading icon"></i>Saving');
	
		console.log(code);
		console.log(unique_hash);
		console.log(email);
		console.log(comments);

		$.ajax({
			url : "http://127.0.0.1:5000/save",
			type : "POST",
			data : {CODE : code,HASH:unique_hash,EMAIL:email,COMMENTS:comments},
			success : function(reply){
				if(reply['STATUS'] != 'TRUE'){
					alert("Failed to enter data to DB");
					$("#save").removeClass("orange");
					$("#save").html('<i id="status" class="checkmark icon"></i>Failed To Save');
					$("#save").addClass("red");
				}
				else
				{
					console.log("Done");
					$("#save").removeClass("orange");
					$("#save").html('<i id="status" class="checkmark icon"></i>Saved');
					$("#save").addClass("green");
				}

			}
		});
	});	
});
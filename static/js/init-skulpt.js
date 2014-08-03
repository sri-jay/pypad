$("#run").click(function(){

	var code = editor.getSession().getDocument().getValue();
	var output = $("#output");
	alert(code);
	Sk.pre = "output";

	Sk.configure({output:outf, read:builtinRead}); 
	try {
	  eval(Sk.importMainWithBody("<stdin>",false,code)); 
	}
	catch(e) {
	   alert(e.toString())
	}
});
if(typeof init === 'undefined'){

	const init = function(){
		var main = document.getElementById('main_s');
		var loc = window.location.hostname;
		if(main === null && loc !== 'www.w3.org'){
			//var bd = document.body.getElementsByTagName("*");
			var bd = document.querySelectorAll( 'body > *' );

			var ele = document.createElement('div');
			ele.setAttribute("id", "main_s");
			ele.setAttribute("class", "main_s");

			var side_nav = document.createElement('div');
			side_nav.setAttribute("id", "sidenav_s");
			side_nav.setAttribute("class", "sidenav_s");



			document.body.innerHTML = '';
			document.body.appendChild(ele);
			document.body.appendChild(side_nav);
			//document.getElementById('main_s').appendChilds(bd)
			for (let item of bd) {
				document.getElementById('main_s').appendChild(item)
			}
			let codigo_nav = '<h1>Limpiar datos</h1><input type="button" id="limpiar" name="limpiar" value="limpiar" /><br><br><h1>Obtener datos auto</h1><input type="button" id="auto" name="auto" value="Obtener" /><br><br><h1>Subir fichero (agregar)</h1><input class="file-upload-button" type="file" /><br><br><h1>Descargar contenido actual</h1><input type="button" id="download" name="download" value="Descragar" /><br><br><h1>Contenido JSON:</h1><p id="tabla_res"></p><br><br><p id="tabla_contenido"></p><script type="text/javascript" src="/JS/agregar_informes.js"></script><script type="text/javascript" src="http://127.0.0.1:5000/tablas.js"></script><script src="/JS/funciones_jquery.js"></script>';
			codigo_nav += "<script>function probando_js(){"+
				"console.log('Entro');}</script>";
			document.getElementById('sidenav_s').innerHTML=codigo_nav;

		}else{
			console.log("Value"+String(main));
		}
		
	}

	init();
}

function probando(){
	console.log('AI');
}


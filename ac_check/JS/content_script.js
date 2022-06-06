if(typeof init === 'undefined'){
	/**
	 * Init es la función que añade la barra lateral a la página web.
	 * 
	 * Solo se añadirá si no está añadida ya y si no estamos en la web de W3C o en las webs de internas de Chrome.
	 * */
	const init = function(){
		var main = document.getElementById('main_s');
		var loc = window.location.hostname;
		if(main === null && loc !== 'www.w3.org' && !loc.startsWith("chrome://")){
			//Primero obtenemos todos los elementos del body.
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
			for (let item of bd) {
				document.getElementById('main_s').appendChild(item)
			}

			//Añadimos el código HTML de la barra lateral
			let codigo_nav = '<img class="clase_logo" src="http://127.0.0.1:5000/logo.png"><br><br>';
			codigo_nav+='<label id="limpiar" name="limpiar" class="boton_secundario_sn">Clean stored data</label><br><br>';
			codigo_nav+='<br><br>'
			codigo_nav+='<label class = "sn_label_for_hyper">Select the websites for automatic data generation</label><br>';
			codigo_nav+= '<label id = "AM_label" class="sn_label_paginas">AccessMonitor</label><input type="checkbox" id="AM_checkbox" checked="checked"><br>';
			codigo_nav+= '<label id = "AC_label" class="sn_label_paginas">AChecker</label><input type="checkbox" id="AC_checkbox" checked="checked"><br>';
			codigo_nav+= '<label id="auto" name="auto" class="boton_principal_sn">Get automatically <br> generated report</label><br><br><br><br>';
			codigo_nav+= '<label class="boton_secundario_sn2"><input id="file-upload-button" type="file" style="display: none;" accept=".json"/>Upload a report</label><br><br><br>';
			codigo_nav+= '<label id="download" name="download" class="boton_principal_sn2">Download report</label><br><br><br>';
			codigo_nav+= '<br><br><p class="titulo_sb">&nbsp;<u>Report content</u>:</p><p id="tabla_res"></label><br><br><p id="tabla_contenido"></p><br><br><br><script type="text/javascript" src="/JS/agregar_informes.js"></script><script type="text/javascript" src="http://127.0.0.1:5000/tablas.js"></script><script src="/JS/funciones_jquery.js"></script>';
			document.getElementById('sidenav_s').innerHTML=codigo_nav;

		}else{
			console.log("Value"+String(main));
		}
		
	}

	init();
}

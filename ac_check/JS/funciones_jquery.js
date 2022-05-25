$(document).ready(function(){

  localStorage.removeItem('ultimo');

  function _x(STR_XPATH) {
    var xresult = document.evaluate(STR_XPATH, document, null, XPathResult.ANY_TYPE, null);
    var xnodes = [];
    var xres;
    while (xres = xresult.iterateNext()) {
        xnodes.push(xres);
    }

    return xnodes;
  }

  function mark_result(text){
      //var txt = '<img src="https://eoidonostiaheo.hezkuntza.net/image/layout_set_logo?img_id=5814476"/image/layout_set_logo?img_id=5814476">';
      let src = "";
      let pos = -1;
      //Primerotenemos que saber si viene de achecker
      let txt = text;
      let posCom = -1;
      let posPun = -1;
      if(txt.includes('...')){
        //Foto
        if(txt.includes('src')){
          pos = txt.search('src');
          txt = txt.substring(pos+5);
          posCom = txt.search('"');
          posPun = txt.search('...');
          if(posCom<posPun){
            txt = txt.substring(0,posCom);  
            src = '//*[@src="'+txt2+'"]';          
          }else{
            txt = txt.substring(0,posPun);
            src = '//img[contains(@src, "'+txt+'")]';
          }
          $(_x(src))[0].setAttribute('style','border: 5px solid red;');
          $(_x(src))[0].scrollIntoView();
          src = $(_x(src))[0].getAttribute('src');
          actualizar_ultimo('//img[contains(@src, "'+src+'")]');
          console.log('forma3')

        }else{  //
          //Primero probamos id
          let pintado = false;
          if(txt.includes('id')){
            pos = txt.search('id');
            txt = txt.substring(pos+4);
            posCom = txt.search('"');
            posPun = txt.indexOf('...');
            if(posCom!== -1 && posCom<posPun){
              //Hemos encontrado id
              pintado = true;
              txt = txt.substring(0,posCom);
              src = '//*[@src="'+txt2+'"]';
              $(_x(src))[0].setAttribute('style','border: 5px solid red;');
              $(_x(src))[0].scrollIntoView();
              actualizar_ultimo(src);            
            }else{
              //No hemos encontrado id, pero probamos si a ver con un poco de suerte solo hay una etiqueta que contenga ese id
              txt = txt.substring(0,posPun-1);
              //Sacamos la etiqueta de la que se trata
              let eti = text.substring(1);
              let posEspa = eti.search(' ');
              eti = eti.substring(0,posEspa);
              let clase_src = '';
              //Comprobamos si tiene una clase valida
              if(text.includes('class')){
                let posCla = text.search('class');
                let clase = text.substring(posCla+7);
                let posCom_ = clase.search('"');
                if(posCom_ !== -1){
                  clase = clase.substring(0,posCom_);
                  clase_src = ' and @class="'+clase+'"';
                }
              }
              let len = $(_x('//'+eti+'[contains(@id, "_com_liferay_port")'+clase_src+']')).length;
              if (len === 1){
                //Solo hay un id que empiece así, nos vale
                pintado = true;
                src = '//'+eti+'[contains(@id, "_com_liferay_port")'+clase_src+']';
                console.log(src);
                $(_x(src))[0].setAttribute('style','border: 5px solid red;');
                $(_x(src))[0].scrollIntoView();
                let id =  $(_x(src))[0].getAttribute('id');
                actualizar_ultimo('//*[@id="'+id+'"]');            
              }

            }
          }
        }
          
      //AccessMonitor
      }else {
        if(txt.includes('src')){
          pos = txt.search('src');
          txt = txt.substring(pos+5);
          pos = txt.search('"');
          txt2= txt.substring(pos+1);
          pos = txt2.search('"');
          txt2= txt2.substring(0,pos);
          src = '//*[@src="'+txt2+'"]';
          console.log(String(src));

          if($(_x(src)).length ){
            $(_x(src))[0].setAttribute('style','border: 5px solid red;');
            $(_x(src))[0].scrollIntoView();
            console.log('HECHO1');
            actualizar_ultimo(src);

          }else{
            pos = txt.search('"');
            txt = txt.substring(0,pos);
            src = '//*[@src="'+txt+'"]';
            $(_x(src))[0].setAttribute('style','border: 5px solid red;');
            $(_x(src))[0].scrollIntoView();
            console.log("Hecho2");
            actualizar_ultimo(src);
         }

          //OJO! PARA https://eoidonostiaheo.hezkuntza.net/documents/5702472/5772458/ikasgunea.jpg/68231b11-6b6f-85ff-381e-0bb7bf62c29e?t=1603723910526 NO funciona
        }else{
            console.log('No incluye src');
        }
    }
  }

  function actualizar_ultimo(src){
    let ultimo = localStorage.getItem('ultimo');
    if(ultimo!==null){
      $(_x(ultimo))[0].setAttribute('style','border: 0px solid red;');
    }
      localStorage.setItem('ultimo',src);

  }


  /*
  $.getScript( "http://127.0.0.1:5000/tablas.js", function( data, textStatus, jqxhr ) {
    console.log( data ); // Data returned
    console.log( textStatus ); // Success
    console.log( jqxhr.status ); // 200
    console.log( "Load was performed." );
  });
  */

  $(document).on('change', '#file-upload-button', function(event) {
    var reader = new FileReader();
    //alert("Entra");
    
    reader.onload = function(event) {
      var jsonT = localStorage.getItem("json");
      var json = JSON.parse(jsonT);
      var jsonObj = JSON.parse(event.target.result);
      
      if (json == null){
        //Caso esta vacio, se pone el que acaba de entrar
        localStorage.setItem("json",JSON.stringify(jsonObj));
      }else{
        //Caso no vacio, se hace merge con el que estaba antes
        merge(json,jsonObj);
        localStorage.setItem("json",JSON.stringify(json));
      }
      alert("JSON cargado correctamente");
      window.location.reload();
    }
  
    reader.readAsText(event.target.files[0]);

  });


  $("#limpiar").click(function(){
      localStorage.removeItem('json');
      localStorage.removeItem('json_resultados');
      localStorage.removeItem("tabla_resultados");
      localStorage.removeItem("tabla_main");
      localStorage.removeItem("ultimo");
      
      alert("Datos limpiados de memoria");
      var origin = window.location.origin; 
      if(origin !=="https://www.w3.org"){
        window.location.reload();
      }
  });

  $(".codigo_analisis").click(function(){
    mark_result($(this).text());
  });


  $(".collapsible_tabla").click(function(){
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });

  $(".collapsible_tabla2").click(function(){
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });

  $(".collapsible_tabla3").click(function(){
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });

  $("#main_table").click(function(){
      var mt = localStorage.getItem('tabla_main');
      localStorage.setItem("tabla_secun",mt); 
      var origin = window.location.origin; 
      if(origin !=="https://www.w3.org"){
        window.location.reload();
      }
  });

  /*
  var json= localStorage.getItem('json_resultados');
  if(json !== null){
    //document.getElementById("estandar_1").addEventListener ("click", probando, false);
  }


  //Usamos wildcard
  $("[id^=estandar_]").click(function(){
    var id = $(this).attr('id');
    id = id.substring(9,);
    id = id.replace('_','.');
    console.log('Id: '+id);
    cambiar_tabla(id);
      /*
      var json_resultados = localStorage.getItem('json_resultados');
      var html_ = "<table class='tabla_contenido' style='width:100%'>";
      html_ += "<tr><th>Standard</th><th>P</th><th>F</th><th>CT</th><th>NP</th><th>NC</th></tr>";
      for (const key in json_resultados) {
          if (key.startsWith("1")){
              html_ += "<tr><td><a href='javascript:cambiar_tabla('"+key+"')'>"+key+"</a></td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>";
          }
      }
      html_ += "</table>";

      document.getElementById('tabla_contenido').innerHTML=html_;
      console.log(html_);
      console.log('Hehco');
      *
  });
  */

  $("#auto").click(function(){
      localStorage.removeItem('json');
      var req = new XMLHttpRequest();
      var url = 'http://127.0.0.1:5000/getJSON/';
      //req.overrideMimeType("application/json");
      req.responseType = 'json';
      var url_local = window.location.href;
      //var nombre = "json_"+url_local;

      req.open('POST', url, true);
      req.onload  = function() {
        var jsonResponse = req.response;
        localStorage.setItem("json",JSON.stringify(jsonResponse));
        alert("Datos insertados automaticamente");
        console.log('update');
        update();
        //Crep que hace el update aun asi porque al cargar la tabla aparece
        //var title = jsonResponse.defineScope.scope.title;
        //Probar poniendo que ponga el JSON imprimido en el parrafo
        //document.getElementById('para').innerHTML='<pre><code>'+JSON.stringify(jsonResponse)+'</code></pre>';
        //download(title+".json", JSON.stringify(jsonResponse));

        var origin = window.location.origin; 
        if(origin !=="https://www.w3.org"){
          window.location.reload();
        }  
      };
      req.setRequestHeader('Content-Type', 'application/json');
      req.send(JSON.stringify({
          'url': url_local
      }));


      document.getElementById('tabla_res').innerHTML='<div class="loader_s"></div>';

  });

  $("#download").click(function(e){
    console.log('Id: '+$(this).attr('id'));
    
      
      var jsonT = localStorage.getItem("json");
      var json = JSON.parse(jsonT);

      var title = json.defineScope.scope.title;
      download(title+".json", JSON.stringify(json));
      var origin = window.location.origin; 
      console.log("Or"+origin);
      
      if(String(origin) !=="https://www.w3.org"){
        window.location.href = "https://www.w3.org/WAI/eval/report-tool/";
      }

  
});
});
$(document).ready(function(){


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
      
      alert("Datos limpiados de memoria");
      var origin = window.location.origin; 
      if(origin !=="https://www.w3.org"){
        window.location.reload();
      }
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
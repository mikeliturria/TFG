$(document).ready(function(){
  /** 
   * Listener para cuando se suba un documento
   */
  $(document).on('change', '#file-upload-button', function(event) {
    var reader = new FileReader();
    
    reader.onload = function(event) {
      var jsonT = localStorage.getItem("json");
      var json = JSON.parse(jsonT);
      var jsonObj = JSON.parse(event.target.result);
      
      if (json == null){
        //Caso esta vacio, se pone el que acaba de entrar
        localStorage.setItem("json",JSON.stringify(jsonObj));
        update();
      }else{
        //Caso no vacio, se hace merge con el que estaba antes
        merge(json,jsonObj);
        localStorage.setItem("json",JSON.stringify(json));
        update();
      }
      alert("JSON successfully loaded!");
      window.location.reload();
    }
  
    reader.readAsText(event.target.files[0]);
  });

  /**
   * Listener para el click del botón de limpiar los datos
   */
  $("#limpiar").click(function(){
      localStorage.removeItem('json');
      localStorage.removeItem('json_resultados');
      localStorage.removeItem("tabla_resultados");
      localStorage.removeItem("tabla_main");
      localStorage.removeItem("ultimo");
      
      alert("Data successfully deleted");
      var origin = window.location.origin; 
      if(origin !=="https://www.w3.org"){
        window.location.reload();
      }
  });


  /**
   * Listener para el click sobre un elemento de los resultados
   */
  $(".collapsible_tabla").click(function(){
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });

  /**
   * Listener para el click sobre un subelemento de los resultados
   */
  $(".collapsible_tabla2").click(function(){
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });

  /**
   * Listener para el click sobre un subsubelemento de los resultados
   */
  $(".collapsible_tabla3").click(function(){
    let foto_ele = $(this).find('img')[0];
    let actual_src = foto_ele.getAttribute('src');
    if(actual_src === "http://127.0.0.1:5000/flecha.png"){
      foto_ele.setAttribute('src',"http://127.0.0.1:5000/flecha_arriba.png");
    }else{
      foto_ele.setAttribute('src',"http://127.0.0.1:5000/flecha.png");
    }
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });

  /**
   * Listener para el click sobre el botón de obtener datos de manera automática
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
        alert("Data successfully saved");
        update();
        var origin = window.location.origin; 
        if(origin !=="https://www.w3.org"){
          window.location.reload();
        }  
      };
      req.setRequestHeader('Content-Type', 'application/json');
      
      req.send(JSON.stringify({
          'url': url_local,
          'AM': $('#AM_checkbox').is(":checked"),
          'AC': $('#AC_checkbox').is(":checked")
      }));
      document.getElementById('tabla_res').innerHTML='<div class="loader_s"></div>';
  });
  /**
   * Listener para el click sobre el botón de descargar informe
   */
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

  /**
   * Listener para el click sobre los links de los analizadores de accesibilidad
   */
  $(".sn_label_paginas").click(function(){
      let url =$(this).attr('id');
      url = url.substring(0,2);
      if(url === "AM"){
         window.open("https://accessmonitor.acessibilidade.gov.pt/", '_blank').focus();
      }
      if(url === "AC"){
         window.open("https://achecker.achecks.ca/checker/index.php", '_blank').focus();
      }
  });
});
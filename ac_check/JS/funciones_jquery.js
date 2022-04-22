$(document).ready(function(){

  $(document).on('change', '.file-upload-button', function(event) {
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
      alert("Datos limpiados de memoria");
      var origin = window.location.origin; 
      if(origin !=="https://www.w3.org"){
        window.location.reload();
      }
  });

  $("#auto").click(function(){
      localStorage.removeItem('json');
      var req = new XMLHttpRequest();
      var url = 'http://127.0.0.1:5000/getJSON/';
      //req.overrideMimeType("application/json");
      req.responseType = 'json';
      var url_local = window.location.href;

      req.open('POST', url, true);
      req.onload  = function() {
        var jsonResponse = req.response;
        localStorage.setItem("json",JSON.stringify(jsonResponse));
        alert("Datos insertados automaticamente");
        update();
        var origin = window.location.origin; 
        if(origin !=="https://www.w3.org"){
          window.location.reload();
        }  
      };
      req.setRequestHeader('Content-Type', 'application/json');
      req.send(JSON.stringify({
          'url': url_local
      }));


      document.getElementById('para').innerHTML='<div class="loader_s"></div>';

  });

  $("#download").click(function(){
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
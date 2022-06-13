$(document).ready(function(){
  /** 
   * Listener for when a document is uploaded
   */
  $(document).on('change', '#file-upload-button', function(event) {
    var reader = new FileReader();
    
    reader.onload = function(event) {
      var jsonT = localStorage.getItem("json");
      var json = JSON.parse(jsonT);
      var jsonObj = JSON.parse(event.target.result);
      
      if (json == null){
        //Case is empty, the one who has just entered gets in.
        localStorage.setItem("json",JSON.stringify(jsonObj));
        update();
      }else{
        //Case not empty, merge with the previous one
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
   * Listener for the clear data button click
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
   * Listener for clicking on an element of the results
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
   * Listener for clicking on a sub-element of the results
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
   * Listener for clicking on a sub-sub-element of the results
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
   * Listener for the click on the button to get data automatically
   */
  $("#auto").click(function(){

    if (!$('#AM_checkbox').is(":checked") && !$('#AC_checkbox').is(":checked")){
      alert('You need to choose at least one analizer');
      return;
    }

    localStorage.removeItem('json');
    var req = new XMLHttpRequest();
    var url = 'http://127.0.0.1:5000/getJSON/';
    req.responseType = 'json';
    var url_local = window.location.href;

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
   * Listener for the click on the download button report
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
   * Listener for clicking on the links of the accessibility analyzers
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
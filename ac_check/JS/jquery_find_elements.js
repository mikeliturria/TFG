$(document).ready(function(){

  /**
  * Listener para el click sobre un código de los resultados
  */
  $(".codigo_analisis").click(function(){
    let alt = $(this).attr('alt');
    let pintado = false;
    if (typeof alt !== 'undefined' && alt !== false) {
      pintado = mark_by_location(alt);  
    }
    if(!pintado){
      mark_result($(this).text());
    }    
  });

  //Cada vez que entremos en una página web borramos el último elemento pintado 
  localStorage.removeItem('ultimo');

  /**
   * La función _x actúa como un selector de XPATH
   * */
  function _x(STR_XPATH) {
    var xresult = document.evaluate(STR_XPATH, document, null, XPathResult.ANY_TYPE, null);
    var xnodes = [];
    var xres;
    while (xres = xresult.iterateNext()) {
        xnodes.push(xres);
    }

    return xnodes;
  }

  //Creamos algunas variables globales
  var src = "";
  var pos = -1;
  var txt = "";
  var posCom = -1;
  var posPun = -1;
  var pintado = false;
  var text = "";
  var txt_for_class= "";

  /**
   *  Pasado por paramétro el código del elemento a buscar, lo busca y lo pinta
   * */
  function mark_result(text_origin){
      src = "";
      pos = -1;
      //Primero tenemos que saber si viene de achecker
      txt = text_origin;
      text = text_origin;
      posCom = -1;
      posPun = -1;
      pintado = false;

      if(txt.includes('...')){
        mt_ac();        
      }else {
        //AccessMonitor
        mt_am(); 
    }
    if(!pintado){
      alert('Element couldn\'t be found');
    }

  }

  /**
   * Pone el último elemento pintado tal y cómo estaba antes de ser pintado
   * */
  function actualizar_ultimo(src){
    let ultimo = localStorage.getItem('ultimo');
    if(ultimo!==null){
      if(ultimo.startsWith("//")){
        eti = ultimo.substring(2,ultimo.indexOf('['));
        if($(_x(ultimo)).length === 1){
          despintar_elemento(eti, $(_x(ultimo))[0]);
        }else{
          let arr_ult = $(_x(ultimo));
          for(let cn = 0; cn< arr_ult.length;cn++){
            despintar_elemento(eti, arr_ult[cn]);
          }
        }
      }else{
        let elemento = document.querySelector(ultimo);
        if(elemento !==null){
          //Significa que al pintar NO se le añadió un div
          despintar_elemento(elemento.tagName.toLowerCase(),elemento);
        }else{
          //Significa que al pintar SI se le añadió un div
          let lastInPa1 = ultimo.lastIndexOf('(');
          let lastInPa2 = ultimo.lastIndexOf(')');
          let num_pos = ultimo.substring(lastInPa1+1,lastInPa2);
          let lastInH = ultimo.lastIndexOf(">");
          let previo = ultimo.substring(0, lastInH);
          let posterior = ultimo.substring(lastInH+1,lastInPa1);
          let location = previo + '>div:nth-child('+num_pos+')>'+posterior+'(1)';
          elemento = document.querySelector(location);
          despintar_elemento(elemento.tagName.toLowerCase(),elemento);
        }
      }
    }
      localStorage.setItem('ultimo',src);
  }

  /** 
   * Despinta el elemento que se le pasa por parámetro
   * */
  function despintar_elemento(eti2, elemento2){
    let padre_html;
    let padre;
    let abuelo;
    let bisabuelo

    switch (true) {
      case (eti2 === 'span' || eti2 === 'b'):
        padre_html = localStorage.getItem('elemento_padre');
        padre = $.parseHTML(padre_html);
        abuelo = elemento2.parentNode.parentNode;
        bisabuelo = abuelo.parentNode;
        bisabuelo.replaceChild(padre[0], abuelo);
        break;
      case (eti2 === 'img'  ||  eti2 === 'body' || eti2 === 'input' || eti2 === 'div' || eti2 === 'href'):
        elemento2.setAttribute('style','border: 0px solid red;');
        break;
      default:
        padre_html = localStorage.getItem('elemento_padre');
        padre = $.parseHTML(padre_html);
        abuelo = elemento2.parentNode.parentNode;
        bisabuelo = abuelo.parentNode;
        bisabuelo.replaceChild(padre[0], abuelo);
        break;

    }
    
  }

  /** 
   * Comprueba si el código del elemento, que ha sido pasado por parámetro, es suficiente
   * para identificar al elemento y poder pintarlo
   */
  function comprobar_pintado(src){
    console.log("Intenta pintar elemento con XPATH: "+src); 
    let eti = src.substring(2,src.indexOf('['));

    if($(_x(src)).length ===1){
      pintado= true;
      actualizar_ultimo(src);
      pintar(eti,$(_x(src))[0]);
    }else{
      //vamos a probar si todos los elementos que encuentra son iguales:
      let arr = [];
      let cont = $(_x(src));

      for (let c = 0; c <cont.length; c++){
        currentValue = cont[c];
        if(!arr.includes(currentValue.outerHTML)){
          arr.push(currentValue.outerHTML);
        }
      }

      if (arr.length === 1){
        pintado = true;
        actualizar_ultimo(src);
        //Son todos iguales, con lo que todos tendrán el mismo error
        for (c = 0; c <cont.length; c++){
          pintar(eti, cont[c]);
        }
      }
    }
  }

  /** 
   * Dado un elemento, lo pinta añadiendole un borde rojo para resaltarlo en la web y hace que
   * la vista de la página se posicione en ese elemento
   */
  function pintar(eti,elemento){
    let ele;
    let padre;
    let html_o;
    let elem_clon;

    switch (true) {
      case (eti === 'span' || eti === 'b'):
          ele = document.createElement('div');
          ele.setAttribute("style",'border: 5px solid red;');
          padre = elemento.parentNode;
          html_o = padre.outerHTML;
          localStorage.setItem('elemento_padre',html_o);
          ele.appendChild(elemento);
          padre.replaceChild(ele,elemento);
          ele.scrollIntoView(); 
        break;
      case (eti === 'img'  || eti === 'div' || eti === 'body' || eti === 'input' || eti === 'href'):
          elemento.setAttribute('style','border: 5px solid red;');
          elemento.scrollIntoView(); 
        break;
      default:
        ele = document.createElement('div');
        ele.setAttribute("style",'border: 5px solid red;');
        padre = elemento.parentNode;
        html_o = padre.outerHTML;
        localStorage.setItem('elemento_padre',html_o);
        elem_clon = elemento.cloneNode(true);
        ele.appendChild(elem_clon);
        padre.replaceChild(ele,elemento);
        ele.scrollIntoView();
        break;
    }
  }

  /** 
   * Mark text: Caso AChecker
   */ 
  function mt_ac(){
     //Foto
    if(txt.includes(' src=') || txt.includes(' src =')){
      mt_ac_src();
    }else if(txt.includes(' href=') || txt.includes(' href =')){
      mt_ac_href();
    }  //
    //Primero probamos id
    txt_for_class = txt;
    if(!pintado && txt.includes(' id=') || txt.includes(' id =')){
      mt_ac_id();
    }
    //Probamos con la clase, solo si no se ha encontrado ya
    if(!pintado && (txt_for_class.includes(' class=') || txt_for_class.includes(' class ='))){
      mt_ac_class();
    }
    if(!pintado && (txt.includes(' name=') || txt.includes(' name ='))){
      mt_ac_name();
    }
  }

  /** 
   * Mark text: Caso AChecker 
   * Caso tiene SRC 
   */
  function mt_ac_src(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    let posCierEti = eti.indexOf('>');
    let posRelativaEtiqueta = eti.search(' src=');
    if(posRelativaEtiqueta === -1){
      posRelativaEtiqueta =eti.indexOf(' src =')+1;
    }
    if(posCierEti ===-1 || posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }
    let pos = text.search(' src=');
    if(pos === -1){
      pos = text.indexOf(' src =') + 1;
    }
    let ele = text.charAt(pos+5);
    pos = pos +5;
    if(ele === " "){
      pos = pos + 1;
      ele = text.charAt(pos);
    }
    
    let txt = text.substring(pos+1);
    let posCom = txt.search(ele);
    let posPun = txt.indexOf('...');

    let ubicacion_arbol;
    let txt2;

    if(posCierEti ===-1 || posRelativaEtiqueta<posCierEti){
      ubicacion_arbol = "./";
    }else{
      ubicacion_arbol = ".//*/"; 
    }

    if(posCom!==-1 && posCom<posPun){
      txt2 = txt.substring(0,posCom);  
      src = '//'+eti+'['+ubicacion_arbol+'@src="'+txt2+'"]';          
    }else{
      txt2 = txt.substring(0,posPun-1);
      src = '//'+eti+'[contains('+ubicacion_arbol+'@src, "'+txt2+'")]';
    }
    comprobar_pintado(src);
  }

  /** 
   * Mark text: Caso AChecker 
   * Caso tiene HREF
   */ 
  function mt_ac_href(){
    //Debería ser un hipervinculo (<a>) pero porseacaso sacamos la etiqueta
    
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    posCierEti = eti.indexOf('>');
    if(posCierEti ===-1 ||posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }

    //PARA SACAR LA ETIQUETA COMPARAR CUAL VIENE ANTES SI ">" O " ", 
    //si viene antes el cierre es que el id y href son de un hijo suyo y no de este
    //asique usar el xpath de arriba

    //Sacamos el href
    let href_pos = txt.indexOf(' href=');
    if(href_pos === -1){
      href_pos =txt.indexOf(' href =')+1;
    }
    let cierre_POS = txt.indexOf('>');

    let ele = text.charAt(href_pos+6);
    href_pos = href_pos + 6;
    if(ele === " "){
      href_pos = href_pos + 1;
      ele = text.charAt(href_pos);
    }


    let href = txt.substring(href_pos+1);
    let posCom = href.search(ele);
    let posPun = href.indexOf('...');
    
    if(cierre_POS !== -1 && href_pos > cierre_POS){
      //Significa que el href es de algún hijo
      if(posCom!==-1 && posCom<posPun){
        href = href.substring(0,posCom);  
        src = '//'+eti+'[.//*/@href="'+href+'"';          
      }else{
        href = href.substring(0,posPun-1);
        src = '//'+eti+'[contains(.//*/@href, "'+href+'")';
      }
    }else {
      if(posCom!==-1 && posCom<posPun){
        href = href.substring(0,posCom);  
        src = '//'+eti+'[@href="'+href+'"';          
      }else{
        href = href.substring(0,posPun-1);
        src = '//'+eti+'[contains(@href, "'+href+'")';
      }
    }

    src = src+']';

    comprobar_pintado(src);
  }

  /** 
   * Mark text: Caso AChecker 
   * Caso tiene ID
   */ 
  function mt_ac_id(){

    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    let posRelativaEtiqueta = eti.search(' id=');
    if(posRelativaEtiqueta === -1){
      posRelativaEtiqueta = eti.search(' id =')+1;
    }
    let posRelativaClase = eti.search(' class=');
    if(posRelativaClase === -1){
      posRelativaClase = eti.search(' class =')+1;
    }
    let posCierEti = eti.indexOf('>');
    if(posCierEti ===-1 || posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }

    let ubicacion_arbol;
    if(posCierEti ===-1 || posRelativaEtiqueta<posCierEti){
      ubicacion_arbol = "./";
    }else{
      ubicacion_arbol = ".//*/"; 
    }

    pos = txt.search(' id=');
    if(pos === -1){
      //Caso sería "src =" 
      pos = txt.search(' id =')+1;
    }
    let ele = txt.charAt(pos+4);
    pos = pos +4;
    if(ele === " "){
      pos = pos + 1;
      ele = txt.charAt(pos);
    }
    txt = txt.substring(pos+1);
    let posCom = txt.search(ele);
    let posPun = txt.indexOf('...');
    if(posCom!== -1 && posCom<posPun){
      //Hemos encontrado id
      //pintado = true;
      txt2 = txt.substring(0,posCom);
      if (src === ""){
        src = '//'+eti+'['+ubicacion_arbol+'@id="'+txt2+'"]';
      }else{
        src = src.substring(0,src.length-1);
        src = src + ' and '+ubicacion_arbol+'@id="'+txt2+'"]';
      }
      
      comprobar_pintado(src);

    }else{
      //No hemos encontrado id, pero probamos si a ver con un poco de suerte solo hay una etiqueta que contenga ese id
      txt2 = txt.substring(0,posPun-1);
      let clase_src = '';
      //Comprobamos si tiene una clase valida
      if(text.includes(' class=') || text.includes(' class =')){
        let posCla = text.search(' class=');
        if(posCla === -1){
          //Caso sería "src =" 
          posCla = text.search(' class =')+1;
        }
        let ele = text.charAt(posCla+7);
        posCla = posCla +7;
        if(ele === " "){
          posCla = posCla + 1;
          ele = text.charAt(posCla);
        }
        let clase = text.substring(posCla+1);
        let posCom_ = clase.search(ele);
        if(posRelativaClase<posCierEti){
          ubicacion_arbol2 = "./";
        }else{
          ubicacion_arbol2 = ".//*/"; 
        }

        if(posCom_ !== -1){
          clase = clase.substring(0,posCom_);
          clase_src = ' and '+ubicacion_arbol2+'@class="'+clase+'"';
        }
      }
      let len = $(_x('//'+eti+'[contains('+ubicacion_arbol+'@id, "'+txt2+'")'+clase_src+']')).length;
      if (len === 1){
        //Solo hay un id que empiece así, nos vale
        src = '//'+eti+'[contains('+ubicacion_arbol+'@id, "'+txt2+'")'+clase_src+']';

        comprobar_pintado(src);
      }
    }
  }

  /** 
   * Mark text: Caso AChecker 
   * Caso tiene CLASS
   */ 
  function mt_ac_class(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    let posCierEti = eti.indexOf('>');
    let posRelativaEtiqueta = eti.search(' class=');
    if(posRelativaEtiqueta === -1){
      posRelativaEtiqueta = eti.search(' class =')+1;
    }
    if(posCierEti ===-1 || posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }

    if(posCierEti ===-1 || posRelativaEtiqueta<posCierEti){
      ubicacion_arbol = "./";
    }else{
      ubicacion_arbol = ".//*/"; 
    }


    txt = txt_for_class;
    let pos = txt.search(' class=');
    let txt2 = "";
    let elem_corte = "";
    if(pos === -1){
      pos = txt.search(' class =')+1;
    }

    elem_corte = txt.charAt(pos+7);
    pos = pos +7;
    if(elem_corte === " "){
      pos = pos + 1;
      elem_corte = txt.charAt(pos);
    }

    txt2 = txt.substring(pos+1);
    let posCom = txt2.search(elem_corte);
    let posPun = txt2.indexOf('...');
    
    if(posCom!== -1 && posCom<posPun){
      //Hemos encontrado class
      txt2 = txt2.substring(0,posCom);
      if (src === ""){
        src = '//'+eti+'['+ubicacion_arbol+'@class="'+txt2+'"]';
      }else{
        src = src.substring(0,src.length-1);
        src = src + ' and '+ubicacion_arbol+'@class="'+txt2+'"]';
      }
      comprobar_pintado(src);
    }else{
      //Tenemos clase parcial
      txt2 = txt2.substring(0,posPun-1);
      if (src === ""){
        src = '//'+eti+'[contains('+ubicacion_arbol+'@class, "'+txt2+'")]';
      }else{
        src = src.substring(0,src.length-1);
        src = src + ' and contains('+ubicacion_arbol+'@class, "'+txt2+'")]';
      }
      comprobar_pintado(src);
    }
  }
  
  /** 
   * Mark text: Caso AChecker 
   * Caso tiene NAME
   */ 
  function mt_ac_name(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    let posCierEti = eti.indexOf('>');
    let posRelativaEtiqueta = eti.search(' name=');
    if(posRelativaEtiqueta === -1){
      posRelativaEtiqueta = eti.search(' name =')+1;
    }
    if(posCierEti ===-1 || posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }

    if(posCierEti ===-1 || posRelativaEtiqueta<posCierEti){
      ubicacion_arbol = "./";
    }else{
      ubicacion_arbol = ".//*/"; 
    }

    txt = txt_for_class;
    let pos = txt.search(' name=');
    let txt2 = "";
    let elem_corte = "";
    if(pos === -1){
      pos = txt.search(' name =')+1;
    }

    elem_corte = txt.charAt(pos+6);
    pos = pos +6;
    if(elem_corte === " "){
      pos = pos + 1;
      elem_corte = txt.charAt(pos);
    }

    txt2 = txt.substring(pos+1);
    let posCom = txt2.search(elem_corte);
    let posPun = txt2.indexOf('...');
    
    if(posCom!== -1 && posCom<posPun){
      //Hemos encontrado class
      txt2 = txt2.substring(0,posCom);
      if (src === ""){
        src = '//'+eti+'['+ubicacion_arbol+'@name="'+txt2+'"]';
      }else{
        src = src.substring(0,src.length-1);
        src = src + ' and '+ubicacion_arbol+'@name="'+txt2+'"]';
      }
      comprobar_pintado(src);
    }else{
      //Tenemos clase parcial
      txt2 = txt2.substring(0,posPun-1);
      if (src === ""){
        src = '//'+eti+'[contains('+ubicacion_arbol+'@name, "'+txt2+'")]';
      }else{
        src = src.substring(0,src.length-1);
        src = src + ' and contains('+ubicacion_arbol+'@name, "'+txt2+'")]';
      }
      comprobar_pintado(src);
    }
  }


  /** 
   * Mark text: Caso AccessMonitor 
   */ 
  function mt_am(){
    if(txt.includes(' src=') || txt.includes(' src =')){
      mt_am_src();

      //OJO! PARA https://eoidonostiaheo.hezkuntza.net/documents/5702472/5772458/ikasgunea.jpg/68231b11-6b6f-85ff-381e-0bb7bf62c29e?t=1603723910526 NO funciona
    }else if(!txt.includes(' id=') && (txt.includes(' href=') || txt.includes(' href ='))){
      mt_am_href();
    }
    if(txt.includes(' id=') || txt.includes(' id =')){
        mt_am_id();
    }else if(txt.includes(' class=') || txt.includes(' class =')){
      mt_am_class();
    }

    if(!pintado && (txt.includes(' name=') || txt.includes(' name ='))){
      mt_am_name();
    }

    //Vemos si todavía no ha sido pintado, si no lo ha sido probamos a ver si tiene nodos hijos puede encontrar
    if(!pintado){
      mt_am_nodos_hijo();
    }
  }

  /** 
   * Mark text: Caso AccessMonitor 
   * Caso tiene SRC
   */ 
  function mt_am_src(){

    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    let posCierEti = eti.indexOf('>');
    let posRelativaEtiqueta = eti.indexOf(' src=');
    if(posRelativaEtiqueta === -1){
      //Caso sería "src =" 
      posRelativaEtiqueta = eti.indexOf(' src =')+1;
    }

    if(posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }
    let ubicacion_arbol =  "";
    if(posRelativaEtiqueta<posCierEti){
      ubicacion_arbol = "./";
    }else{
      ubicacion_arbol = ".//*/"; 
    }

    let pos = text.search(' src=');
    if(pos === -1){
      pos = text.indexOf(' src =')+1;
    }
    let ele = text.charAt(pos+5);
    pos = pos +5;
    if(ele === " "){
      pos = pos + 1;
      ele = text.charAt(pos);
    }


    let txt = text.substring(pos+1);
    pos = txt.search(ele);
    let txt2= txt.substring(0,pos);

    src = '//'+eti+'['+ubicacion_arbol+'@src="'+txt2+'"]';

    let possrc = text.indexOf(' src=');
    let pos1 = 0;
    let pos2 = 0;
    let pos3 = 0;
    if(possrc === -1){
      possrc = text.indexOf(' src =') + 1;
    }
    let ele2 = text.charAt(possrc+5);
    possrc = possrc +5;
    if(ele2 === " "){
      possrc = possrc + 1;
      ele2 = text.charAt(possrc);
    }
    pos1 = text.indexOf(ele2, possrc + 1);
    pos2 = text.indexOf(ele2+' ', possrc + 1);
    pos3 = text.indexOf(ele2+'>', possrc + 1);
    if(((pos2 === -1 || pos2>pos3) && pos3 !== -1 && pos3 !==pos1) ||(pos2 !== -1 && pos2 !==pos1) ){
      pos = text.search(' src=');
      if(pos === -1){
        pos = text.search(' src =')+1;
      }
      let ele2 = text.charAt(pos+5);
      pos = pos +5;
      if(ele2 === " "){
        pos = pos + 1;
        ele = text.charAt(pos);
      }
      let txt3 = text.substring(pos+1);
      pos = txt3.search(ele2);
      txt3= txt3.substring(pos+1);
      pos = txt3.search(ele2);
      txt3= txt3.substring(0,pos);
      src = '//'+eti+'['+ubicacion_arbol+'@src="'+txt3+'"]';
      console.log("SRC2: "+src);
      comprobar_pintado(src);
    }else{
      comprobar_pintado(src);
     }
  }

  /** 
   * Mark text: Caso AccessMonitor 
   * Caso tiene HREF
   */ 
  function mt_am_href(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    let posCierEti = eti.indexOf('>');
    let posRelativaEtiqueta = eti.indexOf(' href=');
    if(posRelativaEtiqueta === -1){
      posRelativaEtiqueta = eti.indexOf(' href =')+1;
    }
    posRelativaEtiqueta2 = eti.indexOf(' class=');
    if(posRelativaEtiqueta2 === -1){
      posRelativaEtiqueta2 = eti.indexOf(' class =')+1;
    }

    if(posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }


    if(posRelativaEtiqueta<posCierEti){
      ubicacion_arbol = "./";
    }else{
      ubicacion_arbol = ".//*/"; 
    }

    //Sacamos el href
    let href_pos = txt.indexOf(' href=');
    if(href_pos === -1){
      href_pos = txt.indexOf(' href =')+1;
    }

    let ele = txt.charAt(href_pos+6);
    href_pos = href_pos +6;
    if(ele === " "){
      href_pos = href_pos + 1;
      ele = txt.charAt(href_pos);
    }

    href = txt.substring(href_pos+1);
    posCom = href.search(ele);
    href = href.substring(0,posCom);  
    src = '//'+eti+'['+ubicacion_arbol+'@href="'+href+'"';    

    //Probamos si basta con el href:
    if($(_x(src+']')).length === 1){
      comprobar_pintado(src+']');
    }else{
      //Probamos si tiene algo mas que podamos usar para identificar (class)
      if(txt.includes(' class=')){

        if(posRelativaEtiqueta2<posCierEti){
          ubicacion_arbol2 = "./";
        }else{
          ubicacion_arbol2 = ".//*/"; 
        }

        pclase = txt.indexOf(' class=');
        if(pclase === -1){
          pclase = txt.indexOf(' class =')+1;
        }
        let ele2 = txt.charAt(pclase+7);
        pclase = pclase +7;
        if(ele2 === " "){
          pclase = pclase + 1;
          ele2 = txt.charAt(pclase);
        }

        clase = txt.substring(pclase+1);
        posCom = clase.indexOf(ele2);
        clase = clase.substring(0,posCom);
        src = src + ' and '+ubicacion_arbol2+'@class = "'+clase+'"]';

        comprobar_pintado(src);
      }

      if(!pintado){
        //Vamos a sacar ahora el contenido del texto de <a>
        posCier = txt.indexOf(">",posRelativaEtiqueta);
        texto_contenido = txt.substring(posCier+1);
        posCA = texto_contenido.indexOf("</a>");
        texto_contenido = texto_contenido.substring(0,posCA);
        //Normalizamos espacios
        texto_contenido = texto_contenido.replace(/\s+/g, ' ')
        //src= src+'and text()="'+texto_contenido+'"]';
        src= src+' and contains(.//*/text(),"'+texto_contenido+'")]';
        comprobar_pintado(src);
      }
    }
  }

  /** 
   * Mark text: Caso AccessMonitor 
   * Caso tiene ID
   */ 
  function mt_am_id(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    posCierEti = eti.indexOf('>');
    posRelativaEtiqueta = eti.indexOf(' id=');
    if(posRelativaEtiqueta === -1){
      posRelativaEtiqueta = eti.indexOf(' id =')+1;
    }

    if(posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }

    if(posRelativaEtiqueta<posCierEti){
      ubicacion_arbol = "./";
    }else{
      ubicacion_arbol = ".//*/"; 
    }

    pos = txt.search(' id=');
    if(pos === -1){
      pos = txt.indexOf(' id =')+1;
    }

    let ele = txt.charAt(pos+4);
    pos = pos +4;
    if(ele === " "){
      pos = pos + 1;
      ele = txt.charAt(pos);
    }
    txt2 = txt.substring(pos+1);
    posCom = txt2.search(ele);
    //Hemos encontrado id
    pintado = true;
    txt2 = txt2.substring(0,posCom);
    src = '//'+eti+'['+ubicacion_arbol+'@id="'+txt2+'"]';

    comprobar_pintado(src);
  }

  /** 
   * Mark text: Caso AccessMonitor 
   * Caso tiene CLASS
   */ 
  function mt_am_class(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    let posCierEti = eti.indexOf('>');
    let posRelativaEtiqueta = eti.indexOf('class=');
    if(posRelativaEtiqueta === -1){
      posRelativaEtiqueta = eti.indexOf(' class =')+1;
    }

    if(posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }

    if(posRelativaEtiqueta<posCierEti){
      ubicacion_arbol = "./";
    }else{
      ubicacion_arbol = ".//*/"; 
    }

    pos = txt.search(' class=');
    if(pos === -1){
      pos = txt.indexOf(' class =')+1;
    }

    let ele = txt.charAt(pos+7);
    pos = pos +7;
    if(ele === " "){
      pos = pos + 1;
      ele = txt.charAt(pos);
    }

    txt2 = txt.substring(pos+1);
    posCom = txt2.search(ele);

    //Hemos encontrado class
    txt2 = txt2.substring(0,posCom);
    if (src === ""){
      src = '//'+eti+'['+ubicacion_arbol+'@class="'+txt2+'"]';
    }else{
      src = src.substring(0,src.length-1);
      src = src + ' and '+ubicacion_arbol+'@class="'+txt2+'"]';
    }
    
    comprobar_pintado(src);
  }

  /** 
   * Mark text: Caso AccessMonitor 
   * Caso tiene NAME
   */ 
  function mt_am_name(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    let posCierEti = eti.indexOf('>');
    let posRelativaEtiqueta = eti.indexOf('name=');
    if(posRelativaEtiqueta === -1){
      posRelativaEtiqueta = eti.indexOf(' name =')+1;
    }

    if(posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }

    if(posRelativaEtiqueta<posCierEti){
      ubicacion_arbol = "./";
    }else{
      ubicacion_arbol = ".//*/"; 
    }


    pos = txt.search(' name=');
    if(pos === -1){
      pos = txt.indexOf(' name =')+1;
    }

    let ele = txt.charAt(pos+6);
    pos = pos +6;
    if(ele === " "){
      pos = pos + 1;
      ele = txt.charAt(pos);
    }

    txt2 = txt.substring(pos+1);
    posCom = txt2.search(ele);
    
    //Hemos encontrado class
    txt2 = txt2.substring(0,posCom);
    if (src === ""){
      src = '//'+eti+'['+ubicacion_arbol+'@name="'+txt2+'"]';
    }else{
      src = src.substring(0,src.length-1);
      src = src + ' and '+ubicacion_arbol+'@name="'+txt2+'"]';
    }
    comprobar_pintado(src);
  }

  /** 
   * Mark text: Caso AccessMonitor 
   * Comprobamos si tiene nodos hijo que podamos usar para localizar el elemento
   */ 
  function mt_am_nodos_hijo(){
    //Primero habrá que comprobar si el src no está vacio
    if (src === ""){
      let eti = text.substring(1);
      let posEspa = eti.search(' ');
      posCierEti = eti.indexOf('>');
      if(posEspa < posCierEti){
        eti = eti.substring(0,posEspa); 
      }else{
        eti = eti.substring(0,posCierEti); 
      }
      src = src +'//'+eti+'[';

      //Probamos si hay algún atributo que podamos usar
      if(posEspa < posCierEti){
        posIgualRel = text.search('='); 
        //Buscamos la ultima posicion del espacio antes que el igual
        string_busqueda = text.substring(0,posIgualRel);
        posEspa2 = string_busqueda.lastIndexOf(' ');
        tipoComilla = text.charAt(posIgualRel+1);
        posComillaCierre = text.indexOf(tipoComilla, posIgualRel+2)
        atributo = text.substring(posEspa2+1);
        posIgual = atributo.indexOf('=');
        atributo = atributo.substring(0,posIgual);
        contenido_atributo = text.substring(posIgualRel+2,posComillaCierre);
        src = src + './@'+atributo+'="'+contenido_atributo+'"]';
      }
    }
    //Tenemos en src el último src que se probó, vamos a comprobar hijos
    let cierreElem = text.indexOf("</",1);
    let abrirElem = text.indexOf("<",1);
    //Si la apertura va antes que el cierre es que hay un elemento dentro
    if(cierreElem !== -1 && abrirElem !== -1 && cierreElem !== abrirElem){
      let nuevoElem = text.substring(abrirElem+1);
      let cier = nuevoElem.indexOf('>');
      espa = nuevoElem.indexOf(' ');
      //Lo que venga antes será la etiqueta
      let eti2 ="";
      if(espa !== -1 && espa<cier){
        eti2 = nuevoElem.substring(0,espa); 
      }else{
        eti2 = nuevoElem.substring(0,cier);
      }
      //Primero añadimos la etiqueta al src 
      src = src.substring(0,src.length-1);
      src = src+" and ./"+eti2;
      //Vemos si tiene un hijo que tenga texto:
      if($(_x(src+'/text()]')).length >0){
        let texto_dentro = "";
        ncier = nuevoElem.indexOf("</");
        if(espa !== -1 && espa<cier){
          texto_dentro = nuevoElem.substring(espa+1,ncier); 
        }else{
          texto_dentro = nuevoElem.substring(cier+1,ncier);
        }
        //Lo añadimos al src y probamos de nuevo
        src = src+'[contains(text(),"'+texto_dentro+'")]]';
        comprobar_pintado(src);
      }

    }else{
      //Sabemos que no tiene hijos, probamos si tiene texto
      posCier = text.indexOf(">");
      posAper = text.indexOf("<",1);
      if(posAper !== -1){
        mensaje = text.substring(posCier+1, posAper);
        src = src.substring(0,src.length-1);
        src = src+' and ./text()="'+mensaje+'"]';
      }
      comprobar_pintado(src);
    }
  }

  /** 
   * Pintamos el elemento usando su posición absoluta
   */
  function mark_by_location(alt){
    //Primero checkeamos si tenemos la location:
    //Hay que sustituir lo que va antes del segundo ">" porque al crear la barra lateral movemos los elementos
    let pos_desp_html = alt.indexOf(">",6);
    alt = "html > body:nth-child(2)>div:nth-child(1)"+alt.substring(pos_desp_html);
    let elemento = document.querySelector(alt);
    console.log("Prueba location: "+alt);
    if(elemento ===null){
      //Probamos si es el elemento que esta pintado justo ahora
      let lastInPa1 = alt.lastIndexOf('(');
      let lastInPa2 = alt.lastIndexOf(')');
      let num_pos = alt.substring(lastInPa1+1,lastInPa2);
      let lastInH = alt.lastIndexOf(">");
      let previo = alt.substring(0, lastInH);
      let posterior = alt.substring(lastInH+1,lastInPa1);
      let location = previo + '>div:nth-child('+num_pos+')>'+posterior+'(1)';
      elemento = document.querySelector(location);
      if(elemento === null){
        return false;
      }else{
        actualizar_ultimo(alt);
        elemento = document.querySelector(alt);
        pintar(elemento.tagName.toLowerCase(),elemento);
        return true;
      }
    }else{
      actualizar_ultimo(alt);
      elemento = document.querySelector(alt);
      pintar(elemento.tagName.toLowerCase(),elemento);
      return true;
    }
  }
});
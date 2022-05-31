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

  var src = "";
  var pos = -1;
  //Primerotenemos que saber si viene de achecker
  var txt = "";
  var posCom = -1;
  var posPun = -1;
  var pintado = false;
  var text = "";
  var txt_for_class= "";

  function mark_result(text_origin){
      //var txt = '<img src="https://eoidonostiaheo.hezkuntza.net/image/layout_set_logo?img_id=5814476"/image/layout_set_logo?img_id=5814476">';
      src = "";
      pos = -1;
      //Primerotenemos que saber si viene de achecker
      txt = text_origin;
      text = text_origin;
      posCom = -1;
      posPun = -1;
      pintado = false;

      if(txt.includes('...')){
        mt_ac();        
      //AccessMonitor
      }else {
        mt_am(); 
    }
    if(!pintado){
      alert('Element couldn\'t be found');
    }

  }

  function actualizar_ultimo(src){
    let ultimo = localStorage.getItem('ultimo');
    if(ultimo!==null){
      eti = ultimo.substring(2,ultimo.indexOf('['));
      if($(_x(ultimo)).length === 1){
        despintar_elemento(eti, $(_x(ultimo))[0]);
      }else{
        let arr_ult = $(_x(ultimo));
        for(let cn = 0; cn< arr_ult.length;cn++){
          despintar_elemento(eti, arr_ult[cn]);
        }
      }
      //$(_x(ultimo))[0].setAttribute('style','border: 0px solid red;');
    }
      localStorage.setItem('ultimo',src);

  }


  function despintar_elemento(eti2, elemento){
    let padre_html;
    let padre;
    let abuelo;
    let bisabuelo

    switch (true) {
      case (eti2 === 'span' || eti2 === 'b'):
        padre_html = localStorage.getItem('elemento_padre');
        padre = $.parseHTML(padre_html);
        abuelo = elemento.parentNode.parentNode;
        bisabuelo = abuelo.parentNode;
        bisabuelo.replaceChild(padre[0], abuelo);
        /*
        padreArtificial = elemento.parentNode;
        padreOrig = elemento.parentNode.parentNode;
        padreOrig.appendChild(elemento);
        padreOrig.removeChild(padreArtificial);
        */
        break;
      case (eti2 === 'img'  ||  eti === 'body' || eti === 'input' || eti2 === 'div' || eti2 === 'href'):
        elemento.setAttribute('style','border: 0px solid red;');
        break;
      default:
        /*
        padreArtificial = elemento.parentNode;
        padreOrig = elemento.parentNode.parentNode;
        padreOrig.appendChild(elemento);
        padreOrig.removeChild(padreArtificial);
        */
        padre_html = localStorage.getItem('elemento_padre');
        padre = $.parseHTML(padre_html);
        abuelo = elemento.parentNode.parentNode;
        bisabuelo = abuelo.parentNode;
        bisabuelo.replaceChild(padre[0], abuelo);
        break;

    }
    
  }

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
          padre.appendChild(ele);
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
        //padre.appendChild(ele);
        padre.replaceChild(ele,elemento);
        ele.scrollIntoView();
        break;

    }
  }


  function mt_ac(){
     //Foto
    if(txt.includes(' src=')){
      mt_ac_src();
    }else if(txt.includes(' href=')){
      mt_ac_href();
    }else{  //
      //Primero probamos id
      txt_for_class = txt;
      if(txt.includes(' id=')){
        mt_ac_id();
      }
      //Probamos con la clase, solo si no se ha encontrado ya
      if(!pintado && txt_for_class.includes(' class=')){
        mt_ac_class();
      }
    }
  }

  function mt_ac_src(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    let posCierEti = eti.indexOf('>');
    let posRelativaEtiqueta = eti.search(' src=');
    if(posCierEti ===-1 || posEspa < posCierEti){
      eti = eti.substring(0,posEspa); 
    }else{
      eti = eti.substring(0,posCierEti); 
    }
    let pos = text.search(' src=');
    txt = txt.substring(pos+6);
    let posCom = txt.search('"');
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
    

    //eti = 'a';

    //ESTE ETI SE CARGA PROGRAMA!!!
    //La solucion seria la de abajo
    //$x('//b[contains(.//*/@href, "https://eoidonostiaheo.hezkuntza.net/documents/5702472/6347984/DISTRIBUCIONAULASL-M.p")]')[0];
    
    //PARA SACAR LA ETIQUETA COMPARAR CUAL VIENE ANTES SI ">" O " ", 
    //si viene antes el cierre es que el id y href son de un hijo suyo y no de este
    //asique usar el xpath de arriba

    //Sacamos el href
    let href_pos = txt.indexOf(' href=');
    cierre_POS = txt.indexOf('>');
    href = txt.substring(href_pos+7);
    posCom = href.search('"');
    posPun = href.indexOf('...');
    
    if(href_pos > cierre_POS){
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
    /*
    //Vamos a sacar ahora si es posible el contenido del texto de <a>
    //Primero habrá que saber si ha entrado todo a
    posCier = txt.indexOf(">");
    if(posCier !== -1){
      //Hay cierre
      //Buscamos si ha entrado completo
      texto_contenido = txt.substring(posCier+1);
      posCA = texto_contenido.indexOf("</a>");
      posPun = texto_contenido.indexOf("...");
      if(posCA !== -1){
        texto_contenido = texto_contenido.substring(0,posCA);
        src= src+'and text()="'+texto_contenido+'"]';
      }else{
        texto_contenido = texto_contenido.substring(0,posPun);
        src= src+'and contains(text(),"'+texto_contenido+'")]';
      }
    }else{
      src = src+']';
    }*/
    src = src+']';
    /*
    if($(_x(src)).length === 1){
      pintado = true;
      actualizar_ultimo(src);
      $(_x(src))[0].setAttribute('style','border: 5px solid red;');
      $(_x(src))[0].scrollIntoView();
    }*/
    comprobar_pintado(src);
  }

  function mt_ac_id(){

    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    posRelativaEtiqueta = eti.search(' id=');
    posRelativaClase = eti.search(' class=');
    posCierEti = eti.indexOf('>');
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

    pos = txt.search(' id=');
    txt = txt.substring(pos+5);
    posCom = txt.search('"');
    posPun = txt.indexOf('...');
    if(posCom!== -1 && posCom<posPun){
      //Hemos encontrado id
      //pintado = true;
      txt2 = txt.substring(0,posCom);
      src = '//'+eti+'['+ubicacion_arbol+'@id="'+txt2+'"]';
      //actualizar_ultimo(src);            
      //$(_x(src))[0].setAttribute('style','border: 5px solid red;');
      //$(_x(src))[0].scrollIntoView();
      comprobar_pintado(src);

    }else{
      //No hemos encontrado id, pero probamos si a ver con un poco de suerte solo hay una etiqueta que contenga ese id
      txt2 = txt.substring(0,posPun-1);
      //Sacamos la etiqueta de la que se trata
      //let eti = text.substring(1);
      //let posEspa = eti.search(' ');
      //eti = eti.substring(0,posEspa);
      let clase_src = '';
      //Comprobamos si tiene una clase valida
      if(text.includes(' class=')){
        let posCla = text.search(' class=');
        let clase = text.substring(posCla+8);
        let posCom_ = clase.search('"');
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
        //pintado = true;
        src = '//'+eti+'[contains('+ubicacion_arbol+'@id, "'+txt2+'")'+clase_src+']';
        //let id =  $(_x(src))[0].getAttribute('id');
        /*
        actualizar_ultimo('//*[@id="'+id+'"]');            
        $(_x(src))[0].setAttribute('style','border: 5px solid red;');
        $(_x(src))[0].scrollIntoView();
        */
        comprobar_pintado(src);

      }
  
    }
  }

  function mt_ac_class(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    posCierEti = eti.indexOf('>');
    posRelativaEtiqueta = eti.search(' class=');
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
    pos = txt.search(' class=');
    txt2 = txt.substring(pos+8);
    posCom = txt2.search('"');
    posPun = txt2.indexOf('...');
    
    if(posCom!== -1 && posCom<posPun){
      //Hemos encontrado class
      txt2 = txt2.substring(0,posCom);
      src = '//'+eti+'['+ubicacion_arbol+'@class="'+txt2+'"]';
      if($(_x(src)).length === 1){
        /*
        pintado = true;
        actualizar_ultimo(src);
        $(_x(src))[0].setAttribute('style','border: 5px solid red;');
        $(_x(src))[0].scrollIntoView();
        */
        comprobar_pintado(src);
      }else{
        //Tenemos clase parcial
        txt2 = txt.substring(0,posPun-1);
        src = '//'+eti+'[contains('+ubicacion_arbol+'@class, "'+txt2+'")]';
        comprobar_pintado(src);
        /*
        if($(_x(src)).length === 1){

            pintado = true;
            let class_entero =  $(_x(src))[0].getAttribute('class');
            actualizar_ultimo('//'+eti+'[@class="'+class_entero+'"]');
            $(_x(src))[0].setAttribute('style','border: 5px solid red;');
            $(_x(src))[0].scrollIntoView();
          }
          */
      }
    }
  }

  function mt_am(){
    if(txt.includes(' src=')){
      mt_am_src();

      //OJO! PARA https://eoidonostiaheo.hezkuntza.net/documents/5702472/5772458/ikasgunea.jpg/68231b11-6b6f-85ff-381e-0bb7bf62c29e?t=1603723910526 NO funciona
    }else if(!txt.includes(' id=') && txt.includes(' href=')){
      mt_am_href();
    }else{
      if(txt.includes(' id=')){
        mt_am_id();
      }else if(txt.includes(' class=')){
        mt_am_class();
      }
    }

    //Vemos si todavía no ha sido pintado, si no lo ha sido probamos a ver si tiene nodos hijos puede encontrar
    if(!pintado){
      mt_am_nodos_hijo();
    }
  }

  function mt_am_src(){

    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    posCierEti = eti.indexOf('>');
    posRelativaEtiqueta = eti.indexOf(' src=');
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

    pos = txt.search(' src=');
    txt = txt.substring(pos+6);
    console.log('TT '+txt);
    pos = txt.search('"');
    txt2= txt.substring(0,pos);
    console.log('TT2 '+txt2);

    src = '//'+eti+'['+ubicacion_arbol+'@src="'+txt2+'"]';
    console.log('SRC1 '+src);

    //A veces accessmonitor falla y saca src dobles, comprobamos si puede ser el caso
    /*
    let posJPG1 = text.indexOf('.jpg');
    let posJPG2 = text.indexOf('.jpg',posJPG1+1);
    let posCOM1 = text.indexOf('="',posJPG1);
    let posPNG1 = text.indexOf('.png');
    let posPNG2 = text.indexOf('.png',posPNG1+1);
    let posCOM2 = text.indexOf('="',posPNG1);

    //&&  $(_x(src)).length ===1 )
    if((posJPG1 === -1 && posPNG1 === -1) ||(posJPG2!== -1 && posCOM1 !==-1 && posJPG2>posCOM1 ) || (posPNG2 !==-1 && posCOM2 !==-1  && posPNG2>posCOM2)){
    */
    let possrc = text.indexOf(' src=');
    let ele = text.charAt(possrc+5);
    let pos1 = text.indexOf(ele, possrc+6);
    let pos2 = text.indexOf(ele+' ', possrc+6);
    let pos3 = text.indexOf(ele+'>', possrc+6);
    if(((pos2 === -1 || pos2>pos3) && pos3 !== -1 && pos3 !==pos1) ||(pos2 !== -1 && pos2 !==pos1) ){
      pos = text.search(' src=');
      txt3 = text.substring(pos+6);
      pos = txt3.search(ele);
      txt3= txt3.substring(pos+1);
      pos = txt3.search(ele);
      txt3= txt3.substring(0,pos);
      src = '//'+eti+'['+ubicacion_arbol+'@src="'+txt3+'"]';
      console.log("SRC2: "+src);
      comprobar_pintado(src);
    }else{
      /*
      pos = text.search(' src=');
      txt3 = text.substring(pos+5);
      pos = txt3.search('"');
      txt3= txt3.substring(pos+1);
      pos = txt3.search('"');
      txt3= txt3.substring(0,pos);
      src = '//'+eti+'['+ubicacion_arbol+'@src="'+txt3+'"]';
      console.log("SRC2: "+src);
      */
      comprobar_pintado(src);

        
        /*
        if($(_x(src)).length ===1 ){
          pintado = true;
          actualizar_ultimo(src);
          $(_x(src))[0].setAttribute('style','border: 5px solid red;');
          $(_x(src))[0].scrollIntoView();
          console.log("Hecho2");
        }
        */
     }
  }

  function mt_am_href(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    posCierEti = eti.indexOf('>');
    posRelativaEtiqueta = eti.indexOf(' href=');
    posRelativaEtiqueta2 = eti.indexOf(' class=');
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
    href = txt.substring(href_pos+7);
    posCom = href.search('"');
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
        clase = txt.substring(pclase+8);
        posCom = clase.indexOf('"');
        clase = clase.substring(0,posCom);
        src = src + ' and '+ubicacion_arbol2+'@class = "'+clase+'"]';
        /*
        if($(_x(src)).length === 1){
          pintado = true;
          actualizar_ultimo(src);
          $(_x(src))[0].setAttribute('style','border: 5px solid red;');
          $(_x(src))[0].scrollIntoView();
        }
        */
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
        /*
        if($(_x(src)).length === 1){
          pintado = true;
          actualizar_ultimo(src);
          $(_x(src))[0].setAttribute('style','border: 5px solid red;');
          $(_x(src))[0].scrollIntoView();
        }
        */
      }
    }
  }

  function mt_am_id(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    posCierEti = eti.indexOf('>');
    posRelativaEtiqueta = eti.indexOf(' id=');
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
    txt2 = txt.substring(pos+5);
    posCom = txt2.search('"');
    //Hemos encontrado id
    pintado = true;
    txt2 = txt2.substring(0,posCom);
    src = '//'+eti+'['+ubicacion_arbol+'@id="'+txt2+'"]';
    /*
    actualizar_ultimo(src);  
    $(_x(src))[0].setAttribute('style','border: 5px solid red;');
    $(_x(src))[0].scrollIntoView();
    */
    comprobar_pintado(src);
  }

  function mt_am_class(){
    let eti = text.substring(1);
    let posEspa = eti.search(' ');
    posCierEti = eti.indexOf('>');
    posRelativaEtiqueta = eti.indexOf('class=');
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
    txt2 = txt.substring(pos+8);
    posCom = txt2.search('"');

    
    //Hemos encontrado class
    txt2 = txt2.substring(0,posCom);
    src = '//'+eti+'['+ubicacion_arbol+'@class="'+txt2+'"]';
    /*
    if($(_x(src)).length ===1){
      pintado = true;
      actualizar_ultimo(src); 
      $(_x(src))[0].setAttribute('style','border: 5px solid red;');
      $(_x(src))[0].scrollIntoView();
    }
    */
    comprobar_pintado(src);
  }

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
        /*
        //No puedo haber ni class ni id porque sino lo hubiera encontrado el anterior
        if(nuevoElem.includes('id')){
          pos = nuevoElem.search('id');
          nuevoid = nuevoElem.substring(pos+4);
          posCom = nuevoid.search('"');
          nuevoid = nuevoid.substring(0,posCom);

        }
        */
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
        /*
        if($(_x(src)).length ===1){
          //Encontrado
          pintado = true;
          actualizar_ultimo(src);  
          $(_x(src))[0].setAttribute('style','border: 5px solid red;');
          $(_x(src))[0].scrollIntoView();
        }
        */
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
    //this.classList.toggle("active");
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
        alert("Data successfully saved");
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
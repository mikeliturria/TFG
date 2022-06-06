/**
 * Función que añade el listener para el click sobre el icono de la extensión.
 * 
 * Ese listener se encarga de encender y apagar la extensión. Se cambia el logo de
 * color para saber el estado de la extensión.
 * */ 
function main_bk(){
  try{
    chrome.runtime.onInstalled.addListener(function() {
        chrome.storage.sync.set({'toggle':true});
    });
    chrome.action.onClicked.addListener((tab) => {
      chrome.storage.sync.get(['toggle'], function(result) {
        var toggle = result.toggle;
        if(!toggle){
          chrome.storage.sync.set({'toggle':true});
          chrome.action.setIcon({path: "/images/icon16.png"});
        }else{
          chrome.storage.sync.set({'toggle':false});
          chrome.action.setIcon({path: "/images/icon16G.png"});
        }
      });

      chrome.scripting.executeScript({
        target: {tabId: tab.id},
        files: ['/JS/reload.js']
      });
  });


  //ON page change
  chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    chrome.storage.sync.get(['toggle'], function(result) {
      var toggle = result.toggle;
      if(toggle){
        chrome.action.setIcon({path: "/images/icon16.png"});
      }else{
        chrome.action.setIcon({path: "/images/icon16G.png"});
      }
      if(changeInfo.status == 'complete' && toggle){
        chrome.action.setIcon({path: "/images/icon16.png"});
        chrome.scripting.executeScript({
          files: ['/JS/content_script.js','/JS/agregar_informes.js','/JS/jquery_listeners.js','/JS/jquery_find_elements.js'],
          target: {tabId: tab.id}
        });
      }
    });
  });    
  
}catch(e){
  console.log(e);
}
}

main_bk();

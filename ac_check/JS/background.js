try{

  //var toggle = true;

  chrome.runtime.onInstalled.addListener(function() {
      chrome.storage.sync.set({'toggle':true});
  });
  chrome.action.onClicked.addListener((tab) => {
    /*
    toggle = !toggle;
    if(toggle){
      chrome.action.setIcon({path: "/images/icon16.png"});
    }
    else{
      chrome.action.setIcon({path: "/images/icon16G.png"});
    }
    */
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
      files: ['/JS/content.js']
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
      //if (changeInfo.url) {
        chrome.action.setIcon({path: "/images/icon16.png"});
        chrome.scripting.executeScript({
          files: ['/JS/content_script.js','/JS/agregar_informes.js','/JS/funciones_jquery.js'],
          target: {tabId: tab.id}
        });
      //}
      }
    });
  });    
  
}catch(e){
  console.log(e);
}

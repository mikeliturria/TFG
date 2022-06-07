/**
 * Function that adds the listener for the click on the icon of the extension.
 * 
 * This listener is in charge of turning the extension on and off. It changes the logo's
 * colour to know the status of the extension.
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

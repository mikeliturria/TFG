
function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

//usage:

/*
readTextFile("../JSON/AA1.json", function(text){
    var data_json = JSON.parse(text);   
    pasarela(data_json);
});
*/
main();
//Pasamos a tener todo en memoria local
function main(){
    //Usar local storage:
    //https://platzi.com/blog/local-storage-html5/
    //Subir Fichero:
    //https://stackoverflow.com/questions/5587973/javascript-upload-file

    var jsonT = localStorage.getItem("json");
    var jsonTabla = localStorage.getItem("tabla_resultados");
    var json = JSON.parse(jsonT);
    var texto = "";

    if (json == null){
        texto = "<div style='text-align:center'><text style='font-size:14px'>Sin datos</text></div>";
    }else{
        //texto = "<pre><code>"+JSON.stringify(json, null, 4)+"</pre></code>";
        texto = jsonTabla;
    }

    //Se esta guardando mal el JSON, mejor pasarlo a texto y guardar el texto?

    //console.log("COntenido: "+texto);
    var loc = window.location.hostname;

    var main = localStorage.getItem("tabla_main");
    var texto2 = "";

    if (main == null){
        texto2 = "<text style='font-size:26px'></text>";
    }else{
        //texto = "<pre><code>"+JSON.stringify(json, null, 4)+"</pre></code>";
        texto2 = main;
    }
    if(loc !== 'www.w3.org'){
        document.getElementById("tabla_res").innerHTML = texto;
        document.getElementById('tabla_contenido').innerHTML=texto2;

    }


}


function pasarela(data_json){ 
    readTextFile("../JSON/AA2.json", function(text){
        var data_json2 = JSON.parse(text);   
        main(data_json,data_json2);
    });
    //Para saber si esta https://stackoverflow.com/questions/40438851/use-javascript-to-check-if-json-object-contain-value
}
function merge(json,json1){
    //Primero hacemos un control de que se cumplen las condiciones para el merge:

    //Usar local storage:
    //https://platzi.com/blog/local-storage-html5/
    //Subir Fichero:
    //https://stackoverflow.com/questions/5587973/javascript-upload-file

    //Tienen que ser ambos AA:
    var tipo_1 = json.defineScope.conformanceTarget;
    var tipo_2 = json1.defineScope.conformanceTarget;

    if(tipo_1 !=="AA" || tipo_2 !== "AA"){
        alert("No se pueden juntar, uno de los dos no es de tipo AA");
        return;
    }
    if(json.defineScope.scope.title !== json1.defineScope.scope.title){
        alert("No se pueden juntar, los nombres de las webs no coinciden");
        return; 
    }


    /*
    var json = crear_JSON_limpio();
    merge_reportFindings(json,JSON1);
    merge_reportFindings(json,JSON2);

    merge_audit_samples(json,JSON1);
    merge_audit_samples(json,JSON2);
    */
    merge_reportFindings(json,json1);
    merge_audit_samples(json,json1);

    //Para hacer todo sombra menos el boton donde subir el informe:
    //Crep que la buena es la segunda opcion, el de hover this box
    //https://stackoverflow.com/questions/48184793/how-to-darken-background-except-of-one-element 

    //Otra opción (mejor la de arriba)
    //https://stackoverflow.com/questions/8644428/how-to-highlight-text-using-javascript




    //var para= document.getElementById("para");
    //para.innerHTML = "<pre><code>"+JSON.stringify(json.auditSample,null,4)+"</pre></code>";

    //Para descargar, descomentar lo de abajo
    //download("informe.json",JSON.stringify(json));
}

function crear_JSON_limpio(){
    var json = {"@context":{"reporter":"http://github.com/w3c/wai-wcag-em-report-tool/","wcagem":"http://www.w3.org/TR/WCAG-EM/#","Evaluation":"wcagem:procedure","defineScope":"wcagem:step1","scope":"wcagem:step1a","step1b":{"@id":"wcagem:step1b","@type":"@id"},"conformanceTarget":"step1b","accessibilitySupportBaseline":"wcagem:step1c","additionalEvaluationRequirements":"wcagem:step1d","exploreTarget":"wcagem:step2","essentialFunctionality":"wcagem:step2b","pageTypeVariety":"wcagem:step2c","technologiesReliedUpon":"wcagem:step2d","selectSample":"wcagem:step3","structuredSample":"wcagem:step3a","randomSample":"wcagem:step3b","Website":"wcagem:website","Webpage":"wcagem:webpage","auditSample":"wcagem:step4","reportFindings":"wcagem:step5","documentSteps":"wcagem:step5a","commissioner":"wcagem:commissioner","evaluator":"wcagem:evaluator","evaluationSpecifics":"wcagem:step5b","WCAG":"http://www.w3.org/TR/WCAG/#","WCAG20":"http://www.w3.org/TR/WCAG20/#","WCAG21":"http://www.w3.org/TR/WCAG21/#","WAI":"http://www.w3.org/WAI/","A":"WAI:WCAG2A-Conformance","AA":"WAI:WCAG2AA-Conformance","AAA":"WAI:WCAG2AAA-Conformance","wcagVersion":"WAI:standards-guidelines/wcag/#versions","reportToolVersion":"wcagem:reportToolVersion","earl":"http://www.w3.org/ns/earl#","Assertion":"earl:Assertion","TestMode":"earl:TestMode","TestCriterion":"earl:TestCriterion","TestCase":"earl:TestCase","TestRequirement":"earl:TestRequirement","TestSubject":"earl:TestSubject","TestResult":"earl:TestResult","OutcomeValue":"earl:OutcomeValue","Pass":"earl:Pass","Fail":"earl:Fail","CannotTell":"earl:CannotTell","NotApplicable":"earl:NotApplicable","NotTested":"earl:NotTested","assertedBy":"earl:assertedBy","mode":"earl:mode","result":"earl:result","subject":"earl:subject","test":"earl:test","outcome":"earl:outcome","dcterms":"http://purl.org/dc/terms/","title":"dcterms:title","description":"dcterms:description","summary":"dcterms:summary","date":"dcterms:date","hasPart":"dcterms:hasPart","isPartOf":"dcterms:isPartOf","id":"@id","type":"@type","language":"@language"},"language":"en","type":"Evaluation","reportToolVersion":"3.0.3","defineScope":{"id":"_:defineScope","scope":{"description":"","title":""},"conformanceTarget":"AA","accessibilitySupportBaseline":"","additionalEvaluationRequirements":"","wcagVersion":"2.1"},"exploreTarget":{"id":"_:exploreTarget","essentialFunctionality":"","pageTypeVariety":"","technologiesReliedUpon":[]},"selectSample":{"id":"_:selectSample","structuredSample":[],"randomSample":[]},"auditSample":[{"type":"Assertion","date":"2022-03-01T18:51:57.699Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.699Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:non-text-content","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.700Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.700Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:audio-only-and-video-only-prerecorded","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.700Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.700Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:captions-prerecorded","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.700Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.700Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:audio-description-or-media-alternative-prerecorded","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.701Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.701Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:captions-live","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.701Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.701Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:audio-description-prerecorded","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.701Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.701Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:info-and-relationships","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.701Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.701Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:meaningful-sequence","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.701Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.701Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:sensory-characteristics","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.701Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.701Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:orientation","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.701Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:identify-input-purpose","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:use-of-color","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:audio-control","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:contrast-minimum","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:resize-text","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:images-of-text","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.540Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:reflow","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:non-text-contrast","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:text-spacing","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:content-on-hover-or-focus","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:keyboard","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:no-keyboard-trap","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:character-key-shortcuts","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.702Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:timing-adjustable","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.702Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:pause-stop-hide","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:three-flashes-or-below-threshold","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:bypass-blocks","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:page-titled","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:focus-order","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:link-purpose-in-context","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:multiple-ways","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:headings-and-labels","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:focus-visible","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:pointer-gestures","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:pointer-cancellation","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:label-in-name","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.703Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.703Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:motion-actuation","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:language-of-page","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:language-of-parts","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:on-focus","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:on-input","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:consistent-navigation","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:consistent-identification","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.541Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:error-identification","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.542Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:labels-or-instructions","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.542Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:error-suggestion","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.542Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:error-prevention-legal-financial-data","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.542Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.704Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.704Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:parsing","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.542Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.705Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.705Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:name-role-value","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.542Z"}},{"type":"Assertion","date":"2022-03-01T18:51:57.705Z","mode":{"type":"TestMode","@value":"earl:manual"},"result":{"type":"TestResult","date":"2022-03-01T18:51:57.705Z","description":"","outcome":{"id":"earl:untested","type":["OutcomeValue","NotTested"]}},"subject":{"id":"_:subject_1","type":["TestSubject","Website"],"date":"2022-03-01T18:51:52.539Z","description":"","title":""},"test":{"id":"WCAG21:status-messages","type":["TestCriterion","TestRequirement"],"date":"2022-03-01T18:51:52.542Z"}}],"reportFindings":{"date":{"type":"http://www.w3.org/TR/NOTE-datetime","@value":"Tue Mar 01 1999"},"summary":"","title":"","commissioner":"","evaluator":"","documentSteps":[{"id":"_:about"},{"id":"_:defineScope"},{"id":"_:exploreTarget"},{"id":"_:selectSample"}],"evaluationSpecifics":""}};
    return json;
}

function merge_reportFindings(json, json1){
    //Date
    let fecha = Date.parse(json.reportFindings.date["@value"]);
    let fecha1 = Date.parse(json1.reportFindings.date["@value"]);
    
    //Se escribe la fecha mas reciente
    if(fecha < fecha1){
        json.reportFindings.date["@value"] = json1.reportFindings.date["@value"];
    }

    //Evaluator: El creador, si está vacío se pone el del documento importado, sino se deja al original
    if(json.reportFindings.evaluator == ""){
        json.reportFindings.evaluator = json1.reportFindings.evaluator;
    }

    //Comissioner: Quien lo ha hecho, se añaden
    let commissioner = json.reportFindings.commissioner;
    let commissioner1 =  json1.reportFindings.commissioner;
    if(commissioner !== ""){
        json.reportFindings.commissioner= commissioner+" & "+commissioner1;
    }else if(commissioner1 !== ""){
        json.reportFindings.commissioner= commissioner1;
    }


    //Summary
    let summary = json.reportFindings.summary;
    let summary1 = json1.reportFindings.summary;
    console.log("1: "+summary+" 2: "+summary1);

    if(summary == ""){
        json.reportFindings.summary= summary1;
    }else if(summary1 !== ""){
        json.reportFindings.summary= summary+" & "+summary1;
    }

    //Document steps??? No se que es


    //Evaluation specifics
    /*
    WCAG-EM suggests that you archive the web pages audited. For more information, see WCAG-EM Step 5.b: Record the Evaluation
     Specifics. You can use this text field to record the evaluation tools, web browsers, assistive technologies, 
     other software, and methods used for the evaluation. What you enter here will be included in the generated report. 
     After you download the report, you could delete or edit this information in the HTML file before submitting the report.
    */
    let evaluationSpecifics = json.reportFindings.evaluationSpecifics;
    let evaluationSpecifics1 =  json1.reportFindings.evaluationSpecifics;
    if(evaluationSpecifics !== ""){
        json.reportFindings.evaluationSpecifics= evaluationSpecifics+" & "+evaluationSpecifics1;
    }else if(evaluationSpecifics1 !== ""){
        json.reportFindings.evaluationSpecifics= evaluationSpecifics1;
    }


    return json;
}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

//IMPORTANTE: TIENEN QUE TENER LA MISMA LONGITUD: SER LOS DOS DEL TIPO AA
function merge_audit_samples(primario,secundario){
    var arr_sec = secundario.auditSample;
    let longitud = primario.auditSample.length;
    console.log("Long: "+longitud);
    //La longitud es 50 en AA

    for (var i = 0; i <longitud; i++){
        var obj_prim = primario.auditSample[i];
        //console.log(obj_prim.test.id);

        /*
        --------------------Criterio---------------------
        -Si en alguno de los dos es FAILED, se pone failed.
        -Si en uno esta untested y en el otro tested, se pone el resultado del otro
        -Si en uno es cantTell y el otro hay un resultado, se pone el resultado
        */

        //Comprobamos si en el original pasa o no.
        var res_prov1 = primario.auditSample[i].result.outcome.id;
        var res_prov2 = secundario.auditSample[i].result.outcome.id;

        var au1 = primario.auditSample[i];
        var au2 = secundario.auditSample[i];

        switch(true){

            //Caso el primero untested y el segundo distinto de untested
            case(res_prov1 == "earl:untested" && res_prov2 !== "earl:untested"):
                primario.auditSample[i].result = au2.result;
                break;


            //Caso los dos fallan: Se suman las descripciones
            case(res_prov1 == "earl:failed" && res_prov2 == "earl:failed"):
                primario.auditSample[i].result.description = "-"+au1.result.description+" \n -"+au2.result.description;
                break;
            //Caso el segundo es failed, da igual cual es el primero
            case(res_prov2 == "earl:failed"):
                primario.auditSample[i].result= au2.result;
                break;

            //Caso el primero es cantTell y el segundo distinto de cantTell
            case(res_prov1 == "earl:cantTell" && res_prov2 !== "earl:cantTell"):
                primario.auditSample[i].result = au2.result;
                break;


            default:
                break;
        }


        /*
        for (var key in obj){
            var value = obj[key];
            document.write("<br> - " + key + ": " + value);
        }
        */
    }
}
;;(function($,yl){yl.forwardHandlerRegistry=yl.forwardHandlerRegistry||{};yl.registerForwardHandler=function(name,handler){yl.forwardHandlerRegistry[name]=handler;};yl.getForwardHandler=function(name){return yl.forwardHandlerRegistry[name];};function getForwardStrategy(element){var checkForCheckboxes=function(){var all=true;$.each(element,function(ix,e){if($(e).attr("type")!=="checkbox"){all=false;}});return all;};if(element.length===1&&element.attr("type")==="checkbox"&&element.attr("value")===undefined){return"exists";}else if(element.length===1&&element.attr("multiple")!==undefined){return"multiple";}else if(checkForCheckboxes()){return"multiple";}else{return"single";}}
yl.getFieldRelativeTo=function(element,name){var prefixes=$(element).getFormPrefixes();for(var i=0;i<prefixes.length;i++){var fieldSelector="[name="+prefixes[i]+name+"]";var field=$(fieldSelector);if(field.length){return field;}}
return $();};yl.getValueFromField=function(field){var strategy=getForwardStrategy(field);var serializedField=$(field).serializeArray();var getSerializedFieldElementAt=function(index){if(serializedField.length>index){return serializedField[index];}else{return null;}};var getValueOf=function(elem){if(elem.hasOwnProperty("value")&&elem.value!==undefined){return elem.value;}else{return null;}};var getSerializedFieldValueAt=function(index){var elem=getSerializedFieldElementAt(index);if(elem!==null){return getValueOf(elem);}else{return null;}};if(strategy==="multiple"){return serializedField.map(function(item){return getValueOf(item);});}else if(strategy==="exists"){return serializedField.length>0;}else{return getSerializedFieldValueAt(0);}};yl.getForwards=function(element){var forwardElem,forwardList,forwardedData,divSelector,form;divSelector="div.dal-forward-conf#dal-forward-conf-for-"+
element.attr("id");form=element.length>0?$(element[0].form):$();forwardElem=form.find(divSelector).find('script');if(forwardElem.length===0){return;}
try{forwardList=JSON.parse(forwardElem.text());}catch(e){return;}
if(!Array.isArray(forwardList)){return;}
forwardedData={};$.each(forwardList,function(ix,field){var srcName,dstName;if(field.type==="const"){forwardedData[field.dst]=field.val;}else if(field.type==="self"){if(field.hasOwnProperty("dst")){dstName=field.dst;}else{dstName="self";}
forwardedData[dstName]=yl.getValueFromField(element);}else if(field.type==="field"){srcName=field.src;if(field.hasOwnProperty("dst")){dstName=field.dst;}else{dstName=srcName;}
var forwardedField=yl.getFieldRelativeTo(element,srcName);if(!forwardedField.length){return;}
forwardedData[dstName]=yl.getValueFromField(forwardedField);}else if(field.type==="javascript"){var handler=yl.getForwardHandler(field.handler);forwardedData[field.dst||field.handler]=handler(element);}});return JSON.stringify(forwardedData);};})(yl.jQuery,yl);
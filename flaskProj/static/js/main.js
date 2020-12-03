function checkForm(formTag) {
    /*
    Element.name.value 
    0,null,'',undifiend =not
    */ 
    debugger
    if (!formTag.siteName.value ||
        !formTag.keyword.value ||
        !formTag.itemCount.value ||
        !formTag.translate.value ||
        !formTag.currency.value) {
        alert('please check empty box');
        return false;
    }
    return true
}
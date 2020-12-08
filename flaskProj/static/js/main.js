
/*DOMContentLoaded = DOM트리구성후 호출됨, 이미지,CSS를 기다리지않음. =$(document).onload 
완전히 페이지가 로드 된 후 사용하기 위해선 window.onload를 사용하여야함 .*/
document.addEventListener("DOMContentLoaded",function(){

    if(typeof searchedVal !== 'undefined'){
        this.querySelector("#siteNameId").value=searchedVal.siteName
        this.querySelector("#keywordId").value=searchedVal.keyword
        this.querySelector("#itemCountId").value=searchedVal.itemCount
        this.querySelector("#translateId").value=searchedVal.translate
        this.querySelector("#currencyId").value=searchedVal.currency
    }
})

function checkForm(formTag) {
    /*
    Element.name.value 
    0,null,'',undifiend =not
    */ 

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
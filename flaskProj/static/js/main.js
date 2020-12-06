
/*DOMContentLoaded = DOM트리구성후 호출됨, 이미지,CSS를 기다리지않음. =$(document).onload 
완전히 페이지가 로드 된 후 사용하기 위해선 window.onload를 사용하여야함 .*/
document.addEventListener("DOMContentLoaded",function(){

    if(typeof searchedVal !== 'undefined'){
        document.querySelector("#siteNameId").value=searchedVal.siteName
        document.querySelector("#keywordId").value=searchedVal.keyword
        document.querySelector("#itemCountId").value=searchedVal.itemCount
        document.querySelector("#translateId").value=searchedVal.translate
        document.querySelector("#currencyId").value=searchedVal.currency
    }
   
    this.querySelector("#siteNameId > option:nth-child(2)").setAttribute('selected','')
    this.querySelector("#keywordId").value='머리띠'
    this.querySelector("#itemCountId").value='5'
    this.querySelector("#translateId > option:nth-child(2)").setAttribute('selected','')
    this.querySelector("#currencyId > option:nth-child(2)").setAttribute('selected','')
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
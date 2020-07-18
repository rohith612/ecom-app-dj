 function getCookies(name){
     var cookieArr = document.cookie.split(";")

     for(var i=0;i<cookieArr.length;i++){
         var cookiePair = cookieArr[i].split("=")
         if(name == cookiePair[0].trim()){
              return decodeURIComponent(cookiePair[1])
         }
     }

     return null;
 }

 var cart = JSON.parse(getCookies('cart'))

 if( cart == undefined || cart == null){
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
 }

  function clearCookies(){
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
  }
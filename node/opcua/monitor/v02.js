

setTimeout(function(){
   /* 代码块... */
   setTimeout(arguments.callee, 10);
}, 10);

setInterval(function(){
   /*代码块... */
 }, 10);
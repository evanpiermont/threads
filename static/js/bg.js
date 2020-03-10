

// this code will initilize the screen, font sizes, colors etc. keep colors
// here for easy changing.
//



$cBG = '#e9eeef';
$cInputBG = '#0A3F61';
$cInputText = '#ED8689';
$cBodyText = '#0A3F61';
$hl = '#ED8689';

fontsize = function () {
    z = 0.09
    if (window.matchMedia("only screen and (max-width : 500px)").matches) {
        z = 0.11
    }
    var x = window.innerWidth * z; // z of container width
    var y = window.innerHeight * z; // z of container height
    var fontSize = Math.min(x,y);
    d3.select("body").style('font-size', fontSize + "px");
};



colors = function(){
    d3.select("#background").style('background-color', $cBG);
    //d3.select("input").style('background-color', $cInputBG);
    //d3.select("input").style('color', $cInputText);
    d3.select("body").style('color', $cBodyText);
    d3.select(".submit").style('background-color', $cInputBG);
};


d3.select(window).on("resize", fontsize);
document.addEventListener("DOMContentLoaded", colors);
document.addEventListener("DOMContentLoaded", fontsize);


// window.location.hash="iLSTxs";  
// window.location.hash="iLSTxs3";//again because google chrome don't insert first hash into history
// window.onhashchange=function(){window.location.hash="iLSTxs";}







$(document).ready(function(){
 $('.header').height($(window).height());
})

var title = document.querySelector('h3');

function getRandomColor(){
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i=0; i < 6; i++){
        color +=letters[Math.floor(Math.random()*16)];
    }
    return color;
};

function changeTitleColor(){
    colorInput = getRandomColor();
    title.style.color = colorInput;
}

setInterval('changeTitleColor()', 500);
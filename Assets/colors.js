export const ICONCOLORS = {
    red : "rgb(205, 73, 69)",
    orange : "rgb(216, 118, 32)",
    yellow : "rgb(202, 142, 27)",
    green : "rgb(45, 153, 100)",
    blue : "rgb(46, 124, 209)",
    purple : "rgb(141, 91, 193)",
    pink : "rgb(201, 64, 121)",
    gray : "rgb(127, 127, 127)",
    white : "rgb(211, 211, 211)"
}

export const COLORS = {
    lightGray : "rgb(55, 55, 55)",
    gray : "rgb(90, 90, 90)",
    brown : "rgb(96, 59, 44)", 
    red : "rgb(110, 54, 48)", 
    orange : "rgb(133, 76, 29)",
    yellow : "rgb(137, 99, 42)", 
    green : "rgb(43, 89, 63)", 
    blue : "rgb(40, 69, 108)", 
    purple : "rgb(73, 47, 100)",
    pink : "rgb(105, 49, 76)"
}

export const PAGECOLORS = {
    subIconGray : "rgb(134, 134, 134)",
    calloutGray : "rgb(39, 39, 39)",
    scrollBarGray : "rgb(71, 76, 80)",
    dividerGray : "rgb(47, 47, 47)",
    backgroundBlack : "rgb(25, 25, 25)",
    whiteText : "rgb(214, 214, 214)"
}


// really funny one liner to turn rgb to rgba with opacity 0.5
export function makeOpaque(str) {
    const numbers = "rgba("+str.split("(")[1].substring(0, str.split("(")[1].length - 1)+", 0.1)";
    return numbers;    
}
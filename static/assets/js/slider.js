"use strict";

productScroll();
productScroll2();
productScroll3();
console.log("product-scroll start")
console.log("product-scroll2 start")

function productScroll() {
  let slider = document.getElementById("slider");
  let next = document.getElementsByClassName("pro-next");
  let prev = document.getElementsByClassName("pro-prev");
  let slide = document.getElementById("slide");
  let item = document.getElementById("slide");

  for (let i = 0; i < next.length; i++) {
    //refer elements by class name

    let position = 0; //slider postion

    prev[i].addEventListener("click", function() {
      //click previos button
      if (position > 0) {
        //avoid slide left beyond the first item
        position -= 1;
        translateX(position); //translate items
      }
    });

    next[i].addEventListener("click", function() {
      if (position >= 0 && position < hiddenItems()) {
        //avoid slide right beyond the last item
        position += 1;
        translateX(position); //translate items
      }
    });
  }

  function hiddenItems() {
    //get hidden items
    let items = getCount(item, false);
    let visibleItems = slider.offsetWidth / 210;
    return items - Math.ceil(visibleItems);
  }
}

function translateX(position) {
  //translate items
  slide.style.left = position * -140 + "px";
}

function getCount(parent, getChildrensChildren) {
  //count no of items
  let relevantChildren = 0;
  let children = parent.childNodes.length;
  for (let i = 0; i < children; i++) {
    if (parent.childNodes[i].nodeType != 3) {
      if (getChildrensChildren)
        relevantChildren += getCount(parent.childNodes[i], true);
      relevantChildren++;
    }
  }
  return relevantChildren;
}


// for second slider 
function productScroll2() {
  let slider2 = document.getElementById("slider2");
  let next2 = document.getElementsByClassName("pro-next2");
  let prev2 = document.getElementsByClassName("pro-prev2");
  let slide2 = document.getElementById("slide2");
  let item2 = document.getElementById("slide2");

  for (let j = 0; j < next2.length; j++) {
    //refer elements by class name

    let position2 = 0; //slider postion

    prev2[j].addEventListener("click", function() {
      //click previos button
      if (position2 > 0) {
        //avoid slide left beyond the first item
        position2 -= 1;
        translateX2(position2); //translate items
      }
    });

    next2[j].addEventListener("click", function() {
      if (position2 >= 0 && position2 < hiddenItems2()) {
        //avoid slide right beyond the last item
        position2 += 1;
        translateX2(position2); //translate items
      }
    });
  }

  function hiddenItems2() {
    //get hidden items
    let items2 = getCount2(item2, false);
    let visibleItems2 = slider2.offsetWidth / 210;
    return items2 - Math.ceil(visibleItems2);
  }
}

function translateX2(position2) {
  //translate items
  slide2.style.left = position2 * -140 + "px";
}

function getCount2(parent2, getChildrensChildren2) {
  //count no of items
  let relevantChildren2 = 0;
  let children2 = parent2.childNodes.length;
  for (let j = 0; j < children2; j++) {
    if (parent2.childNodes[j].nodeType != 3) {
      if (getChildrensChildren2)
        relevantChildren2 += getCount2(parent.childNodes[j], true);
      relevantChildren2++;
    }
  }
  return relevantChildren2;
}


// for third slider 
function productScroll3() {
  let slider3 = document.getElementById("slider3");
  let next3 = document.getElementsByClassName("pro-next3");
  let prev3 = document.getElementsByClassName("pro-prev3");
  let slide3 = document.getElementById("slide3");
  let item3 = document.getElementById("slide3");

  for (let k = 0; k < next3.length; k++) {
    //refer elements by class name

    let position3 = 0; //slider postion

    prev3[k].addEventListener("click", function() {
      //click previos button
      if (position3 > 0) {
        //avoid slide left beyond the first item
        position3 -= 1;
        translateX3(position3); //translate items
      }
    });

    next3[k].addEventListener("click", function() {
      if (position3 >= 0 && position3 < hiddenItems3()) {
        //avoid slide right beyond the last item
        position3 += 1;
        translateX3(position3); //translate items
      }
    });
  }

  function hiddenItems3() {
    //get hidden items
    let items3 = getCount3(item3, false);
    let visibleItems3 = slider3.offsetWidth / 210;
    return items3 - Math.ceil(visibleItems3);
  }
}

function translateX3(position3) {
  //translate items
  slide3.style.left = position3 * -140 + "px";
}

function getCount3(parent3, getChildrensChildren3) {
  //count no of items
  let relevantChildren3 = 0;
  let children3 = parent3.childNodes.length;
  for (let k = 0; k < children3; k++) {
    if (parent3.childNodes[k].nodeType != 3) {
      if (getChildrensChildren3)
        relevantChildren3 += getCount3(parent.childNodes[k], true);
      relevantChildren3++;
    }
  }
  return relevantChildren3;
}


// ==UserScript==
// @name           TrollEyBuzz
// @namespace      http://userscripts.org/users/20935
// @description    Hide comments written by trolls on Google Buzz
// @author         Wojciech 'KosciaK' Pietrzok
// @version        0.1
// @include        https://mail.google.*/mail/*
// @include        http://mail.google.*/mail/*
// ==/UserScript==


(function() {

/*
 * ----------------------------------------------------------------------------
 * Edit TROLLS list below. 
 * Copy troll's profile URL (right click on his name, and copy URL) 
 * and add to the list.
 * 
 * Example:
   var TROLLS = [
       'http://www.google.com/profiles/UglyTroll#buzz',
       'http://www.google.com/profiles/123456789012345678901#buzz',
   ];
 */

var TROLLS = [
    '',
];

/*
 * Do not edit below this line
 * ----------------------------------------------------------------------------
 */

var CANVAS

var hideNode = function(node) {
    node.innerHTML = '[...]';
    node.title = 'Show comment';
    node.previousSibling.style.display = 'none';
    node.addEventListener('click', show, false);
}

var hide = function() {
    this.removeEventListener('click', hide, false);
    hideNode(this);
}

var show = function() {
    this.innerHTML = ' <b>(hide)<b>';
    this.title = 'Hide comment';
    this.previousSibling.style.display = 'inline';
    this.removeEventListener('click', show, false);
    this.addEventListener('click', hide, false);
}

var detrollify = function() {
    for (i=0; i < TROLLS.length ; i++) {
        var result = CANVAS.evaluate('//span[@class="Yd"]/a[@href="'+ TROLLS[i] +'" and not(@troll="true")]', 
                                     CANVAS, null, 
                                     XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, 
                                     null); 
        for (j=0; j < result.snapshotLength ; j++) {
            item = result.snapshotItem(j);
            item.setAttribute("troll", "true");
            item.style.textDecoration = "line-through";
            comment = item.parentNode.getElementsByTagName('span')[1];
            button = CANVAS.createElement('span');
            button.className = "showHide";
            item.parentNode.insertBefore(button, comment.nextSibling);
            hideNode(button);
        }
    }
    setTimeout(detrollify, 500)
}

var init = function() {
    if (!document.getElementById('canvas_frame')) {
        return;
    }
    CANVAS = document.getElementById('canvas_frame').contentDocument;
    var result = CANVAS.evaluate('//span[@class="Yd"]/a[1]', 
                                 CANVAS, null, 
                                 XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, 
                                 null); 
    if (result.snapshotLength < 1) {
        setTimeout(init, 250);
        return;
    }
    detrollify();
}

GM_addStyle('.showHide:hover {text-decoration: underline; cursor: pointer; cursor: hand;}');
init();

})();


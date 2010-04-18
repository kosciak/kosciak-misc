// ==UserScript==
// @name           Blip.pl - Rdir.pl stats and re.blipi.pl
// @namespace      http://userscripts.org/users/20935
// @description    Rdir.pl stats and re.blipi.pl mashup
// @author         Wojciech 'KosciaK' Pietrzok
// @version        0.3.1
// @include        http://rdir.pl/*/stats
// ==/UserScript==

function $$(xpath,root) { 
  xpath = xpath
    .replace(/((^|\|)\s*)([^/|\s]+)/g,'$2.//$3')
    .replace(/\.([\w-]+)(?!([^\]]*]))/g, '[@class="$1" or @class$=" $1" or @class^="$1 " or @class~=" $1 "]')
    .replace(/#([\w-]+)/g, '[@id="$1"]')
    .replace(/\/\[/g,'/*[');
  str = '(@\\w+|"[^"]*"|\'[^\']*\')';
  xpath = xpath
    .replace(new RegExp(str+'\\s*~=\\s*'+str,'g'), 'contains($1,$2)')
    .replace(new RegExp(str+'\\s*\\^=\\s*'+str,'g'), 'starts-with($1,$2)')
    .replace(new RegExp(str+'\\s*\\$=\\s*'+str,'g'), 'substring($1,string-length($1)-string-length($2)+1)=$2');
  var got = document.evaluate(xpath, root||document, null, 5, null), result=[];
  while (next = got.iterateNext())
    result.push(next);
  return result;
 }



(function() {
    url = document.documentURI
    rdir_id = url.substring(15, url.lastIndexOf("/"))
    reblipi_url = "http://re.blipi.pl/" + rdir_id

    GM_addStyle("#loading { display: block; margin: 1em auto; }")
    GM_addStyle(".avatar {width: 15px; height: 15px;} br {margin-bottom: 1em;} .show { font-size: smaller; }")
    
    box = $$(".module")[0]

    header = document.createElement('h3')
    header.innerHTML = 'Magia RE.BLIPI <a href="' + reblipi_url + '">' + reblipi_url + '</a>'

    loading = document.createElement('img')
    loading.setAttribute('id', 'loading')
    loading.setAttribute('src', 'http://blip.pl/images/ajax-loading.gif')

    box.appendChild(header)
    box.appendChild(loading)

    GM_xmlhttpRequest({
        method: "GET",
        url: "http://re.blipi.pl/" + rdir_id,
        onload: function(response) {
            var responseXML = document.createElement('html')
            responseXML.innerHTML = response.responseText

            results = document.createElement('ul');

            active = $$("tr", responseXML)
            last_td = active[active.length-1];
            if (last_td.childNodes[1].className != "head") {
                results.innerHTML = '<li class="normal margin"><li>' + last_td.innerHTML + "</li>"
            }
            box.replaceChild(results, loading)
            /*
            for (i=active.length-1; i>=0; i--) {
                last_td = active[i];
                alert(last_td.attributes.getNamedItem("colspan").value)
                if (last_td.attributes.getNamedItem("colspan")) {
                    results.innerHTML = '<li class="normal margin">Napisali:</li><li>' + last_td.innerHTML + "</li>"

                    box.replaceChild(results, loading)
                    break;
                }
            }
            */
        }
    });

})();




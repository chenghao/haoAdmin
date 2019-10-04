/** EasyWeb spa v3.0.8 data:2019-03-24 License By http://easyweb.vip */

//eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('4.H(["t","5"],8(a){2 c=4.t;2 b=4.5;2 d={C:8(h,j,e){7(2 g=0;g<j.s;g++){d.u(h,j[g],e[g])}2 f=c(\'[x-y="\'+h+\'"]+.4-5-z .4-5-v B\');f.6(\'[r="q"]\').G();b.F("E("+h+")",8(i){d.C(h,j,e)})},u:8(f,m,n){2 e=c(\'[x-y="\'+f+\'"]+.4-5-z .4-5-v B\');2 k=b.D[f];2 o=k[0][n],g=1;7(2 l=1;l<k.s;l++){w(k[l][n]==o){g++;w(l==k.s-1){e.3(l-g+1).6("9").3(m).p("A",g);7(2 h=1;h<g;h++){e.3(l-h+1).6("9").3(m).p("r","q")}}}I{e.3(l-g).6("9").3(m).p("A",g);7(2 h=1;h<g;h++){e.3(l-h).6("9").3(m).p("r","q")}g=1;o=k[l][n]}}}};a("J",d)});',46,46,'||var|eq|layui|table|find|for|function|td||||||||||||||||attr|true|del|length|jquery|merge|body|if|lay|filter|view|rowspan|tr|merges|cache|sort|on|remove|define|else|tableX'.split('|'),0,{}))

layui.define(["jquery", "table"],
    function(a) {
        var c = layui.jquery;
        var b = layui.table;
        var d = {
            merges: function(h, j, e) {
                for (var g = 0; g < j.length; g++) {
                    d.merge(h, j[g], e[g])
                }
                var f = c('[lay-filter="' + h + '"]+.layui-table-view .layui-table-body tr');
                f.find('[del="true"]').remove();
                b.on("sort(" + h + ")",
                    function(i) {
                        d.merges(h, j, e)
                    })
            },
            merge: function(f, m, n) {
                var e = c('[lay-filter="' + f + '"]+.layui-table-view .layui-table-body tr');
                var k = b.cache[f];
                var o = k[0][n],
                    g = 1;
                for (var l = 1; l < k.length; l++) {
                    if (k[l][n] == o) {
                        g++;
                        if (l == k.length - 1) {
                            e.eq(l - g + 1).find("td").eq(m).attr("rowspan", g);
                            for (var h = 1; h < g; h++) {
                                e.eq(l - h + 1).find("td").eq(m).attr("del", "true")
                            }
                        }
                    } else {
                        e.eq(l - g).find("td").eq(m).attr("rowspan", g);
                        for (var h = 1; h < g; h++) {
                            e.eq(l - h).find("td").eq(m).attr("del", "true")
                        }
                        g = 1;
                        o = k[l][n]
                    }
                }
            }
        };
        a("tableX", d)
    });
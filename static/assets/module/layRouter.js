﻿/** EasyWeb spa v3.0.8 data:2019-03-24 License By http://easyweb.vip */

//eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('n.B(2(d){3 a=[];3 f,c=9.i;3 e=2(j){3 h;3 g="";1(j){g=j;h=n.q("#"+j)}7{h=n.q();p(3 k=0;k<h.t.s;k++){g+=("/"+h.t[k])}}1(!g||g=="/"){1(f){9.C("#"+f)}}7{1(g){p(3 k=0;k<a.s;k++){1(h.v.E(a[k])){g=a[k];D}}1(b.5){b.5.o(4,h)}b.A=h.v;1(b[g]){b[g].o(4,h)}7{1(b.6){b.6.o(4,h)}}}}};3 b={m:u,K:2(g){f=g.L;1(g.5&&8 g.5=="2"){b.5=g.5}1(g.6&&8 g.6=="2"){b.6=g.6}e();l 4},w:2(j,g){1(!j){l}1(g==z){g=2(){}}1(j x F){b[j]=g;a.G(j)}7{1(j x H){p(3 h I j){4.w.J(4,[].y(j[h]).y(g))}}7{1(8 j=="r"){1(8 g=="2"){b[j]=g}7{1(8 g=="r"&&b[g]){b[j]=b[g]}}}}}l 4},M:2(g){9.i="#"+g},N:2(g){b.m=O;e(g);b.m=u}};P(2(){1(c!=9.i){c=9.i;e()}},Q);d("R",b)});',54,54,'|if|function|var|this|pop|notFound|else|typeof|location|||||||||hash|||return|isRefresh|layui|call|for|router|string|length|path|false|href|reg|instanceof|concat|undefined|lash|define|replace|break|match|RegExp|push|Array|in|apply|init|index|go|refresh|true|setInterval|100|layRouter'.split('|'),0,{}))

layui.define(function(d) {
    var a = [];
    var f, c = location.hash;
    var e = function(j) {
        var h;
        var g = "";
        if (j) {
            g = j;
            h = layui.router("#" + j)
        } else {
            h = layui.router();
            for (var k = 0; k < h.path.length; k++) {
                g += ("/" + h.path[k])
            }
        }

        if (!g || g == "/") {
            if (f) {
                location.replace("#" + f)
            }
        } else {
            if (g) {
                for (var k = 0; k < a.length; k++) {
                    if (h.href.match(a[k])) {
                        g = a[k];
                        break
                    }
                }
                if (b.pop) {
                    b.pop.call(this, h)
                }
                b.lash = h.href;
                if (b[g]) {
                    b[g].call(this, h)
                } else {
                    if (b.notFound) {
                        b.notFound.call(this, h)
                    }
                }
            }
        }
    };
    var b = {
        isRefresh: false,
        init: function(g) {
            f = g.index;
            if (g.pop && typeof g.pop == "function") {
                b.pop = g.pop
            }
            if (g.notFound && typeof g.notFound == "function") {
                b.notFound = g.notFound
            }
            e();
            return this
        },
        reg: function(j, g) {
            if (!j) {
                return
            }
            if (g == undefined) {
                g = function() {}
            }
            if (j instanceof RegExp) {
                b[j] = g;
                a.push(j)
            } else {
                if (j instanceof Array) {
                    for (var h in j) {
                        this.reg.apply(this, [].concat(j[h]).concat(g))
                    }
                } else {
                    if (typeof j == "string") {
                        if (typeof g == "function") {
                            b[j] = g
                        } else {
                            if (typeof g == "string" && b[g]) {
                                b[j] = b[g]
                            }
                        }
                    }
                }
            }
            return this
        },
        go: function(g) {
            location.hash = "#" + g
        },
        refresh: function(g) {
            b.isRefresh = true;
            e(g);
            b.isRefresh = false
        }
    };
    setInterval(function() {
            if (c != location.hash) {
                c = location.hash;
                e()
            }
        },
        100);
    d("layRouter", b)
});
/** EasyWeb spa v3.0.8 data:2019-03-24 License By http://easyweb.vip */

//eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('4.E(1(a){3 b={W:"/11/",8:"T-U",V:r,Z:g,13:x,A:"B",C:".F",I:"K-n",o:1(){3 c=4.9(b.8);7(c){5 c.i}},w:1(){4.9(b.8,{k:"i",y:g})},z:1(c){4.9(b.8,{k:"i",h:c})},s:1(){3 c=4.9(b.8);7(c){5 c.t}},D:1(c){4.9(b.8,{k:"t",h:c})},1e:1(){3 e=b.s().G;3 c=[];H(3 d=0;d<e.J;d++){c.p(e[d].L)}5 c},M:1(){3 d=[];3 c=b.o();7(c){d.p({N:"O",h:"P "+c})}5 d},Q:1(c){7(c.j==S){b.w();f.l("登录过期",{m:2,X:Y},1(){u.10()});5 r}v{7(c.j==12){f.l("没有访问权限",{m:2})}v{7(c.j==q){f.l("q目标不存在",{m:2})}}}5 g},14:1(c){f.15("路由"+u.16+"不存在",{17:"提示",18:"4-f-n",19:[],1a:"1b",1c:6,1d:g})}};a("R",b)});',62,77,'|function||var|layui|return||if|tableName|data||||||layer|true|value|token|code|key|msg|icon|admin|getToken|push|404|false|getUser|login_user|location|else|removeToken|20|remove|putToken|viewPath|components|viewSuffix|putUser|define|html|authorities|for|defaultTheme|length|theme|authority|getAjaxHeaders|name|Authorization|Bearer|ajaxSuccessBefore|config|401|easyweb|jwt|pageTabs|base_server|time|1500|openTabCtxMenu|reload|v1|403|maxTabNum|routerNotFound|alert|hash|title|skin|btn|offset|30px|anim|shadeClose|getUserAuths'.split('|'),0,{}))

layui.define(function(a) {
    var b = {
        base_server: "/v1/",
        tableName: "easyweb-jwt",
        pageTabs: true,
        openTabCtxMenu: true,
        maxTabNum: 20,
        viewPath: "components",
        viewSuffix: ".html",
        defaultTheme: "theme-admin",
        getToken: function() {
            var c = layui.data(b.tableName);
            if (c) {
                return c.token
            }
        },
        removeToken: function() {
            layui.data(b.tableName, {
                key: "token",
                remove: true
            })
        },
        putToken: function(c) {
            layui.data(b.tableName, {
                key: "token",
                value: c
            })
        },
        getUser: function() {
            var c = layui.data(b.tableName);
            if (c) {
                return c.login_user
            }
        },
        putUser: function(c) {
            layui.data(b.tableName, {
                key: "login_user",
                value: c
            })
        },
        getUserAuths: function() {
            var e = b.getUser().authorities;
            var c = [];
            for (var d = 0; d < e.length; d++) {
                c.push(e[d].authority)
            }
            return c
        },
        getAjaxHeaders: function() {
            var d = [];
            var c = b.getToken();
            if (c) {
                d.push({
                    name: "Authorization",
                    value: "Bearer " + c
                })
            }
            return d
        },
        ajaxSuccessBefore: function(c) {
            if (c.code == 401) {
                b.removeToken();
                layer.msg("登录过期", {
                        icon: 2,
                        time: 1500
                    },
                    function() {
                        location.reload()
                    });
                return false
            } else {
                if (c.code == 403) {
                    layer.msg("没有访问权限", {
                        icon: 2
                    })
                } else {
                    if (c.code == 404) {
                        layer.msg("404目标不存在", {
                            icon: 2
                        })
                    }
                }
            }
            return true
        },
        routerNotFound: function(c) {
            layer.alert("路由" + location.hash + "不存在", {
                title: "提示",
                skin: "layui-layer-admin",
                btn: [],
                offset: "30px",
                anim: 6,
                shadeClose: true
            })
        }
    };
    a("config", b)
});
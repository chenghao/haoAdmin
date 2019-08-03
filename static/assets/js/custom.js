/**
 * 成功的提示
 * @param msg
 */
function success(msg, param, callback) {
    if(!param) param = {icon: 1};
    layer.msg(msg, param, function () {
        if(callback) callback();
    });
}

/**
 * 失败的提示
 * @param msg
 */
function error(msg) {
    layer.msg(msg, {icon: 2});
}

/**
 * 加载等待框
 */
function loadWait() {
    layer.load();
}

/**
 * 关闭等待框
 */
function closeLoadWait() {
    layer.closeAll('loading');
}

////////////////////////////////////////////////////////////////////////////////////////////

/**
 * 删除时的提示框
 * @param url
 * @param param
 * @param jquery
 * @param callback
 */
function confirmDel(jquery, url, param, callback, title) {
    if(!title) title = '确定删除此数据吗？';
    _confirm(jquery, title, url, param, callback, 'DELETE');
}

/**
 * 新增时的提示框
 * @param url
 * @param param
 * @param jquery
 * @param callback
 */
function confirmAdd(jquery, url, param, callback, title) {
    if(!title) title = '确定新增此数据吗？';
    _confirm(jquery, title, url, param, callback, 'POST');
}

/**
 * 编辑时的提示框
 * @param url
 * @param param
 * @param jquery
 * @param callback
 */
function confirmEdit(jquery, url, param, callback, title) {
    if(!title) title = '确定编辑此数据吗？';
    _confirm(jquery, title, url, param, callback, 'PUT');
}

/**
 * 确认
 * @param title
 * @param url
 * @param param
 * @param jquery
 * @param callback
 * @param method
 * @private
 */
function _confirm(jquery, title, url, param, callback, method) {
    layer.confirm(title, {
        offset: '65px',
        skin: 'layui-layer-admin'
    }, function (i) {
        layer.close(i);

        jqueryAjax(jquery, url, param, function (data) {
            if(callback){
                callback(data);
            }
        }, method);
    });
}

////////////////////////////////////////////////////////////////////////////////////////////

/**
 * 打开窗口
 * @param jquery
 * @param area
 * @param title
 * @param id
 * @param callback
 */
function openWindow(jquery, area, title, id, callback) {
    layer.open({
        skin: 'layui-layer-admin',
        type: 1,
        area: area,
        offset: '65px',
        title: title,
        content: jquery(id).html(),
        success: function (layero, index) {
            jquery(layero).children('.layui-layer-content').css('overflow', 'visible');

            if(callback){
                callback();
            }
        }
    });
}

////////////////////////////////////////////////////////////////////////////////////////////
function jqueryAjaxGET(jquery, url, param, callback, notLoad, hideSuccessMsg) {
    jqueryAjax(jquery, url, param, callback, "GET", notLoad, hideSuccessMsg)
}
function jqueryAjaxPOST(jquery, url, param, callback, notLoad, hideSuccessMsg) {
    jqueryAjax(jquery, url, param, callback, "POST", notLoad, hideSuccessMsg)
}
function jqueryAjaxPUT(jquery, url, param, callback, notLoad, hideSuccessMsg) {
    jqueryAjax(jquery, url, param, callback, "PUT", notLoad, hideSuccessMsg)
}
function jqueryAjaxDELETE(jquery, url, param, callback, notLoad, hideSuccessMsg) {
    jqueryAjax(jquery, url, param, callback, "DELETE", notLoad, hideSuccessMsg)
}

function jqueryAjax(jquery, url, param, callback, method, notLoad, hideSuccessMsg) {
    if(!notLoad){ // 为true时就不显示等待框
        loadWait();
    }

    jquery.ajax({
        url: layui.config.base_server + url,
        type: method ? method : "get",
        data: param ? param : {},
        dataType: "json",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'JWT ' + layui.config.getToken());
        },
        success: function (data) {
            console.log("==================")
            console.log(url);
            console.log(data);
            console.log("==================")
            if(data.code == 200 || data.code == 0){
                if(!hideSuccessMsg) success(data.msg);

                if(callback) callback(data);
            } else {
                error(data.msg);
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            // console.log(textStatus);
            // console.log(errorThrown);
            if(jqXHR.hasOwnProperty("responseJSON")){
                var json = jqXHR.responseJSON;
                if(json.hasOwnProperty("msg")){
                    error(json.msg);
                }
            }
        },
        complete: function () {
            closeLoadWait();
        }
    });
}

////////////////////////////////////////////////////////////////////////////////////////////
function table_render(table, id, url, cols, opts, parseData) {
    var opt = {
        elem: id,
        url: layui.config.base_server + url,
        headers: {
            'Authorization': 'JWT ' + layui.config.getToken()
        },
        cellMinWidth: 100,
        cols: cols,
        parseData: function (res) {
            if(parseData) parseData(res);
        }
    };

    if(!opts) opts = {};
    opt["page"] = opts.hasOwnProperty("page") ? opts["page"] : true;
    opt["limit"] = opts.hasOwnProperty("limit") ? opts["limit"] : 10;
    opt["limits"] = opts.hasOwnProperty("limits") ? opts["limits"] : [10,30,50];
    if(opts.hasOwnProperty("toolbar")) opt["toolbar"] = opts["toolbar"];
    if(opts.hasOwnProperty("defaultToolbar")) opt["defaultToolbar"] = opts["defaultToolbar"];
    if(opts.hasOwnProperty("height")) opt["height"] = opts["height"];

    var result = table.render(opt);
    return result;
}
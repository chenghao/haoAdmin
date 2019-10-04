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
 * @param callback
 */
function confirmDel(url, param, callback, title, notJointBaseServer) {
    if(!title) title = '确定删除此数据吗？';
    _confirm(title, url, param, callback, 'DELETE', notJointBaseServer);
}

/**
 * 新增时的提示框
 * @param url
 * @param param
 * @param callback
 */
function confirmAdd(url, param, callback, title, notJointBaseServer) {
    if(!title) title = '确定新增此数据吗？';
    _confirm(title, url, param, callback, 'POST', notJointBaseServer);
}

/**
 * 编辑时的提示框
 * @param url
 * @param param
 * @param callback
 */
function confirmEdit(url, param, callback, title, notJointBaseServer) {
    if(!title) title = '确定编辑此数据吗？';
    _confirm(title, url, param, callback, 'PUT', notJointBaseServer);
}

/**
 * 确认
 * @param title
 * @param url
 * @param param
 * @param callback
 * @param method
 * @private
 */
function _confirm(title, url, param, callback, method, notJointBaseServer) {
    layer.confirm(title, {
        offset: '65px',
        skin: 'layui-layer-admin'
    }, function (i) {
        layer.close(i);

        jqueryAjax(url, param, function (data) {
            if(callback){
                callback(data);
            }
        }, method, false, false, notJointBaseServer);
    });
}

////////////////////////////////////////////////////////////////////////////////////////////

/**
 * 打开窗口
 * @param area
 * @param title
 * @param id
 * @param callback
 */
function openWindow(area, title, id, callback) {
    layer.open({
        skin: 'layui-layer-admin',
        type: 1,
        area: area,
        offset: '65px',
        title: title,
        content: $(id).html(),
        success: function (layero, index) {
            $(layero).children('.layui-layer-content').css('overflow', 'visible');

            if(callback){
                callback();
            }
        }
    });
}

////////////////////////////////////////////////////////////////////////////////////////////
function jqueryAjaxGET(url, param, callback, notLoad, hideSuccessMsg, notJointBaseServer) {
    jqueryAjax(url, param, callback, "GET", notLoad, hideSuccessMsg, notJointBaseServer)
}
function jqueryAjaxPOST(url, param, callback, notLoad, hideSuccessMsg, notJointBaseServer) {
    jqueryAjax(url, param, callback, "POST", notLoad, hideSuccessMsg, notJointBaseServer)
}
function jqueryAjaxPUT(url, param, callback, notLoad, hideSuccessMsg, notJointBaseServer) {
    jqueryAjax(url, param, callback, "PUT", notLoad, hideSuccessMsg, notJointBaseServer)
}
function jqueryAjaxDELETE(url, param, callback, notLoad, hideSuccessMsg, notJointBaseServer) {
    jqueryAjax(url, param, callback, "DELETE", notLoad, hideSuccessMsg, notJointBaseServer)
}

function jqueryAjax(url, param, callback, method, notLoad, hideSuccessMsg, notJointBaseServer) {
    if(!notLoad){ // 为true时就不显示等待框
        loadWait();
    }
    if(!notJointBaseServer){
        url = layui.config.base_server + url;
    }

    $.ajax({
        url: url,
        type: method ? method : "get",
        data: param ? param : {},
        dataType: "json",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Bearer ' + layui.config.getToken());
        },
        success: function (data) {
            /*console.log("==================")
            console.log(url);
            console.log(data);
            console.log("==================")*/
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
            'Authorization': 'Bearer ' + layui.config.getToken()
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
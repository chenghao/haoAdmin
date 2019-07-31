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
 * @param admin
 * @param callback
 */
function confirmDel(url, param, admin, callback) {
    _confirm('确定删除此数据吗？', url, param, admin, callback, 'DELETE');
}
function confirmDel(title, url, param, admin, callback) {
    _confirm(title, url, param, admin, callback, 'DELETE');
}

/**
 * 新增时的提示框
 * @param url
 * @param param
 * @param admin
 * @param callback
 */
function confirmAdd(url, param, admin, callback) {
    _confirm('确定新增此数据吗？', url, param, admin, callback, 'POST');
}
function confirmAdd(title, url, param, admin, callback) {
    _confirm(title, url, param, admin, callback, 'POST');
}

/**
 * 编辑时的提示框
 * @param url
 * @param param
 * @param admin
 * @param callback
 */
function confirmEdit(url, param, admin, callback) {
    _confirm('确定编辑此数据吗？', url, param, admin, callback, 'PUT');
}
function confirmEdit(title, url, param, admin, callback) {
    _confirm(title, url, param, admin, callback, 'PUT');
}

/**
 * 确认
 * @param title
 * @param url
 * @param param
 * @param admin
 * @param callback
 * @param method
 * @private
 */
function _confirm(title, url, param, admin, callback, method) {
    layer.confirm(title, {
        skin: 'layui-layer-admin'
    }, function (i) {
        layer.close(i);

        _req(url, param, admin, function (data) {
            if(callback){
                callback(data);
            }
        }, method);
    });
}
////////////////////////////////////////////////////////////////////////////////////////////

/**
 * 新增请求
 * @param url
 * @param param
 * @param admin
 * @param callback
 */
function reqAdd(url, param, admin, callback) {
    _req(url, param, admin, callback, "POST");
}

/**
 * 编辑请求
 * @param url
 * @param param
 * @param admin
 * @param callback
 */
function reqEdit(url, param, admin, callback) {
    _req(url, param, admin, callback, "PUT");
}

/**
 * 获取请求
 * @param url
 * @param param
 * @param admin
 * @param callback
 */
function reqGet(url, param, admin, callback) {
    _req(url, param, admin, callback, "GET");
}
function reqGet(url, param, admin, callback, hideSuccessMsg) {
    _req(url, param, admin, callback, "GET", hideSuccessMsg);
}

/**
 * 请求
 * @param url
 * @param param
 * @param admin
 * @param callback
 * @param method
 */
function _req(url, param, admin, callback, method, hideSuccessMsg, hideLoad) {
    if(!hideLoad){
        loadWait();
    }
    admin.req(url, param, function (data) {
        closeLoadWait();
        admin.removeLoading();  // 移除页面加载动画

        if (data.code == 200) {
            if(!hideSuccessMsg){
                success(data.msg);
            }

            if(callback){
                callback(data);
            }
        } else {
            error(data.msg);
        }
    }, method);
}

////////////////////////////////////////////////////////////////////////////////////////////

/**
 * 打开窗口
 * @param admin
 * @param area
 * @param title
 * @param id
 * @param callback
 */
function openWindow(admin, area, title, id, callback, jq) {
    admin.open({
        type: 1,
        area: area,
        offset: '65px',
        title: title,
        content: jq('#' + id).html(),
        success: function (layero, index) {
            jq(layero).children('.layui-layer-content').css('overflow', 'visible');

            if(callback){
                callback();
            }
        }
    });
}

////////////////////////////////////////////////////////////////////////////////////////////

function jqueryAjax(jquery, url, param, callback, method, notLoad, hideSuccessMsg) {
    if(!notLoad){ // 为true时就不显示等待框
        loadWait();
    }

    jquery.ajax({
        url: url,
        type: method ? method : "get",
        data: param ? param : {},
        dataType: "json",
        success: function (data) {
            if(data.code == 200){
                if(!hideSuccessMsg) success(data.msg);

                if(callback) callback(data);
            } else {
                error(data.msg);
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(jqXHR)
            console.log(textStatus)
            console.log(errorThrown)
        },
        complete: function () {
            closeLoadWait();
        }
    });
}
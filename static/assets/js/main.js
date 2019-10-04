layui.config({
    base: 'assets/module/'
}).extend({
    formSelects: 'formSelects/formSelects-v4',
    treetable: 'treetable-lay/treetable',
    dropdown: 'dropdown/dropdown',
    notice: 'notice/notice',
    step: 'step-lay/step',
    dtree: 'dtree/dtree',
    citypicker: 'city-picker/city-picker',
    tableSelect: 'tableSelect/tableSelect'
}).use(['layer', 'element', 'config', 'index', 'admin', 'laytpl'], function () {
    var $ = layui.jquery;
    var layer = layui.layer;
    var element = layui.element;
    var config = layui.config;
    var index = layui.index;
    var admin = layui.admin;
    var laytpl = layui.laytpl;

    // 检查是否登录
    if (!config.getToken()) {
        return location.replace('login.html');
    }

    // *************************************************************************************
    // 默认设置蓝色主题
    initTheme("theme-blue");
    function initTheme(themeColor){
        if(!themeColor) themeColor = "theme-blue";
        var mTheme = layui.data(config.tableName).theme;
        var theme = mTheme ? mTheme : themeColor;
        if(themeColor != mTheme) admin.changeTheme(theme);
    }
    // 默认设置关闭页脚
    initFooter(false);
    function initFooter(footer){
        var openFooter = layui.data(config.tableName).openFooter;
        var checked = openFooter == undefined ? footer : openFooter;
        if(footer != openFooter){
            $('#setFooter').prop('checked', checked);
            layui.data(config.tableName, {key: 'openFooter', value: checked});
            checked ? $('body.layui-layout-body').removeClass('close-footer') : $('body.layui-layout-body').addClass('close-footer');
        }
    }
    // *************************************************************************************

    // 获取用户信息
    jqueryAjaxGET("sys/user/info", {}, function (data) {
        admin.removeLoading();  // 移除页面加载动画

        $('#huName').text(data.data.nick_name);
    }, true, true);

    // 加载侧边栏
    jqueryAjaxGET("sys/menu/user_menu", {}, function (data) {
        laytpl(sideNav.innerHTML).render(data.data, function (html) {
            $('.layui-layout-admin .layui-side .layui-nav').html(html);
            element.render('nav');
        });
        index.regRouter(data.data);  // 注册路由
        index.loadHome({  // 加载主页
            url: '#/welcome',
            name: '<i class="layui-icon layui-icon-home"></i>'
        });
    }, true, true);

});

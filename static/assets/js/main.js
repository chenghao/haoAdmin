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

    // 获取用户信息
    _req("sys/user/info", {}, admin, function (data) {
        $('#huName').text(data.data.nick_name);
    }, "GET", true, true);

    // 加载侧边栏
    _req("sys/menu/user_menu", {}, admin, function (data) {
        laytpl(sideNav.innerHTML).render(data.data, function (html) {
            $('.layui-layout-admin .layui-side .layui-nav').html(html);
            element.render('nav');
        });
        index.regRouter(data.data);  // 注册路由
        index.loadHome({  // 加载主页
            url: '#/welcome',
            name: '<i class="layui-icon layui-icon-home"></i>'
        });
    }, "GET", true, true);

});

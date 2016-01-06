$('nav a').css('color', '#FFF');
$('ul.dropdown-menu a').css('color', '#000');

$(document).ready(function(){
    $(document).off('click.bs.dropdown.data-api');
});

// 修改头像
$('#navbar img').attr('src',"{{ url_for('static', filename='uploads/avatars/xxx') }}".replace('xxx', "{{ g.user.avatar }}"));

// 添加导航栏动画
var elem = document.querySelector("nav");
var headroom = new Headroom(elem, {
  "tolerance": 5,
  "offset": 500,
});
headroom.init();
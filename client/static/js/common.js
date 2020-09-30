$(document).ready(function () {
    //檢測ie 6789
    if (!(/msie [6|7|8|9]/i.test(navigator.userAgent))) {
        window.scrollReveal = new scrollReveal({
            reset: true
        });
    }
    // 彈窗回復評論
    var list = document.getElementsByClassName('replyComment');
    for (var i of list) {
        i.addEventListener("click", function (ev) {
            ev.preventDefault();
            var txt=  "請輸入回復：";
            window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.input,{
                onOk:function(reply){
                    console.log(reply);
                }
            });
        }, false);
    }

    /*nav show or hide*/
    $('.nav>li').hover(function () {
        $(this).children('ul').stop(true, true).show(400);
    }, function () {
        $(this).children('ul').stop(true, true).hide(400);
    });
    /*search*/
    $('.search_ico').click(function () {
        $('.search_bar').toggleClass('search_open');
        if ($('#keyboard').val().length > 2) {
            $('#keyboard').val('');
            $('#searchform').submit();
        } else {
            return false;
        }
    });
    /*banner*/
    $('#banner').easyFader();

    /*topnav select*/
    var obj = null;
    var allMenu = document.getElementById('topnav').getElementsByTagName('a');
    // console.log(allMenu);
    obj = allMenu[0];
    for (i = 1; i < allMenu.length; i++) {
        if (window.location.href.indexOf(allMenu[i].href) >= 0) {
            obj = allMenu[i];
        }
    }
    obj.id = 'topnav_current';

    /*mnav dl open*/
    var oH2 = document.getElementsByTagName('h2')[0];
    var oUl = document.getElementsByTagName('dl')[0];
    oH2.onclick = function () {
        var style = oUl.style;
        style.display = style.display == 'block' ? 'none' : 'block';
        oH2.className = style.display == 'block' ? 'open' : '';
    };
    //菜单点击效果
    $('.list_dt').on('click', function () {
        $('.list_dd').stop();
        $(this).siblings('dt').removeAttr('id');
        if ($(this).attr('id') == 'open') {
            $(this).removeAttr('id').siblings('dd').slideUp();
        } else {
            $(this).attr('id', 'open').next().slideDown().siblings('dd').slideUp();
        }
    });

    //设置固定关注我们

    if ($('#follow-us')) {
        var followUsPosition = $('#follow-us').offset().top;
        window.onscroll = function () {
            var nowPosition = document.documentElement.scrollTop;
            if (nowPosition - followUsPosition > 0) {
                setTimeout(function () {
                    $('#follow-us').attr('class', 'guanzhu gd');
                }, 150);
            } else {
                $('#follow-us').attr('class', 'guanzhu');
            }
        };
    }


    //回到顶部
    // browser window scroll (in pixels) after which the "back to top" link is shown
    var offset = 300,
        //browser window scroll (in pixels) after which the "back to top" link opacity is reduced
        offset_opacity = 1200,
        //duration of the top scrolling animation (in ms)
        scroll_top_duration = 700,
        //grab the "back to top" link
        $back_to_top = $('.cd-top');

    //hide or show the "back to top" link
    $(window).scroll(function () {
        ($(this).scrollTop() > offset) ? $back_to_top.addClass('cd-is-visible'): $back_to_top.removeClass('cd-is-visible cd-fade-out');
        if ($(this).scrollTop() > offset_opacity) {
            $back_to_top.addClass('cd-fade-out');
        }
    });
    //smooth scroll to top
    $back_to_top.on('click', function (event) {
        event.preventDefault();
        $('body,html').animate({
            scrollTop: 0,
        }, scroll_top_duration);
    });

});


function makeHeader(blog_username, username){
    //blog_username 當前訪問部落格的板住
    //username   登陸的用戶

    //部落格作者-用户信息url
    var user_info_url = '/' + blog_username + '/' + 'info'
    //登陸用戶發文章url
    if (username){
        var topic_release_url = '/' + username + '/' + 'topic/release'
    }else{
        //沒有登錄狀態 跳回登入
        var topic_release_url = '/login'
    }

    //訪問部落格版主文章
    var user_topics_url = '/' + blog_username + '/' + 'topics'

    var header_body = ''
    header_body += '<header id="header">';
    header_body += '<div class="menu">';
    header_body += ' <nav class="nav" id="topnav"> ';
    header_body += '<h1 class="logo"><a href="/index"> ' + blog_username + '的部落格</a></h1>';
    header_body += '<li><a href="/index">網站首頁</a></li>';
    header_body += '<li>';
    header_body += '<a href=' + '"' + user_topics_url + '"' + '>個人文章列表</a>';
    header_body += '<ul class="sub-nav">';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=tec"' + '>技術類文章</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=no-tec"' + '>非技術類文章</a></li>';
    header_body += '</ul>';
    header_body += '</li>';
    header_body += '<li><a href=' + '"' + user_info_url + '"' + '>個人簡介</a> </li>';
    header_body += '<li><a href=' + '"' + topic_release_url + '"' + '>發表文章</a> </li>';
    header_body += '</nav>';
    header_body += '</div>';
    if (username){
        header_body += '<li><a href= /' + username + '/change_info id="change_info" target="_blank">修改個人訊息</a></li>';
        //header_body += '<li><a href="/" id="login_out" target="_blank">登出</a></li>';
        header_body += '<li><span id="login_out" target="_blank">登出</span></li>';
    }else{
        header_body += '<a href="/login" id="login" target="_blank">登入</a>';
        header_body += '<a href="registe" id="register" target="_blank">註冊</a>';
    }
    header_body += '</header>';

    return header_body
}


function loginOut(){

    $('#login_out').on('click', function(){

            if(confirm("確定登出嗎?")){
                window.localStorage.removeItem('dnblog_token');
                window.localStorage.removeItem('dnblog_user');
                window.location.href= '/index';
            }
        }
    )

}

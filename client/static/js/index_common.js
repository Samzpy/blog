function makeindex(username){
    //blog_username 當前訪問部落格的板住
    //username   登陸的用戶

    //部落格作者-用户信息url
    if (username){
        var topic_release_url = '/' + username + '/' + 'topic/release'
    }else{
        //没有登陸狀態跳回登入
        var topic_release_url = '/login'
    }

    //訪問版主文章
    if (username){
    var user_topics_url = '/' + username + '/' + 'topics'
    }else{
        var user_topics_url  = '/login'

    }
    if (username){
    var user_info_url = '/' + username + '/' + 'info'
    }else{
        var user_info_url = '/login'

    }

    var header_body = ''
    header_body += '<div class="menu">';
    header_body += ' <nav class="nav" id="topnav"> ';
    header_body += '<h1 class="logo"><a href="/index"> 煙花部落格</a></h1>';
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
        header_body += '<li><a href= /' + username + '/change_info id="change_info" target="_blank" style="top:2px" >修改個人訊息</a></li>';
        //header_body += '<li><a href="/" id="login_out" target="_blank">登出</a></li>';
        header_body += '<li><span id="login_out" target="_blank" style="top:2px">登出</span></li>';
    }else{
        header_body += '<a href="/login" id="login" target="_blank" style="top:2px">登入</a>';
        header_body += '<a href="/register" id="register" target="_blank" style="top:2px">註冊</a>';
    }

    return header_body
}


function loginOut(){

    $('#login_out').on('click', function(){

            if(confirm("確定登出嗎？")){
                window.localStorage.removeItem('dnblog_token');
                window.localStorage.removeItem('dnblog_user');
                window.location.href= '/index';
            }
        }
    )

}

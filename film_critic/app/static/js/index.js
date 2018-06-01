$(document).ready(function () {

    var $slide_content = $('.slide-content');
    // 轮播索引 从第 1 开始
    var slide_index = 1;
    var slide_index_max = parseInt($slide_content.attr('data-slide-index-max'));

    // 轮播宽度
    var screening_width = 700;

    // 控制按钮
    var $pre_btn = $('.screening-head .pre-btn');
    var $next_btn = $('.screening-head .next-btn');

    // 鼠标放置停止轮播
    var $slide_items = $('.slide-content .ui-slide-item, .screening-head .pre-btn, .screening-head .next-btn');

    var is_clickable = true;

    // 初始化初始位置
    $slide_content.css('left', -700);

    $pre_btn.click(function () {
        if (is_clickable)
            slide_index--;
        else
            return false;
        is_clickable = false;
        if (slide_index <= 0)
            $('.ui-slide-index').text(slide_index_max);
        else
            $('.ui-slide-index').text(slide_index);
        var animateLength = slide_index * -screening_width + "px";
        $slide_content.animate({ 'left': animateLength }, "slow", function () {
            if (slide_index <= 0) {
                slide_index = slide_index_max;
                $slide_content.css('left', '-' + slide_index_max * screening_width + 'px');
            }
            is_clickable = true;
        });
    });

    $next_btn.click(function () {
        if (is_clickable)
            slide_index++;
        else
            return false;
        is_clickable = false;
        if (slide_index >= slide_index_max + 1)
            $('.ui-slide-index').text(1);
        else
            $('.ui-slide-index').text(slide_index);
        var animateLength = slide_index * -screening_width + "px";
        $slide_content.animate({ 'left': animateLength }, "slow", function () {
            if (slide_index >= slide_index_max + 1) {
                $slide_content.css('left', '-' + screening_width + 'px');
                slide_index = 1;
                $('.ui-slide-index').text(slide_index);
            }
            is_clickable = true;
        });
    });

    var auto_move = function () {
        $next_btn.trigger('click');
    };

    var t = setInterval(auto_move, 15000);

    $slide_items.hover(function () {
        clearInterval(t);
    }, function () {
        t = setInterval(auto_move, 15000);
    });

    // 第二个轮播控制

    var $slider_container = $('.slider .slider-container');
    var $slide_page = $('.slide-page');

    var $pre_btn2 = $('.slide-ctrl .pre-btn');
    var $next_btn2 = $('.slide-ctrl .next-btn');

    // screening_width = 700
    // is_clickable = true

    // 初始化
    $slider_container.css('width', '4900px');
    $slider_container.css('left', '-700px');

    var dot_color_normal = '#D8D8D8';
    var dot_color_active = '#6198D7';

    $('.slide-ctrl [data-index=' + '1' + ']').css('background-color', dot_color_active);
    var slide_index2 = 1;

    $pre_btn2.click(function () {
        if (is_clickable)
            slide_index2--;
        else
            return false;
        is_clickable = false;
        if (slide_index2 <= 0) {
            $('.slide-ctrl [data-index=' + 5 + ']').css('background-color', dot_color_active);
            $('.slide-ctrl [data-index=' + 1 + ']').css('background-color', dot_color_normal);
        }
        else {
            $('.slide-ctrl [data-index=' + slide_index2 + ']').css('background-color', dot_color_active);
            $('.slide-ctrl [data-index=' + (slide_index2 + 1) + ']').css('background-color', dot_color_normal);
        }
        var animate_length = slide_index2 * -screening_width + "px";
        $slider_container.animate({ 'left': animate_length }, "slow", function () {
            if (slide_index2 <= 0) {
                slide_index2 = 5;
                $slider_container.css('left', '-' + 5 * screening_width + 'px');
            }
            is_clickable = true;
        });
    });

    $next_btn2.click(function () {
        if (is_clickable)
            slide_index2++;
        else
            return false;
        is_clickable = false;
        if (slide_index2 >= 6) {
            $('.slide-ctrl [data-index=' + 1 + ']').css('background-color', dot_color_active);
            $('.slide-ctrl [data-index=' + 5 + ']').css('background-color', dot_color_normal);
        }
        else {
            $('.slide-ctrl [data-index=' + slide_index2 + ']').css('background-color', dot_color_active);
            $('.slide-ctrl [data-index=' + (slide_index2 - 1) + ']').css('background-color', dot_color_normal);
        }
        var animate_length = slide_index2 * -screening_width + "px";
        $slider_container.animate({ 'left': animate_length }, "slow", function () {
            if (slide_index2 >= 6) {
                slide_index2 = 1;
                $slider_container.css('left', '-' + screening_width + 'px');
            }
            is_clickable = true;
        });
    });

    var auto_move2 = function () {
        $next_btn2.trigger('click');
    };

    var t2 = setInterval(auto_move2, 30000);

    $('.slider-container .slide-item').hover(function () {
        clearInterval(t2);
    }, function () {
        t2 = setInterval(auto_move2, 30000);
    });

    // 热门电影悬停弹出框
    var hot_movie_popover_content = $('.slide-item .hot-movie-popover-content');

    var pop_content = hot_movie_popover_content.html();

    // $('.slide-item').hover(function () {
    //     hot_movie_popover_content.css('display', 'block');
    //     console.log('debug')
    // }, function () {
    //
    // })
});
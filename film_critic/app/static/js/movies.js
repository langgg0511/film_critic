$(document).ready(function () {
    $(".evaluate-ul li a").click(function () {
        var evaluate = parseInt($(this).html());
        // var user_id = {{ user.id }};
//            alert("评分成功");
//         var movie_id = document.getElementById("{{ movie.id }}").attributes["id"].value;
        var movie_id = 1;
        var user_id = 1;
        // var movie_id = parseInt($("#{{ movie.id }}").id);
        $.ajax({
            url: "{{ url_for('main.users_movies_evaluate') }}",
            type: "GET",
            data: "movie_id=" + movie_id + "evaluate=" + evaluate,
            dataType: "json",
            success: function (res) {
                if (res.ok == 1) {
                    $("#show_col_msg").empty();
                    $("#show_col_msg").append("评分成功！");
                } else {
                    $("#show_col_msg").empty();
                    $("#show_col_msg").append("您已经评分！");
                }
            }
        })
        alert("评分成功")
    });
    $(".evaluate-ul li a").mouseover(function () {

        //判断是全星点还是半星点，修改当前标签的父标签li的class为对应的星星图像
        if (parseInt($(this).html()) % 2 == 1) {
            $(this).parent().attr("class", "halfStar");
            switch (parseInt($(this).html())) {
                case 1 :
                    document.getElementById("ratingText").innerHTML = "很差";
                    break;
                case 3 :
                    document.getElementById("ratingText").innerHTML = "较差";
                    break;
                case 5 :
                    document.getElementById("ratingText").innerHTML = "还行";
                    break;
                case 7 :
                    document.getElementById("ratingText").innerHTML = "推荐";
                    break;
                case 9:
                    document.getElementById("ratingText").innerHTML = "力荐";
                    break;
                default :
                    document.getElementById("ratingText").innerHTML = "";
            }
        }
        else {
            $(this).parent().attr("class", "fullStar");
            switch (parseInt($(this).html())) {
                case  2 :
                    document.getElementById("ratingText").innerHTML = "很差";
                    break;
                case  4 :
                    document.getElementById("ratingText").innerHTML = "较差";
                    break;
                case  6 :
                    document.getElementById("ratingText").innerHTML = "还行";
                    break;
                case  8 :
                    document.getElementById("ratingText").innerHTML = "推荐";
                    break;
                case  10 :
                    document.getElementById("ratingText").innerHTML = "力荐";
                    break;
                default :
                    document.getElementById("ratingText").innerHTML = "";
            }
        }

        //对前方的星星进行处理，遍历前方的li使背景图均变为全星
        var prev = $(this).parent();
        for (var i = 0; i <= (parseInt($(this).html()) / 2) - 1; i++) {
            prev.prev().attr("class", "fullStar");
            prev = prev.prev();
        }
        //对后方星星进行处理，遍历后面的li使背景图均变为空星
        var after = $(this).parent();
        for (var i = 0; i <= (5 - parseInt($(this).html()) / 2) - 1; i++) {
            after.next().attr("class", "emptyStar");
            after = after.next();
        }

    });

});




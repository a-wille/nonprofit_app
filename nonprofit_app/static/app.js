
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function sign_in() {
    $("#login_window").show().kendoWindow({
                content: {
                    url: 'login'
                },
                width: 300,
                height: 400,
            });
            var win = $("#login_window").data("kendoWindow");
            win.open();
            win.center();
};

function redirect() {
    window.location.replace('http://127.0.0.1:8000/client/user_manual/');
}

function create_account() {
    $("#account_window").kendoWindow({
        content: {
            url: 'create'
        },
        width: 300,
        height: 600,
    });
    var win = $("#account_window").data("kendoWindow");
    win.open();
    win.center();
};

function logout() {
    $.ajax({
        type: "POST",
        url: "/client/logout/",
        headers: {'X-CSRFToken': csrftoken},
        contentType: "application/x-www-form-urlencoded",
        success: function(response) {
            location.reload();
        }
    });
}

$(window).resize(function () {
    $('.login-window').css({
        position: 'absolute',
        left: ($(window).width() - $('.login-window').outerWidth()) / 2,
        top: ($(window).height() - $('.login-window').outerHeight()) / 2,
    });
});

// $(window).resize(function () {
//     $('.account-window').css({
//         position: 'absolute',
//         left: ($(window).width() - $('.account-window').outerWidth()) / 2,
//         top: ($(window).height() - $('.account-window').outerHeight()) / 2,
//     });
// });

$(document).ready(function() {
    $('#account_creation').kendoButton({
        click: function(e) {
            e.preventDefault();
            create_account();
        }
    });
    $('#account_signin').kendoButton({
        click: function(e) {
            e.preventDefault();
            sign_in();
        }
    });
    $('#user_manual').kendoButton({
        click: function(e) {
            e.preventDefault();
            redirect();
        }
    });

    $('#account_logout').kendoButton({
        click: logout
    })
    // var tabStrip = $("#tabstrip").kendoTabStrip({
    //     animation:  {
    //         open: {
    //             effects: "fadeIn"
    //         }
    //     },
    //     contentUrls: [
    //         'home',
    //         'events',
    //         'donate',
    //         'volunteer',
    //         'about'
    //     ]
    // }).data("kendoTabStrip");
    // tabStrip.select(0);

    $.ajax({
        type: "POST",
        url: "/client/check_admin/",
        headers: {'X-CSRFToken': csrftoken},
        contentType: "application/x-www-form-urlencoded",
        success: function(response) {
            if(response == "success"){
                var tabStrip = $("#tabstrip").kendoTabStrip({
                    animation:  {
                        open: {
                            effects: "fadeIn"
                        }
                    },
                    contentUrls: [
                        'home',
                        'events',
                        'donate',
                        'volunteer',
                        'all_events',
                        "all_volunteers"
                    ]
                }).data("kendoTabStrip");
                tabStrip.select(0);
            } else {
                var tabStrip = $("#tabstrip").kendoTabStrip({
                    animation:  {
                        open: {
                            effects: "fadeIn"
                        }
                    },
                    contentUrls: [
                        'home',
                        'events',
                        'donate',
                        'volunteer',
                        'about'
                    ]
                }).data("kendoTabStrip");
                tabStrip.select(0);
            }
        }
    });
});

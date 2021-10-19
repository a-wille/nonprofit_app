
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
    });
};

function create_account() {
    $("#account_window").show().kendoWindow({
        content: {
            url: 'create'
        },
    });
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

$(window).resize(function () {
    $('.account-window').css({
        position: 'absolute',
        left: ($(window).width() - $('.account-window').outerWidth()) / 2,
        top: ($(window).height() - $('.account-window').outerHeight()) / 2,
    });
});

$(document).ready(function() {
    $('#account_creation').kendoButton({
        click: create_account
    });
    $('#account_signin').kendoButton({
        click: sign_in
    });
    $('#account_logout').kendoButton({
        click: logout
    })
    $("#tabstrip").kendoTabStrip({
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
    });
});

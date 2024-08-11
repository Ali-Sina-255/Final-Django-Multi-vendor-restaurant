
document.addEventListener('htmx:afterRequest', function(event) {
    if (event.detail.xhr.responseJSON && event.detail.xhr.responseJSON.redirect_url) {
        window.location.href = event.detail.xhr.responseJSON.redirect_url;
    }
});

window.location.href = 'accounts/menu_builder/';

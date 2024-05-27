function sort_by(sortType) {
    var query = get_url_parameter('query');
    var newUrl = '/search/information?query=' + query + '&sort_by=' + sortType;
    window.location.href = newUrl;
}

function get_url_parameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

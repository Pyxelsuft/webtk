window.onload = function() {
    var temp_title = ' Pixelsuft WebTK Example!';

    function title_change() {
        temp_title = temp_title.substr(1) + temp_title[0];
        py_title(temp_title).then(function() {
            setTimeout(title_change, temp_title[0] == 'P' ? 3000 : 500);
        });
    }
    title_change();

    py_print('Hello', 'world');
}

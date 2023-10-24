window.onload = function() {
    var temp_title = ' Pixelsuft WebTK Example!';

    function title_change() {
        temp_title = temp_title.substr(1) + temp_title[0];
        py_title(temp_title).then(function() {
            setTimeout(title_change, temp_title[0] == 'P' ? 3000 : 200);
        });
    }
    title_change();

    py_print('Hello', 'world');

    document.addEventListener('keydown', function(e) {
        if (e.keyCode == 27 || e.keyCode == 81)  // ESCape or Q
            py_stop();
    });

    document.getElementById('button0').addEventListener('click', function(e) {
        py_screen().then(function(e) {
            document.getElementById('screen0').src = e[0];
        });
    });

    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });
}

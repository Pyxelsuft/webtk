window.onload = function() {
    var temp_title = ' Pixelsuft WebTK Example!';

    if (!window.py_title) {
        window.py_title = async function(new_title) {
            document.title = new_title;
        }

        window.py_print = async function(new_title) {
            console.log(new_title);
        }

        window.py_stop = async function(new_title) {
            window.close();
        }

        window.py_screen = async function(new_title) {
            // Blah Blah Blah
        }

        window.py_fetch = async function(new_title) {
            // Blah Blah Blah
        }
    }

    function title_change() {
        temp_title = temp_title.substr(1) + temp_title[0];
        if (temp_title[0] == ' ')
            return title_change();
        py_title(temp_title).then(function() {
            setTimeout(title_change, temp_title[0] == 'P' ? 3000 : 500);
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.keyCode == 27 || e.keyCode == 81)  // ESCape or Q
            py_stop();
    });

    document.getElementById('button0').addEventListener('click', function(e) {
        py_screen().then(function(e) {
            document.getElementById('screen0').src = e[0];
        });
    });

    document.getElementById('button1').addEventListener('click', function(e) {
        py_fetch().then(function(e) {
            console.log(e, e.followers);
            document.getElementById('text0').textContent = `Pixelsuft: ${e.fws} followers, ${e.fwg} following, ${e.rps} repositories`;
        });
    });

    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });

    document.getElementById('screen0').addEventListener('dragstart', function(e) {
        e.preventDefault();
    });

    title_change();

    py_print('Hello', 'world');
}

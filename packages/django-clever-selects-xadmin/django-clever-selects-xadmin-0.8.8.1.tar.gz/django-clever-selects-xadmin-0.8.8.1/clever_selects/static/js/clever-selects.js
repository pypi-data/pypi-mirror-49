function loadChildChoices(parentField, child) {
    var valueField = child;
    var ajaxUrl = valueField.getAttribute("ajax_url");
    var emptyLabel = valueField.getAttribute('empty_label') || '--------';

    // Set up our HTTP request
    var xhr = new XMLHttpRequest();
    xhr.open('GET', ajaxUrl + "?field=" + valueField.getAttribute("name") + "&parent_field=" + parentField.getAttribute("name") + "&parent_value=" + parentField.value, true);

    xhr.setRequestHeader('Accept', 'application/json');
    xhr.timeout = 5;
    xhr.withCredentials = true;

    // Setup our listener to process compeleted requests
    xhr.onreadystatechange = function () {

        // Only run if the request is complete
        if (xhr.readyState !== 4) return;

        // Process our return data
        if (xhr.status >= 200 && xhr.status < 300) {
            // What do when the request is successful
            var options = JSON.parse(xhr.responseText);
            var optionsHTML = "";

            if (typeof valueField.selectize !== 'undefined') {
                // select control initiated by selectize.js
                valueField.selectize.clear(true);
                valueField.selectize.clearOptions();

                for (let i = 0, len = options.length; i < len; i++) {
                    valueField.selectize.addOption({value:options[i][0],text:options[i][1]});
                }
            }
            else {
                // normal select control
                if (!child[0].hasAttribute("multiple")) {
                    optionsHTML += '<option value="">' + emptyLabel + '</option>';
                }

                for (let i = 0, len = options.length; i < len; i++) {
                    optionsHTML += '<option value="' + options[i][0] + '">' + options[i][1] + '</option>';
                }
                valueField.innerHTML = optionsHTML;
            }

            valueField.dispatchEvent(new Event("change"));
            valueField.dispatchEvent(new Event("load"));
            valueField.dispatchEvent(new Event("liszt:updated")); // support for chosen versions < 1.0.0
            valueField.dispatchEvent(new Event("chosen:updated")); // support for chosen versions >= 1.0.0

        } else {
            // What to do when the request has failed
            console.log('error', xhr);
        }
    };
    xhr.send();
}

function loadAllChainedChoices(parentField) {
    var chained_ids = parentField.getAttribute('chained_ids').split(",");

    for (let i = 0, len = chained_ids.length; i < len; i++) {
        var child = document.getElementById(chained_ids[i]);
        loadChildChoices(parentField, child);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var parentFields = document.querySelectorAll(".chained-parent-field");

    for (let i = 0, len = parentFields.length; i < len; i++) {
        if ( parentFields[i].classList.contains('chzn-done') ) {
            $(parentFields[i]).change(function() {
                loadAllChainedChoices(this);
            });
        } else {
            parentFields[i].addEventListener("change", function() { loadAllChainedChoices(this); });
        }
    }
});
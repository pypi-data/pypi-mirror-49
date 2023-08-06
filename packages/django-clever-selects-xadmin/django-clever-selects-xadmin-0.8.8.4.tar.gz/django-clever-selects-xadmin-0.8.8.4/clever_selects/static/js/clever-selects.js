function loadChildChoices(parentField, child) {
    var valueField = child;
    var ajaxUrl = valueField.getAttribute("ajax_url");
    var emptyLabel = valueField.getAttribute('empty_label') || '--------';

    // Set up our HTTP request
    var xhr = new XMLHttpRequest();
    xhr.open('GET', ajaxUrl + "?field=" + valueField.getAttribute("name") + "&parent_field=" + parentField.getAttribute("name") + "&parent_value=" + parentField.value);

    xhr.setRequestHeader('Accept', 'application/json');
    xhr.timeout = 5000;
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

            var event1, event2, event3, event4;
            if (typeof(Event) === 'function') {
                event1 = new Event('change');
                event2 = new Event('load');
                event3 = new Event('liszt:updated');
                event4 = new Event('chosen:updated');

            } else {
                event1 = document.createEvent('Event');
                event2 = document.createEvent('Event');
                event3 = document.createEvent('Event');
                event4 = document.createEvent('Event');

                event1.initEvent('change', true, true);
                event2.initEvent('load', true, true);
                event3.initEvent('liszt:updated', true, true);
                event4.initEvent('chosen:updated', true, true);
            }

            valueField.dispatchEvent(event1);
            valueField.dispatchEvent(event2);
            valueField.dispatchEvent(event3); // support for chosen versions < 1.0.0
            valueField.dispatchEvent(event4); // support for chosen versions >= 1.0.0

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
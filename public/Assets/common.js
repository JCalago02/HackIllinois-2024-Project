// Function to parse URL parameters
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

document.addEventListener('DOMContentLoaded', function() {
    var colorPickerWrapper = document.getElementById('color-picker-wrapper');
    var commitGraphWrapper = document.getElementById('commit-graph-wrapper');
    var documentationBarWrapper = document.getElementById('documentation-bar-wrapper');
    var issueProgressWrapper = document.getElementById("issue-progress-wrapper");
    var defaultWrapper = document.getElementById("default-wrapper");

    var widgetParam = getUrlParameter('widget');
    console.log(widgetParam);
    console.log(defaultWrapper);

    // Show/hide widgets based on URL parameter
    if (widgetParam === 'colorPicker') {
        colorPickerWrapper.style.display = 'block';
    } else if (widgetParam === 'commitGraph') {
        commitGraphWrapper.style.display = 'block';
    } else if (widgetParam== 'documentationBar') {
        documentationBarWrapper.style.display = 'block';
    } else if (widgetParam=="isseProgress") {
        issueProgressWrapper.style.display = 'block';
    } else {
        defaultWrapper.style.display = 'block';
    }
});
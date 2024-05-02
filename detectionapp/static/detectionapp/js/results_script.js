// Inside
var currentPageInside = 1;
var itemsPerPageInside = 1;
showPageInside(currentPageInside);

function showPageInside(page) {
    var elementsInside = document.querySelectorAll('#result-details-inside .card-body');
    elementsInside.forEach(function(element) {
        element.style.display = 'none';
    });
    elementsInside[page - 1].style.display = 'block';

    var totalItemsInside = elementsInside.length;
    var totalPagesInside = Math.ceil(totalItemsInside / itemsPerPageInside);
    document.getElementById('page-info-inside').textContent = 'Page ' + page + '/' + totalPagesInside;
}

$('#prev-page-inside').click(function() {
    if (currentPageInside > 1) {
        currentPageInside--;
        showPageInside(currentPageInside);
    }
});

$('#next-page-inside').click(function() {
    var totalItemsInside = document.querySelectorAll('#result-details-inside .card-body').length;
    var totalPagesInside = Math.ceil(totalItemsInside / itemsPerPageInside);
    if (currentPageInside < totalPagesInside) {
        currentPageInside++;
        showPageInside(currentPageInside);
    }
});

// Outside
var currentPageOutside = 1;
var itemsPerPageOutside = 1;
showPageOutside(currentPageOutside);

function showPageOutside(page) {
    var elementsOutside = document.querySelectorAll('#result-details-outside .card-body');
    elementsOutside.forEach(function(element) {
        element.style.display = 'none';
    });
    elementsOutside[page - 1].style.display = 'block';

    var totalItemsOutside = elementsOutside.length;
    var totalPagesOutside = Math.ceil(totalItemsOutside / itemsPerPageOutside);
    document.getElementById('page-info-outside').textContent = 'Page ' + page + '/' + totalPagesOutside;
}

$('#prev-page-outside').click(function() {
    if (currentPageOutside > 1) {
        currentPageOutside--;
        showPageOutside(currentPageOutside);
    }
});

$('#next-page-outside').click(function() {
    var totalItemsOutside = document.querySelectorAll('#result-details-outside .card-body').length;
    var totalPagesOutside = Math.ceil(totalItemsOutside / itemsPerPageOutside);
    if (currentPageOutside < totalPagesOutside) {
        currentPageOutside++;
        showPageOutside(currentPageOutside);
    }
});
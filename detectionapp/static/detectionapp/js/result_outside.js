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
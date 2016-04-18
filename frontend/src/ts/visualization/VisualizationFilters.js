var VisualizationFilters = (function () {
    function VisualizationFilters() {
    }
    VisualizationFilters.currencyFilter = function (n) {
        if (n > 1000000000)
            return (n / 1000000000).toFixed(2) + " milli\u00E1rd Ft";
        if (n > 1000000)
            return (n / 1000000).toFixed(2) + " milli\u00F3 Ft";
        if (n > 1000)
            return (n / 1000).toFixed(2) + " ezer Ft";
        else
            return n + " Ft";
    };
    return VisualizationFilters;
})();
//# sourceMappingURL=VisualizationFilters.js.map
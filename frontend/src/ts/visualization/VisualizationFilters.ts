class VisualizationFilters {
    static currencyFilter(n: number) {
        if (n > 1000000000) return `${(n / 1000000000).toFixed(2)} milliárd Ft`;
        if (n > 1000000) return `${(n / 1000000).toFixed(2)} millió Ft`;
        if (n > 1000) return `${(n / 1000).toFixed(2)} ezer Ft`;
        else return `${n} Ft`;
    }
}
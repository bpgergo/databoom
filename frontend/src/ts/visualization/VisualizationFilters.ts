class VisualizationFilters {
    static currencyFilter(n: number) {
        if (n > 1000000000) return `${n / 1000000000} milliárd Ft`;
        if (n > 1000000) return `${n / 1000000} millió Ft`;
        if (n > 1000) return `${n / 1000} ezer Ft`;
        else return `${n} Ft`;
    } 
}
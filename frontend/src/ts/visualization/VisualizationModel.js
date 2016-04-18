var VisualizationModel = (function () {
    function VisualizationModel() {
        var _this = this;
        this.autocompleteValues = [
            'altalanos',
            'vedelem',
            'kozrend',
            'gazdasagi',
            'termeszetvedelem',
            'lakasepites',
            'egeszseg',
            'szabadido',
            'oktatas',
            'szocialis'
        ];
        this.data = [
            []
        ];
        $.getJSON('data/budget.json')
            .then(function (d) { return _this.budget = d; })
            .then(function () { return $.getJSON('data/functions.json'); })
            .then(function (d) { return _this.funcitons = d; }).then(function () {
            console.log(_this.budget.length);
            _this.data = _this.budget.filter(function (d) { return 0 < d.id && d.id <= 11; });
            _this.data = [_this.funcitons
                    .filter(function (d) { return 0 < d.id && d.id <= 11; })
                    .map(function (d) {
                    return {
                        id: d.id,
                        name: d.value,
                        amount: _this.budget
                            .filter(function (e) { return e.func_id.startsWith('0' + d.id); })
                            .reduce(function (a, b) { return a + parseFloat(b.value); }, 0)
                    };
                })];
        })
            .then(function () { return _this.onDataLoaded && _this.onDataLoaded({}); });
    }
    VisualizationModel.prototype.requestLevel = function (id) {
        var _this = this;
        if (id[0] !== '0')
            id = "0" + id;
        while (id[id.length - 1] === '0')
            id = id.slice(0, -1);
        var level = Math.floor(id.length / 2);
        return this.funcitons
            .filter(function (d) { return d.id.startsWith(id) && d.id.slice(d.id.length).split('').all(function (e) { return e == 0; }); })
            .map(function (d) {
            return {
                id: d.id,
                name: d.value,
                amount: _this.budget
                    .filter(function (e) { return e.func_id.startsWith(id); })
                    .reduce(function (a, b) { return a + parseFloat(b.value); }, 0)
            };
        });
    };
    return VisualizationModel;
})();
//# sourceMappingURL=VisualizationModel.js.map
/// <reference path="View.ts" />
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var VisualizationView = (function (_super) {
    __extends(VisualizationView, _super);
    function VisualizationView(_model) {
        _super.call(this);
        this._model = _model;
        this.html = "\n<div class=\"frame\">\n    \n</div>\n";
        this.currentLevel = 0;
        _model.onDataLoaded = this.showCurrentLevel.bind(this);
    }
    VisualizationView.prototype.showCurrentLevel = function (data) {
        var _this = this;
        if (data === void 0) { data = null; }
        // if (data === null) {
        data = this._model.data[0];
        // }
        // if (!data || !data.length) return;
        var sum = data.map(function (d) { return d.amount; }).reduce(function (a, b) { return a + b; }, 0);
        var divHeight = 334;
        var _a = [14, 34], labelBase = _a[0], labelStep = _a[1];
        var multiplier = divHeight / sum;
        var midPoints = [];
        var n = data.length;
        var t = data.map(function (d) { return d.amount; });
        var s = 0;
        for (var i = 0; i < n; ++i) {
            s = s + t[i];
            midPoints.push(s - t[i] + t[i] / 2);
        }
        this.$('.stack')
            .empty()
            .append(data
            .map(function (d, i) { return $('<div>', {
            class: 'block',
            css: {
                height: d.amount * multiplier,
                backgroundColor: VisualizationView.colors[i],
                top: data
                    .filter(function (d, j) { return j < i; })
                    .map(function (d) { return d.amount * multiplier; })
                    .reduce(function (a, b) { return a + b; }, 0),
                left: 0
            }
        }).on('click', _this.blockClicked.bind(_this, d.id)); }));
        this.$('.lines')
            .empty()
            .append(data
            .map(function (d, i) {
            return $(document.createElementNS('http://www.w3.org/2000/svg', 'polyline'))
                .attr({
                points: [
                    [-2, midPoints[i] * multiplier],
                    [0, midPoints[i] * multiplier],
                    [28, labelBase + labelStep * i],
                    [60, labelBase + labelStep * i]
                ].join(' '),
                style: "\n                                fill: none;\n                                stroke: " + VisualizationView.colors[i]
            });
        }));
        this.$('.category-labels')
            .empty()
            .append(data
            .map(function (d, i) {
            return $('<div>', {
                class: 'category-label'
            })
                .append($('<i>', {
                class: 'icon',
                css: {
                    backgroundImage: "url(" + VisualizationView.getIcon(d) + ")",
                    backgroundColor: VisualizationView.colors[i]
                }
            }), $('<div>', {
                text: d.name,
                class: 'cat-name'
            }), $('<div>', {
                text: VisualizationFilters.currencyFilter(d.amount),
                class: 'cat-value'
            }));
        }));
    };
    VisualizationView.prototype.blockClicked = function (e) {
        console.log('clicked');
        this.$('.block').css('left', -this.$('.block').width());
        console.log(e);
        this.showCurrentLevel(this._model.requestLevel(e));
    };
    VisualizationView.colors = [
        '#ec1e79',
        '#3ea9f5',
        '#33ddc0',
        '#8bc53e',
        '#387915',
        '#999999',
        '#f44040',
        '#2c6b8e',
        '#92278f',
        '#ff7300'
    ];
    VisualizationView.getIcon = function (s) { return ("img/icons/" + (VisualizationView.iconBindings[s.id] || '') + ".svg"); };
    VisualizationView.iconBindings = {
        1: 'altalanos',
        2: 'vedelem',
        3: 'kozrend',
        4: 'gazdasagi',
        5: 'termeszetvedelem',
        6: 'lakasepites',
        7: 'egeszseg',
        8: 'szabadido',
        9: 'oktatas',
        10: 'szocialis'
    };
    return VisualizationView;
})(View);
//# sourceMappingURL=VisualizationView.js.map
/// <reference path="View.ts" />


class VisualizationView extends View {
    constructor(
        private _model: VisualizationModel
    ) {
        super();
        _model.onDataLoaded = this.showCurrentLevel.bind(this);
    }

    html = `
<div class="frame">
    
</div>
`

    public static colors = [
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

    private static getIcon = s => `img/icons/${VisualizationView.iconBindings[s.id] || ''}.svg`;
    public static iconBindings = {
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

    public currentLevel: number = 0;

    showCurrentLevel(data: initialDTO[] = null) {

        // if (data === null) {
            data = this._model.data[0];
        // }
        
        // if (!data || !data.length) return;

        let sum: number = data.map(d => d.amount).reduce((a, b) => a + b, 0);

        const divHeight = 334;
        const [labelBase, labelStep] = [14, 34]

        let multiplier = divHeight / sum;


        let midPoints = [];

        var n = data.length;
        var t = data.map(d => d.amount)
        var s = 0;
        for (var i = 0; i < n; ++i) {
            s = s + t[i];
            midPoints.push(s - t[i] + t[i] / 2);
        }

        this.$('.stack')
            .empty()
            .append(data
                .map((d, i) => $('<div>', {
                    class: 'block',
                    css: {
                        height: d.amount * multiplier,
                        backgroundColor: VisualizationView.colors[i],
                        top: data
                            .filter((d, j) => j < i)
                            .map(d => d.amount * multiplier)
                            .reduce((a, b) => a + b, 0),
                        left: 0
                    }
                }).on('click', this.blockClicked.bind(this, d.id)))
            );

        this.$('.lines')
            .empty()
            .append(data
                .map((d, i) =>
                    $(document.createElementNS('http://www.w3.org/2000/svg', 'polyline'))
                        .attr({
                            points: [
                                [-2, midPoints[i] * multiplier],
                                [0, midPoints[i] * multiplier],
                                [28, labelBase + labelStep * i],
                                [60, labelBase + labelStep * i]
                            ].join(' '),
                            style: `
                                fill: none;
                                stroke: ${VisualizationView.colors[i]}`
                        })
                )
            );

        this.$('.category-labels')
            .empty()
            .append(data
                .map((d, i) =>
                    $('<div>', {
                        class: 'category-label'
                    })
                        .append(
                        $('<i>', {
                            class: 'icon',
                            css: {
                                backgroundImage: `url(${VisualizationView.getIcon(d)})`,
                                backgroundColor: VisualizationView.colors[i]
                            }
                        }),
                        $('<div>', {
                            text: d.name,
                            class: 'cat-name'
                        }),
                        $('<div>', {
                            text: VisualizationFilters.currencyFilter(d.amount),
                            class: 'cat-value'
                        })
                        )
                )
            )
    }

    blockClicked(e) {
        console.log('clicked');
        this.$('.block').css('left', -this.$('.block').width());

        console.log(e)
        
        this.showCurrentLevel(this._model.requestLevel(e))
    }
}
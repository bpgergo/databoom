class VisualizationModel {
    public autocompleteValues: string[] = [
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

    public budget;
    public funcitons;

    // 2, 4, 6 kari
    // rabbit nevu wifi

    public onDataLoaded: (e: Object) => any;

    constructor() {
        $.getJSON('data/budget.json')
            .then(d => this.budget = d)
            .then(() => $.getJSON('data/functions.json'))
            .then(d => this.funcitons = d).then(() => {
                console.log(this.budget.length)
                this.data = this.budget.filter(d => 0 < d.id && d.id <= 11);

                this.data = [this.funcitons
                    .filter(d => 0 < d.id && d.id <= 11)
                    .map(d => {
                        return {
                            id: d.id,
                            name: d.value,
                            amount: this.budget
                                .filter(e => e.func_id.startsWith('0' + d.id))
                                .reduce((a, b) => a + parseFloat(b.value), 0)
                        }
                    })];
            })
            .then(() => this.onDataLoaded && this.onDataLoaded({}));
    }

    requestLevel(id: string): initialDTO[] {
        if (id[0] !== '0') id = `0${id}`;

        while (id[id.length - 1] === '0')
            id = id.slice(0, -1);

        let level = Math.floor(id.length / 2);


        return this.funcitons
            .filter(d => d.id.startsWith(id) && d.id.slice(d.id.length).split('').all(e => e == 0))
            .map(d => {
                return {
                    id: d.id,
                    name: d.value,
                    amount: this.budget
                        .filter(e => e.func_id.startsWith(id))
                        .reduce((a, b) => a + parseFloat(b.value), 0)
                }
            });
    }

    data = [
        [
            //     { id: 1, name: 'Általános közszolgáltatások', amount: 50 },
            //     { id: 2, name: 'Védelem', amount: 30 },
            //     { id: 3, name: 'Közrend és közbiztonság', amount: 20 },
            //     { id: 4, name: 'Gazdasági ügyek', amount: 20 },
            //     { id: 5, name: 'Környezetvédelem', amount: 10 },
            //     { id: 6, name: 'Lakásépítés és kommunális'/* létesítmények'*/, amount: 5 },
            //     { id: 7, name: 'Egészségügy', amount: 5 },
            //     { id: 8, name: 'Szabadidő, sport, kultúra és vallás', amount: 5 },
            //     { id: 9, name: 'Oktatás', amount: 5 },
            //     { id: 10, name: 'Szociális védelem', amount: 1 }
            // ],
            // [
            //     { id: 1, name: 'Általános közszolgáltatások', amount: 50 },
            //     { id: 2, name: 'Védelem', amount: 30 },
        ]
    ];
}
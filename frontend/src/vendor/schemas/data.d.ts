interface budgetDTO {
    func_id: string;
    econ_id: string;
    org_id: string;
    tags?: string[];
    id: string;
    date_start: Date;
    date_end: Date;
    comments?: string;
}

interface functionsDTO {
    parent_id: string;
    id: string;
    value: string;
}

interface economiesDTO {
    parent_id: string;
    id: string;
    value: string;
}

interface initialDTO {
    id: string;
    name: string;
    amount: number;
}
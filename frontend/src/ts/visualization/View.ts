/// <reference path="../../../typings/jquery/jquery.d.ts" />


abstract class View {
    public html: string;
    private _selector: JQuery;
    protected get _domElement() { return this._selector }

    public render(selector: string) {
        (this._selector = $(selector)).html(this.html);
    }
    
    protected $(selector: string) {
        return $(selector, this._selector);
    }
}
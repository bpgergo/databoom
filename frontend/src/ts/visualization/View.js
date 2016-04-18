/// <reference path="../../../typings/jquery/jquery.d.ts" />
var View = (function () {
    function View() {
    }
    Object.defineProperty(View.prototype, "_domElement", {
        get: function () { return this._selector; },
        enumerable: true,
        configurable: true
    });
    View.prototype.render = function (selector) {
        (this._selector = $(selector)).html(this.html);
    };
    View.prototype.$ = function (selector) {
        return $(selector, this._selector);
    };
    return View;
})();
//# sourceMappingURL=View.js.map
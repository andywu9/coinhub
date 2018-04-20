Number.prototype.formatMoney = function (c, d, t) {
    var n, s, i, j;

    c = Math.abs(c);
    c = isNaN(c) ? 2 : c;
    d = d === undefined ? "." : d;
    t = t === undefined ? "," : t;
    n = Math.abs(Number(this) || 0).toFixed(c);
    s = n < 0 ? "-" : "";
    i = String(parseInt(n, 10));
    j = i.length;

    j = j > 3 ? j % 3 : 0;
    return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};
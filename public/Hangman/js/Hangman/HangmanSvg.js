class HangmanSvg extends Hangman {
    constructor(svg) {

        super({
            canvas: {
                width: svg.getAttribute("width") || 300,
                height: svg.getAttribute("height") || 200
            },
            ctx: svg
        });
        customJsInterface(this, Hangman.__virtual_methods() || []);
    }

    __update_GUI_Line(opts) {
        let { iniX, iniY, nextX, nextY } = opts;
        let { currX, currY, ctx } = this;

        var newElement = document.createElementNS("http://www.w3.org/2000/svg", 'line'); //Create a path in SVG's namespace
        newElement.setAttribute("x1", iniX || currX);
        newElement.setAttribute("y1", iniY || currY);
        newElement.setAttribute("x2", nextX);
        newElement.setAttribute("y2", nextY);
        newElement.setAttribute("class", "figure-part");
        ctx.appendChild(newElement);
    }

    __update_GUI_Circle(opts) {
        let { iniX, iniY, radius } = opts;
        let { currX, currY, ctx } = this;

        var newElement = document.createElementNS("http://www.w3.org/2000/svg", 'circle'); //Create a path in SVG's namespace
        newElement.setAttribute("cx", iniX || currX);
        newElement.setAttribute("cy", (iniY + radius) || currY);
        newElement.setAttribute("r", radius);
        newElement.setAttribute("class", "figure-part");
        ctx.appendChild(newElement);
    }
}
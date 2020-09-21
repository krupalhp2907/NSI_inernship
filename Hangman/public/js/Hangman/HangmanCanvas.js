class HangmanCanvas extends Hangman {
    constructor(canvas) {
        super({
            canvas,
            ctx: canvas.getContext("2d")
        });
        customJsInterface.call(this, this, Hangman.__virtual_methods() || []);
    }

    __update_GUI_Line(opts) {
        let { iniX, iniY, nextX, nextY } = opts;
        let { currX, currY, ctx } = this;
        ctx.beginPath();
        ctx.moveTo(iniX || currX, iniY || currY);
        ctx.lineTo(nextX, nextY);
        ctx.stroke();
    }

    __update_GUI_Circle(opts) {
        let { iniX, iniY, radius } = opts;
        let { currX, currY, ctx } = this;
        ctx.beginPath();
        ctx.arc(iniX || currX, (iniY + radius) || currY, radius, 0, 2 * Math.PI);
        ctx.stroke();
    }
}
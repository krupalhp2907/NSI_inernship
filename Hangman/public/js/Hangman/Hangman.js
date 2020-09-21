class Hangman {
    constructor(opts) {
        this.startX = opts.startX;
        this.startY = opts.startY;
        // Canvas
        if (!opts.canvas) throw Error("Canvas Element is required");
        this.canvas = opts.canvas;
        // Canvas Element
        if (!opts.canvas) throw Error("Context Element is required");
        this.ctx = opts.ctx;

        // Canvas Dimensions
        this.canvasX = this.canvas.width || 300;
        this.canvasY = this.canvas.height || 200;
        // Count for GAME OVER
        this.count = 0;
        // Starting position of cursor
        this.currX = opts.startX || this.canvasX * 0.02;
        this.currY = opts.startY || this.canvasY * 0.95; // this.canvasY - 10

        // Length of Base Line or Bottom Support
        this.baseLineWidth = opts.baseLineWidth || (this.canvasX - this.currX) * 0.4; // 100
        // Left Most Pillar Height
        this.leftPillarHeight = opts.leftPillarHeight || this.currY * 0.96; // 160
        // The gap between the end and beginning
        this.horizontalPoleGap = opts.horizontalPoleGap || this.leftPillarHeight * 0.07; // 10
        // Upper Horizontal pole Lenght
        this.horizontalPoleLength = opts.horizontalPoleLength || (this.canvasX - this.currX) * 0.4; // 125
        // Radius of Head
        this.headRadius = opts.headRadius || this.leftPillarHeight * 0.13; // 20
        // Height of Torso
        this.torsoHeight = opts.torsoHeight || this.headRadius * 2.34; // 50
        // The percentage of torso where hands should start defaulf 25% height of torso
        this.handStartAtRelativeToTorso = opts.handStartAtRelativeToTorso || this.torsoHeight * 0.25;
        // Size of hand default 75% of torso
        this.handSize = opts.handSize || this.torsoHeight * 0.75;
        // Angle W.R.T torso
        this.handAngle = opts.handAngle || 60;
        // Size of legs
        this.legSize = opts.legSize || this.torsoHeight * 0.75;
        // Angle WRT to torso line
        this.legAngle = opts.legAngle || 45;
        // This is the particular sequence to follow to make torso donot change this sequence
        this.sequence = [
            this.__head,
            this.__torso,
            this.__leftHand,
            this.__rightHand,
            this.__leftLeg,
            this.__rightLeg
        ]
        // Incorrect answers to complete game
        this.MAX = this.sequence.length;

        // Initialise Hangmans 
        this.__baseLine(),
            // Comment this section so that only first section fails
            this.__leftPillar(),
            this.__horizontalPole(),
            this.__rightPillar();
    }

    static __virtual_methods() {
        return ['__update_GUI_Circle', '__update_GUI_Line'];
    }

    __baseLine() {
        let { currX, currY, baseLineWidth } = this;

        let iniX = currX,
            iniY = currY;

        let nextX = iniX + baseLineWidth,
            nextY = iniY;

        this.__update_GUI_Line({
            iniX, iniY,
            nextX, nextY
        });

        this.currX = nextX, this.currY = nextY;
    }

    __leftPillar() {
        let { currX, currY, baseLineWidth, leftPillarHeight } = this;

        let iniX = (currX + (currX - baseLineWidth)) / 2,
            iniY = currY;

        let nextX = iniX,
            nextY = iniY - leftPillarHeight;

        this.__update_GUI_Line({
            iniX, iniY,
            nextX, nextY
        });

        this.currX = nextX, this.currY = nextY;
    }

    __horizontalPole() {
        let { currX, currY, ctx, horizontalPoleLength, horizontalPoleGap } = this;

        let iniX = currX - horizontalPoleGap,
            iniY = currY + horizontalPoleGap;

        let nextX = iniX + horizontalPoleLength,
            nextY = iniY;

        this.__update_GUI_Line({
            iniX, iniY,
            nextX, nextY
        });

        this.currX = nextX, this.currY = nextY;

    }

    __rightPillar() {
        let { currX, currY, horizontalPoleGap } = this;

        let iniX = currX - horizontalPoleGap * 2,
            iniY = currY;

        let nextX = iniX,
            nextY = currY + 10;

        this.__update_GUI_Line({
            iniX, iniY,
            nextX, nextY
        });

        this.currX = nextX, this.currY = nextY;

    }

    __head() {
        let { currX, currY, headRadius } = this;

        let iniX = currX,
            iniY = currY;

        let nextX = iniX,
            nextY = currY + 2 * headRadius;

        this.__update_GUI_Circle({
            iniX, iniY, radius: headRadius
        })

        this.currX = nextX, this.currY = nextY;
    }

    __torso() {
        let { currX, currY, ctx, torsoHeight } = this;

        let iniX = currX,
            iniY = currY;

        let nextX = iniX,
            nextY = currY + torsoHeight;

        this.__update_GUI_Line({
            iniX, iniY,
            nextX, nextY
        });

        this.currX = nextX, this.currY = nextY;
    }

    __leftHand() {
        let { currX, currY, ctx, handStartAtRelativeToTorso, handSize, handAngle, torsoHeight } = this;

        let iniX = currX,
            iniY = currY - torsoHeight + handStartAtRelativeToTorso;

        let nextX = iniX - handSize * Math.sin(Math.PI * handAngle / 180.0),
            nextY = iniY + handSize * Math.cos(Math.PI * handAngle / 180.0);


        this.__update_GUI_Line({
            iniX, iniY,
            nextX, nextY
        });

    }

    __rightHand() {
        let { currX, currY, ctx, handStartAtRelativeToTorso, handSize, handAngle, torsoHeight } = this;

        let iniX = currX,
            iniY = currY - torsoHeight + handStartAtRelativeToTorso;

        let nextX = iniX + handSize * Math.sin(Math.PI * handAngle / 180.0),
            nextY = iniY + handSize * Math.cos(Math.PI * handAngle / 180.0);


        this.__update_GUI_Line({
            iniX, iniY,
            nextX, nextY
        });

    }

    __leftLeg() {
        let { currX, currY, ctx, legSize, legAngle } = this;

        let iniX = currX,
            iniY = currY;

        let nextX = iniX - legSize * Math.sin(Math.PI * legAngle / 180.0),
            nextY = iniY + legSize * Math.cos(Math.PI * legAngle / 180.0);


        this.__update_GUI_Line({
            iniX, iniY,
            nextX, nextY
        });
    }

    __rightLeg() {
        let { currX, currY, ctx, legSize, legAngle } = this;

        let iniX = currX,
            iniY = currY;

        let nextX = iniX + legSize * Math.sin(Math.PI * legAngle / 180.0),
            nextY = iniY + legSize * Math.cos(Math.PI * legAngle / 180.0);


        this.__update_GUI_Line({
            iniX, iniY,
            nextX, nextY
        });
    }

    draw() {
        let { MAX, sequence } = this;

        if (this.count >= MAX) {
            return -1;
        }

        sequence[this.count].call(this);
        this.count++;
        return 1;
    }

    reset() {
        this.currX = this.startX || this.canvasX * 0.02;
        this.currY = this.startY || this.canvasY * 0.95; // this.canvasY - 10
        this.count = 0;
        this.__baseLine(),
            // comment to fail all test cases
            this.__leftPillar(),
            this.__horizontalPole(),
            this.__rightPillar();
    }
}
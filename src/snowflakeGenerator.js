import { renderSnowflake } from './snowflake.js';

const MIN_CANVAS_SIZE = 360;
const RESIZE_DEBOUNCE = 80;

export class SnowflakeGenerator {
    constructor(canvas) {
        if (!canvas) {
            throw new Error('SnowflakeGenerator 需要有效的 canvas 元素');
        }

        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.state = null;

        this.running = true;
        this.needsRender = true;
        this.lastTimestamp = performance.now();
        this.elapsed = 0;
        this.angle = 0;
        this.pulsePhase = 0;
        this.resizeTimer = null;

        this.loop = this.loop.bind(this);
        this.handleResize = this.handleResize.bind(this);
        this.observeResize = this.observeResize.bind(this);

        this.observeResize();
        this.handleResize();
        requestAnimationFrame(this.loop);
    }

    observeResize() {
        const parent = this.canvas.parentElement;
        if (window.ResizeObserver && parent) {
            this.resizeObserver = new ResizeObserver(() => this.scheduleResize());
            this.resizeObserver.observe(parent);
        } else {
            window.addEventListener('resize', this.handleResize);
        }
    }

    scheduleResize() {
        if (this.resizeTimer) {
            clearTimeout(this.resizeTimer);
        }
        this.resizeTimer = setTimeout(() => {
            this.handleResize();
            this.resizeTimer = null;
        }, RESIZE_DEBOUNCE);
    }

    handleResize() {
        const parent = this.canvas.parentElement ?? this.canvas;
        const rect = parent.getBoundingClientRect();
        const availableWidth = rect.width || this.canvas.clientWidth || MIN_CANVAS_SIZE;
        const availableHeight = rect.height || window.innerHeight || availableWidth;
        const maxHeight = Math.max(MIN_CANVAS_SIZE, Math.min(availableHeight, window.innerHeight - 160 || availableHeight));
        const size = Math.max(MIN_CANVAS_SIZE, Math.min(availableWidth, maxHeight));
        const ratio = window.devicePixelRatio || 1;

        const pixelSize = Math.round(size * ratio);
        if (this.canvas.width !== pixelSize || this.canvas.height !== pixelSize) {
            this.canvas.width = pixelSize;
            this.canvas.height = pixelSize;
            this.canvas.style.width = `${size}px`;
            this.canvas.style.height = `${size}px`;
            this.ctx.setTransform(1, 0, 0, 1, 0, 0);
            this.needsRender = true;
        }
    }

    setState(state, options = {}) {
        this.state = state;

        if (!options.preserveAngle && options.angle === undefined) {
            this.angle = 0;
        }
        if (!options.preservePulsePhase && options.pulsePhase === undefined) {
            this.pulsePhase = 0;
        }

        if (options.angle !== undefined) {
            this.angle = options.angle;
        }

        if (options.pulsePhase !== undefined) {
            this.pulsePhase = options.pulsePhase;
        }

        if (!options.preserveTime) {
            this.elapsed = 0;
        }

        this.requestRender();
    }

    requestRender() {
        this.needsRender = true;
    }

    toggleAnimation() {
        this.running = !this.running;
        if (this.running) {
            this.requestRender();
        }
        return this.running;
    }

    setRunning(value) {
        this.running = Boolean(value);
        if (this.running) {
            this.requestRender();
        }
    }

    isRunning() {
        return this.running;
    }

    getAngle() {
        return this.angle;
    }

    getPulsePhase() {
        return this.pulsePhase;
    }

    getPulseValue() {
        return Math.sin(this.pulsePhase);
    }

    getRenderSnapshot() {
        return {
            angle: this.angle,
            pulse: this.getPulseValue(),
            time: this.elapsed,
        };
    }

    loop(timestamp) {
        requestAnimationFrame(this.loop);

        const delta = timestamp - this.lastTimestamp;
        this.lastTimestamp = timestamp;

        if (this.running && this.state?.params?.animate) {
            const params = this.state.params;
            this.angle += delta * params.spinSpeed;
            this.pulsePhase += delta * params.pulseSpeed;
            this.elapsed += delta;
            this.needsRender = true;
        }

        if (!this.state || !this.needsRender) {
            return;
        }

        renderSnowflake(this.ctx, this.state, {
            angle: this.angle,
            pulse: this.getPulseValue(),
            time: this.elapsed,
        });

        this.needsRender = false;
    }

    destroy() {
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        } else {
            window.removeEventListener('resize', this.handleResize);
        }
        if (this.resizeTimer) {
            clearTimeout(this.resizeTimer);
            this.resizeTimer = null;
        }
    }
}

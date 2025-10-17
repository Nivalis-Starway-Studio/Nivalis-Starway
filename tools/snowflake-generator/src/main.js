import {
    createParameters,
    createSnowflakeState,
    renderSnowflake,
    randomSeed,
    decodeParameters,
    createShareableHash,
} from './snowflake.js';
import { GalleryManager } from './gallery.js';
import { ShareManager } from './share.js';
import { registerKeyboardShortcuts } from './keyboard.js';

const NOTIFICATION_TIMEOUT = 3200;

function parseNumber(value, fallback, parser = Number) {
    const parsed = parser(value);
    return Number.isFinite(parsed) ? parsed : fallback;
}

function clampToInput(input, value) {
    if (!input) return value;
    const min = input.min !== '' ? Number(input.min) : undefined;
    const max = input.max !== '' ? Number(input.max) : undefined;
    let result = Number(value);
    if (Number.isFinite(min)) {
        result = Math.max(result, min);
    }
    if (Number.isFinite(max)) {
        result = Math.min(result, max);
    }
    if (input.step && input.step !== 'any') {
        const step = Number(input.step);
        if (Number.isFinite(step) && step > 0) {
            result = Math.round(result / step) * step;
            const decimalPlaces = (input.step.split('.')[1] || '').length;
            result = Number(result.toFixed(decimalPlaces));
        }
    }
    return result;
}

class SnowflakeApp {
    constructor() {
        this.canvas = document.getElementById('snowflakeCanvas');
        if (!this.canvas) {
            throw new Error('Snowflake canvas element not found');
        }
        this.ctx = this.canvas.getContext('2d');

        this.controls = {
            branches: document.getElementById('branches'),
            complexity: document.getElementById('complexity'),
            size: document.getElementById('size'),
            lineWidth: document.getElementById('lineWidth'),
            color: document.getElementById('color'),
            generateBtn: document.getElementById('generateBtn'),
            toggleAnimationBtn: document.getElementById('toggleAnimationBtn'),
            exportBtn: document.getElementById('exportBtn'),
            addToGalleryBtn: document.getElementById('addToGalleryBtn'),
            toggleGalleryBtn: document.getElementById('toggleGalleryBtn'),
            animationStatus: document.getElementById('animationStatus'),
        };

        this.notificationEl = document.getElementById('notification');

        this.snowflakeState = null;
        this.currentSeed = randomSeed();
        this.animation = {
            running: true,
            angle: 0,
            pulse: 0,
            lastTime: performance.now(),
        };
        this.needsRender = true;
        this.notificationTimer = null;

        this.gallery = new GalleryManager();
        this.share = new ShareManager();

        this.bindUI();
        this.setupGalleryCallbacks();
        this.setupShareCallbacks();
        this.setupKeyboardShortcuts();
        this.watchHashChanges();

        const restored = this.initializeFromHash();
        if (!restored) {
            this.generateNewSnowflake({ showNotification: false });
        }

        this.updateAnimationStatus();
        requestAnimationFrame((timestamp) => this.loop(timestamp));
    }

    bindUI() {
        const sliderBindings = [
            { input: this.controls.branches, labelId: 'branchesValue' },
            { input: this.controls.complexity, labelId: 'complexityValue' },
            { input: this.controls.size, labelId: 'sizeValue' },
            { input: this.controls.lineWidth, labelId: 'lineWidthValue' },
        ];

        sliderBindings.forEach(({ input, labelId }) => {
            if (!input) return;
            const label = document.getElementById(labelId);
            const updateLabel = () => {
                if (label) {
                    label.textContent = input.value;
                }
            };
            updateLabel();
            input.addEventListener('input', () => {
                updateLabel();
                this.updateFromControls();
            });
        });

        if (this.controls.color) {
            this.controls.color.addEventListener('input', () => this.updateFromControls());
        }

        this.controls.generateBtn?.addEventListener('click', () => this.generateNewSnowflake());
        this.controls.toggleAnimationBtn?.addEventListener('click', () => this.toggleAnimation());
        this.controls.exportBtn?.addEventListener('click', () => this.exportSnowflake());
        this.controls.addToGalleryBtn?.addEventListener('click', () => this.captureToGallery());
        this.controls.toggleGalleryBtn?.addEventListener('click', () => this.gallery.toggle());
    }

    setupGalleryCallbacks() {
        this.gallery.onExport((params, id) => {
            this.exportSnowflake(id, params);
        });

        this.gallery.onApply((params) => {
            this.applyParameters(params, {
                showNotification: true,
                notificationMessage: 'Snowflake applied from gallery',
            });
            this.gallery.close();
        });
    }

    setupShareCallbacks() {
        this.share.onGetCurrentParams(() => {
            if (!this.snowflakeState) return null;
            return JSON.parse(JSON.stringify(this.snowflakeState.params));
        });
    }

    setupKeyboardShortcuts() {
        this.cleanupShortcuts = registerKeyboardShortcuts([
            { code: 'KeyN', ctrl: true, action: () => this.generateNewSnowflake() },
            { code: 'KeyG', action: () => this.generateNewSnowflake() },
            { code: 'KeyA', ctrl: true, action: () => this.toggleAnimation() },
            { code: 'KeyA', action: () => this.toggleAnimation() },
            { code: 'KeyE', ctrl: true, action: () => this.exportSnowflake() },
            { code: 'KeyE', action: () => this.exportSnowflake() },
            { code: 'KeyS', action: () => this.share.toggle() },
            { code: 'KeyC', action: () => this.captureToGallery() },
            { code: 'KeyV', action: () => this.gallery.toggle() },
        ]);
    }

    watchHashChanges() {
        window.addEventListener('hashchange', () => {
            const applied = this.initializeFromHash({ notify: true });
            if (!applied) {
                this.showNotification('Unable to load snowflake from link', 'error');
            }
        });
    }

    getControlSettings() {
        return {
            branches: parseNumber(this.controls.branches?.value, 6, Number.parseInt),
            complexity: parseNumber(this.controls.complexity?.value, 5, Number.parseInt),
            size: parseNumber(this.controls.size?.value, 300, Number.parseInt),
            lineWidth: parseNumber(this.controls.lineWidth?.value, 2, Number.parseFloat),
            color: this.controls.color?.value ?? '#4a90e2',
        };
    }

    updateFromControls() {
        const settings = this.getControlSettings();
        const params = createParameters(settings, { seed: this.currentSeed });
        this.applyParameters(params, {
            showNotification: false,
            skipControlSync: true,
            preserveAngle: true,
            preservePulse: true,
        });
    }

    generateNewSnowflake({ showNotification = true } = {}) {
        this.currentSeed = randomSeed();
        const params = createParameters(this.getControlSettings(), { seed: this.currentSeed });
        this.applyParameters(params, {
            showNotification,
            notificationMessage: 'Generated new snowflake',
        });
    }

    initializeFromHash({ notify = false } = {}) {
        const params = decodeParameters(window.location.hash);
        if (!params) {
            return false;
        }
        this.applyParameters(params, {
            showNotification: notify,
            notificationMessage: 'Loaded snowflake from link',
        });
        return true;
    }

    applyParameters(params, options = {}) {
        if (!params) return;
        this.currentSeed = parseNumber(params.seed, this.currentSeed, Number.parseInt);

        if (!options.skipControlSync) {
            this.syncControls(params);
        }

        this.snowflakeState = createSnowflakeState({ ...params, seed: this.currentSeed });

        if (!options.preserveAngle) {
            this.animation.angle = 0;
        }
        if (!options.preservePulse) {
            this.animation.pulse = 0;
        }
        this.animation.lastTime = performance.now();

        this.requestRender();
        this.updateAnimationStatus();
        this.updateShareHash();

        if (options.showNotification) {
            this.showNotification(options.notificationMessage ?? 'Updated snowflake', 'info');
        }
    }

    syncControls(params) {
        const { branches, complexity, radius, lineWidth, color } = params;
        this.setControlValue(this.controls.branches, branches, 'branchesValue');
        this.setControlValue(this.controls.complexity, complexity, 'complexityValue');
        this.setControlValue(this.controls.size, radius, 'sizeValue');
        this.setControlValue(this.controls.lineWidth, lineWidth, 'lineWidthValue');
        if (this.controls.color && typeof color === 'string') {
            this.controls.color.value = color;
        }
    }

    setControlValue(input, value, labelId) {
        if (!input || value === undefined) return;
        const clamped = clampToInput(input, value);
        input.value = clamped;
        const label = document.getElementById(labelId);
        if (label) {
            label.textContent = clamped;
        }
    }

    requestRender() {
        this.needsRender = true;
    }

    loop(timestamp) {
        requestAnimationFrame((time) => this.loop(time));
        if (!this.snowflakeState) return;

        const delta = timestamp - this.animation.lastTime;
        this.animation.lastTime = timestamp;

        if (this.animation.running && this.snowflakeState.params.animate) {
            this.animation.angle += delta * this.snowflakeState.params.spinSpeed;
            this.animation.pulse += delta * this.snowflakeState.params.pulseSpeed;
            this.needsRender = true;
        }

        if (!this.needsRender) return;

        const pulseValue = Math.sin(this.animation.pulse);
        renderSnowflake(this.ctx, this.snowflakeState, {
            angle: this.animation.angle,
            pulse: pulseValue,
        });
        this.needsRender = false;
    }

    toggleAnimation() {
        this.animation.running = !this.animation.running;
        this.updateAnimationStatus();
        this.requestRender();
        this.showNotification(
            this.animation.running ? 'Animation resumed' : 'Animation paused',
            'info',
        );
    }

    updateAnimationStatus() {
        const label = this.animation.running ? 'Animation: ON' : 'Animation: OFF';
        const statusEl = this.controls.animationStatus;
        if (statusEl) {
            statusEl.textContent = label;
            statusEl.classList.toggle('active', this.animation.running);
        }

        if (this.controls.toggleAnimationBtn) {
            this.controls.toggleAnimationBtn.textContent = this.animation.running
                ? 'Pause Animation'
                : 'Resume Animation';
        }
    }

    exportSnowflake(filename = null, paramsOverride = null) {
        const state = paramsOverride ? createSnowflakeState(paramsOverride) : this.snowflakeState;
        if (!state) {
            this.showNotification('Nothing to export yet', 'error');
            return;
        }

        const exportCanvas = document.createElement('canvas');
        exportCanvas.width = 2400;
        exportCanvas.height = 2400;
        const exportCtx = exportCanvas.getContext('2d');
        const angle = paramsOverride ? 0 : this.animation.angle;
        const pulse = paramsOverride ? 0 : Math.sin(this.animation.pulse);

        renderSnowflake(exportCtx, state, { angle, pulse });

        exportCanvas.toBlob((blob) => {
            if (!blob) {
                this.showNotification('Export failed', 'error');
                return;
            }
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            const baseName = filename ?? `snowflake-${state.params.seed}`;
            link.download = `${baseName}.png`;
            link.href = url;
            link.click();
            URL.revokeObjectURL(url);
            this.showNotification('Snowflake exported as PNG', 'success');
        }, 'image/png');
    }

    captureToGallery() {
        if (!this.snowflakeState) {
            this.showNotification('Generate a snowflake first', 'error');
            return;
        }
        const paramsCopy = JSON.parse(JSON.stringify(this.snowflakeState.params));
        this.gallery.add(paramsCopy);
        this.showNotification('Snowflake saved to gallery', 'success');
    }

    updateShareHash() {
        if (!this.snowflakeState) return;
        const hash = createShareableHash(this.snowflakeState.params);
        if (window.history?.replaceState) {
            window.history.replaceState(null, '', `#${hash}`);
        } else {
            window.location.hash = hash;
        }
    }

    showNotification(message, type = 'info') {
        if (!this.notificationEl) return;
        if (this.notificationTimer) {
            clearTimeout(this.notificationTimer);
        }
        this.notificationEl.textContent = message;
        this.notificationEl.className = `notification ${type}`;
        this.notificationEl.classList.add('show');
        this.notificationTimer = setTimeout(() => {
            this.notificationEl.classList.remove('show');
        }, NOTIFICATION_TIMEOUT);
    }
}

if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        window.addEventListener('DOMContentLoaded', () => new SnowflakeApp());
    } else {
        new SnowflakeApp();
    }
}

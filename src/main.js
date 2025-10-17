import {
    createParameters,
    createSnowflakeState,
    renderSnowflake,
    randomSeed,
    decodeParameters,
    createShareableHash,
} from './snowflake.js';
import { SnowflakeGenerator } from './snowflakeGenerator.js';
import { GalleryManager } from './gallery.js';
import { ShareManager } from './share.js';
import { registerKeyboardShortcuts } from './keyboard.js';

const NOTIFICATION_TIMEOUT = 3200;
const SYMMETRY_OPTIONS = [6, 8, 12];

function parseNumber(value, fallback, parser = Number) {
    const parsed = parser(value);
    return Number.isFinite(parsed) ? parsed : fallback;
}

function snapToSymmetry(value) {
    const numeric = Number.isFinite(value) ? value : SYMMETRY_OPTIONS[0];
    return SYMMETRY_OPTIONS.reduce((closest, option) => {
        const diffCurrent = Math.abs(option - numeric);
        const diffClosest = Math.abs(closest - numeric);
        return diffCurrent < diffClosest ? option : closest;
    }, SYMMETRY_OPTIONS[0]);
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
        this.notificationTimer = null;

        this.generator = new SnowflakeGenerator(this.canvas);

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
                let displayValue = input.value;
                if (input === this.controls.branches) {
                    const snapped = snapToSymmetry(parseNumber(displayValue, SYMMETRY_OPTIONS[0], Number.parseInt));
                    if (Number(displayValue) !== snapped) {
                        input.value = snapped;
                        displayValue = snapped;
                    } else {
                        displayValue = snapped;
                    }
                }
                if (label) {
                    label.textContent = displayValue;
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
        const rawBranches = parseNumber(this.controls.branches?.value, SYMMETRY_OPTIONS[0], Number.parseInt);
        return {
            branches: snapToSymmetry(rawBranches),
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

        this.generator.setState(this.snowflakeState, {
            preserveAngle: options.preserveAngle,
            preservePulsePhase: options.preservePulse,
            preserveTime: options.preserveTime ?? false,
        });

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

    toggleAnimation() {
        const running = this.generator.toggleAnimation();
        this.updateAnimationStatus();
        this.showNotification(
            running ? '动画已恢复' : '动画已暂停',
            'info',
        );
    }

    updateAnimationStatus() {
        const running = this.generator.isRunning();
        const label = running ? 'Animation: ON' : 'Animation: OFF';
        const statusEl = this.controls.animationStatus;
        if (statusEl) {
            statusEl.textContent = label;
            statusEl.classList.toggle('active', running);
        }

        if (this.controls.toggleAnimationBtn) {
            this.controls.toggleAnimationBtn.textContent = running
                ? 'Pause Animation'
                : 'Resume Animation';
        }
    }

    exportSnowflake(filename = null, paramsOverride = null) {
        const state = paramsOverride ? createSnowflakeState(paramsOverride) : this.snowflakeState;
        if (!state) {
            this.showNotification('还没有可导出的雪花', 'error');
            return;
        }

        const exportCanvas = document.createElement('canvas');
        exportCanvas.width = 2400;
        exportCanvas.height = 2400;
        const exportCtx = exportCanvas.getContext('2d');

        const renderSnapshot = paramsOverride ? { angle: 0, pulse: 0, time: 0 } : this.generator.getRenderSnapshot();

        renderSnowflake(exportCtx, state, renderSnapshot);

        exportCanvas.toBlob((blob) => {
            if (!blob) {
                this.showNotification('导出失败', 'error');
                return;
            }
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            const baseName = filename ?? `snowflake-${state.params.seed}`;
            link.download = `${baseName}.png`;
            link.href = url;
            link.click();
            URL.revokeObjectURL(url);
            this.showNotification('雪花已导出为 PNG', 'success');
        }, 'image/png');
    }

    captureToGallery() {
        if (!this.snowflakeState) {
            this.showNotification('请先生成一个雪花', 'error');
            return;
        }
        const paramsCopy = JSON.parse(JSON.stringify(this.snowflakeState.params));
        this.gallery.add(paramsCopy);
        this.showNotification('雪花已保存到画廊', 'success');
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

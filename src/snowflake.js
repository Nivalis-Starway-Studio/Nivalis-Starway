const TAU = Math.PI * 2;
const MAX_GALLERY_ITEMS = 24;

function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
}

function hexToRgb(hex) {
    let value = hex.replace('#', '').trim();
    if (value.length === 3) {
        value = value.split('').map((ch) => ch + ch).join('');
    }
    const int = parseInt(value, 16);
    return {
        r: (int >> 16) & 255,
        g: (int >> 8) & 255,
        b: int & 255,
    };
}

function rgbToHex(r, g, b) {
    const toHex = (component) => component.toString(16).padStart(2, '0');
    return `#${toHex(clamp(Math.round(component), 0, 255))}${toHex(clamp(Math.round(g), 0, 255))}${toHex(clamp(Math.round(b), 0, 255))}`;
}

function lighten(hex, factor) {
    const { r, g, b } = hexToRgb(hex);
    return rgbToHex(
        r + (255 - r) * factor,
        g + (255 - g) * factor,
        b + (255 - b) * factor,
    );
}

function darken(hex, factor) {
    const { r, g, b } = hexToRgb(hex);
    return rgbToHex(r * (1 - factor), g * (1 - factor), b * (1 - factor));
}

function rgba(hex, alpha) {
    const { r, g, b } = hexToRgb(hex);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function createRandom(seed) {
    let state = seed >>> 0;
    return () => {
        state = (state * 1664525 + 1013904223) >>> 0;
        return state / 4294967296;
    };
}

export function randomSeed() {
    if (window.crypto?.getRandomValues) {
        const array = new Uint32Array(1);
        window.crypto.getRandomValues(array);
        return array[0];
    }
    return Math.floor(Math.random() * 0xffffffff);
}

export function createParameters(settings = {}, overrides = {}) {
    const seed = overrides.seed ?? randomSeed();
    const random = createRandom(seed);

    const branchesFromSettings = Number.parseInt(settings.branches ?? 0, 10);
    const complexityFromSettings = Number.parseInt(settings.complexity ?? 0, 10);
    const radiusFromSettings = Number.parseInt(settings.size ?? 0, 10);
    const lineWidthFromSettings = Number.parseFloat(settings.lineWidth ?? 0);
    const baseColorSetting = (settings.color ?? '#4a90e2').toString().trim();

    const params = {
        seed,
        branches: clamp(overrides.branches ?? branchesFromSettings || Math.floor(5 + random() * 5), 3, 14),
        complexity: clamp(overrides.complexity ?? complexityFromSettings || Math.floor(3 + random() * 5), 1, 12),
        radius: clamp(overrides.radius ?? radiusFromSettings || Math.floor(260 + random() * 80), 120, 380),
        lineWidth: clamp(overrides.lineWidth ?? lineWidthFromSettings || (1.5 + random() * 1.5), 0.6, 6),
        color: (overrides.color ?? baseColorSetting).toLowerCase(),
        accentColor: overrides.accentColor ?? lighten(baseColorSetting, 0.25 + random() * 0.2),
        coreColor: overrides.coreColor ?? lighten(baseColorSetting, 0.18),
        background: overrides.background ?? darken(baseColorSetting, 0.75),
        branchSpread: overrides.branchSpread ?? (0.28 + random() * 0.4),
        branchJitter: overrides.branchJitter ?? (0.1 + random() * 0.2),
        secondaryBranches: overrides.secondaryBranches ?? Math.max(1, Math.round(2 + random() * 3)),
        tipDetails: overrides.tipDetails ?? Math.max(2, Math.round(3 + random() * 3)),
        sparkleCount: overrides.sparkleCount ?? Math.round(10 + random() * 14),
        animate: overrides.animate ?? true,
        spinSpeed: overrides.spinSpeed ?? (0.00025 + random() * 0.00055),
        pulseSpeed: overrides.pulseSpeed ?? (0.00035 + random() * 0.00045),
        pulseStrength: overrides.pulseStrength ?? (0.06 + random() * 0.09),
        glow: overrides.glow ?? (0.4 + random() * 0.4),
    };

    return params;
}

export function buildStructure(params) {
    const random = createRandom((params.seed ^ 0x9e3779b9) >>> 0);
    const nodes = [];

    for (let layer = 0; layer < params.complexity; layer += 1) {
        const progress = (layer + 1) / (params.complexity + 1);
        const distance = params.radius * progress;
        const branchLength = params.radius * (0.25 + (1 - progress) * 0.65) * (0.85 + random() * 0.3);
        const thickness = params.lineWidth * (1.15 - progress * 0.6);
        const lateral = (random() - 0.5) * params.radius * params.branchJitter;
        const detailCount = Math.max(1, Math.round(params.secondaryBranches + random() * params.secondaryBranches));
        const details = [];

        for (let i = 0; i < detailCount; i += 1) {
            const offsetIndex = i - (detailCount - 1) / 2;
            const angle = offsetIndex * params.branchSpread * (0.9 + random() * 0.25);
            const lengthFactor = 0.45 + random() * 0.45;
            const thicknessFactor = 0.7 + random() * 0.3;
            details.push({ angle, lengthFactor, thicknessFactor });
        }

        const crystalChance = random();
        const crystal = crystalChance > 0.65 ? {
            radius: branchLength * (0.12 + random() * 0.22),
            points: 4 + Math.floor(random() * 4),
            rotation: random() * TAU,
        } : null;

        nodes.push({
            distance,
            branchLength,
            thickness,
            lateral,
            details,
            crystal,
        });
    }

    const tipDecorations = [];
    for (let i = 0; i < params.tipDetails; i += 1) {
        const offsetIndex = i - (params.tipDetails - 1) / 2;
        tipDecorations.push({
            lengthFactor: 0.25 + Math.abs(offsetIndex) * 0.15 + random() * 0.35,
            thicknessFactor: 0.6 + random() * 0.3,
            angle: offsetIndex * params.branchSpread * 0.6,
            offset: params.radius * (0.75 + random() * 0.18),
        });
    }

    const sparkles = [];
    for (let i = 0; i < params.sparkleCount; i += 1) {
        const distance = params.radius * (0.2 + random() * 0.75);
        sparkles.push({
            distance,
            angle: random() * TAU,
            size: 1.4 + random() * 2.4,
            alpha: 0.3 + random() * 0.45,
        });
    }

    const ringCount = Math.max(1, Math.round(params.complexity / 2));
    const rings = [];
    for (let i = 0; i < ringCount; i += 1) {
        const factor = (i + 1) / (ringCount + 1);
        rings.push({
            radius: params.radius * (0.3 + factor * 0.65),
            thickness: params.lineWidth * (0.4 + (1 - factor) * 0.8),
            alpha: 0.2 + factor * 0.3,
        });
    }

    return { nodes, tipDecorations, sparkles, rings };
}

function createArmGradient(ctx, params) {
    const gradient = ctx.createLinearGradient(0, 0, params.radius, 0);
    gradient.addColorStop(0, rgba(params.coreColor, 0.9));
    gradient.addColorStop(0.45, params.color);
    gradient.addColorStop(1, lighten(params.color, 0.25));
    return gradient;
}

function drawBackground(ctx, params) {
    const { width, height } = ctx.canvas;
    const gradient = ctx.createRadialGradient(
        width / 2,
        height / 2,
        Math.min(width, height) * 0.05,
        width / 2,
        height / 2,
        Math.max(width, height) * 0.65,
    );
    gradient.addColorStop(0, rgba(lighten(params.background, 0.2), 0.95));
    gradient.addColorStop(1, rgba(darken(params.background, 0.15), 1));

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
}

function drawSparkles(ctx, params, structure, pulse) {
    ctx.save();
    ctx.fillStyle = rgba(lighten(params.accentColor, 0.2), 0.45 + pulse * 0.2);
    structure.sparkles.forEach((sparkle) => {
        const radius = sparkle.distance * (1 + pulse * params.pulseStrength * 0.3);
        const x = Math.cos(sparkle.angle) * radius;
        const y = Math.sin(sparkle.angle) * radius;
        ctx.globalAlpha = sparkle.alpha + pulse * 0.2;
        ctx.beginPath();
        ctx.arc(x, y, sparkle.size, 0, TAU);
        ctx.fill();
    });
    ctx.restore();
}

function drawCrystal(ctx, params, crystal, pulse) {
    ctx.save();
    ctx.rotate(crystal.rotation + pulse * 0.8);
    ctx.beginPath();
    const points = crystal.points;
    const radius = crystal.radius * (1 + pulse * params.pulseStrength * 0.4);
    for (let i = 0; i < points; i += 1) {
        const angle = (TAU / points) * i;
        const innerRadius = radius * 0.42;
        ctx.lineTo(Math.cos(angle) * radius, Math.sin(angle) * radius);
        ctx.lineTo(Math.cos(angle + TAU / (points * 2)) * innerRadius, Math.sin(angle + TAU / (points * 2)) * innerRadius);
    }
    ctx.closePath();
    ctx.fillStyle = rgba(params.accentColor, 0.25);
    ctx.fill();
    ctx.strokeStyle = rgba(params.accentColor, 0.6);
    ctx.lineWidth = params.lineWidth * 0.6;
    ctx.stroke();
    ctx.restore();
}

function drawArm(ctx, params, structure, pulse) {
    ctx.strokeStyle = createArmGradient(ctx, params);
    ctx.lineWidth = params.lineWidth;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(params.radius, 0);
    ctx.stroke();

    structure.nodes.forEach((node) => {
        const pulseFactor = 1 + pulse * params.pulseStrength;
        const branchLength = node.branchLength * (0.75 + pulse * params.pulseStrength * 0.2);
        ctx.save();
        ctx.translate(node.distance, node.lateral * pulse * 0.5);

        ctx.strokeStyle = rgba(params.color, 0.9);
        ctx.lineWidth = node.thickness;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(branchLength, 0);
        ctx.stroke();

        node.details.forEach((detail) => {
            ctx.save();
            ctx.rotate(detail.angle + pulse * params.pulseStrength * 0.35 * (detail.angle >= 0 ? 1 : -1));
            ctx.lineWidth = node.thickness * detail.thicknessFactor;
            ctx.strokeStyle = rgba(params.accentColor, 0.9);
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(branchLength * detail.lengthFactor * pulseFactor, 0);
            ctx.stroke();
            ctx.restore();
        });

        if (node.crystal) {
            drawCrystal(ctx, params, node.crystal, pulse);
        }

        ctx.restore();
    });

    structure.tipDecorations.forEach((tip) => {
        ctx.save();
        ctx.translate(tip.offset, 0);
        ctx.rotate(tip.angle + pulse * params.pulseStrength * 0.3);
        ctx.lineWidth = params.lineWidth * tip.thicknessFactor;
        ctx.strokeStyle = rgba(params.accentColor, 0.85);
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(params.radius * tip.lengthFactor * (0.8 + pulse * 0.2), 0);
        ctx.stroke();
        ctx.restore();
    });
}

function drawRings(ctx, params, structure, pulse) {
    ctx.save();
    ctx.strokeStyle = rgba(params.accentColor, 0.45 + pulse * 0.2);
    structure.rings.forEach((ring) => {
        ctx.lineWidth = ring.thickness;
        ctx.globalAlpha = ring.alpha + pulse * 0.1;
        ctx.beginPath();
        ctx.arc(0, 0, ring.radius * (1 + pulse * params.pulseStrength * 0.05), 0, TAU);
        ctx.stroke();
    });
    ctx.restore();
}

export function createSnowflakeState(params) {
    const structure = buildStructure(params);
    return { params, structure };
}

export function renderSnowflake(ctx, state, renderState = {}) {
    const { params, structure } = state;
    const { angle = 0, pulse = 0 } = renderState;

    drawBackground(ctx, params);

    ctx.save();
    const { width, height } = ctx.canvas;
    ctx.translate(width / 2, height / 2);
    const scale = Math.min(width, height) / ((params.radius * 2) + 120);
    ctx.scale(scale, scale);
    ctx.rotate(angle);

    ctx.shadowColor = rgba(params.color, 0.35 + params.glow * 0.4);
    ctx.shadowBlur = 30 + params.glow * 20;

    drawSparkles(ctx, params, structure, pulse);
    drawRings(ctx, params, structure, pulse);

    for (let i = 0; i < params.branches; i += 1) {
        ctx.save();
        ctx.rotate((TAU / params.branches) * i);
        drawArm(ctx, params, structure, pulse);
        ctx.restore();
    }

    ctx.restore();
}

function encodeBase64Unicode(str) {
    return btoa(unescape(encodeURIComponent(str)));
}

function decodeBase64Unicode(str) {
    try {
        return decodeURIComponent(escape(atob(str)));
    } catch (error) {
        return null;
    }
}

export function encodeParameters(params) {
    const json = JSON.stringify(params);
    return encodeBase64Unicode(json);
}

export function decodeParameters(hash) {
    if (!hash) return null;
    const clean = hash.replace(/^#?snowflake[:=]?/i, '');
    const json = decodeBase64Unicode(clean);
    if (!json) return null;
    try {
        const parsed = JSON.parse(json);
        if (!parsed || typeof parsed !== 'object') return null;
        return parsed;
    } catch (error) {
        return null;
    }
}

export function createShareableHash(params) {
    return `snowflake=${encodeParameters(params)}`;
}

export function withLimit(entries) {
    return entries.slice(0, MAX_GALLERY_ITEMS);
}

const TAU = Math.PI * 2;
const MAX_GALLERY_ITEMS = 24;
const SYMMETRY_OPTIONS = [6, 8, 12];

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
    return `#${toHex(clamp(Math.round(r), 0, 255))}${toHex(clamp(Math.round(g), 0, 255))}${toHex(clamp(Math.round(b), 0, 255))}`;
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

function chooseSymmetry(preferred, random) {
    if (!Number.isFinite(preferred)) {
        return SYMMETRY_OPTIONS[Math.floor(random() * SYMMETRY_OPTIONS.length)];
    }
    let closest = SYMMETRY_OPTIONS[0];
    let minDiff = Math.abs(closest - preferred);
    for (let i = 1; i < SYMMETRY_OPTIONS.length; i += 1) {
        const candidate = SYMMETRY_OPTIONS[i];
        const diff = Math.abs(candidate - preferred);
        if (diff < minDiff) {
            closest = candidate;
            minDiff = diff;
        }
    }
    return closest;
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

    const branchesSetting = Number.parseInt(settings.branches ?? settings.symmetry ?? 0, 10);
    const complexitySetting = Number.parseInt(settings.complexity ?? 0, 10);
    const radiusSetting = Number.parseInt(settings.size ?? 0, 10);
    const lineWidthSetting = Number.parseFloat(settings.lineWidth ?? 0);
    const baseColorSetting = (settings.color ?? '#4a90e2').toString().trim();

    const preferredBranches = overrides.branches ?? branchesSetting;
    const radialSymmetry = overrides.radialSymmetry ?? chooseSymmetry(preferredBranches, random);

    let branchCount;
    if (Number.isFinite(overrides.branches)) {
        branchCount = clamp(overrides.branches, 3, 14);
    } else if (Number.isFinite(branchesSetting) && branchesSetting >= 3) {
        branchCount = chooseSymmetry(branchesSetting, random);
    } else {
        branchCount = radialSymmetry;
    }

    const params = {
        seed,
        branches: clamp(branchCount, 3, 14),
        radialSymmetry: clamp(radialSymmetry, 3, 14),
        complexity: clamp(overrides.complexity ?? complexitySetting || Math.floor(3 + random() * 5), 1, 12),
        radius: clamp(overrides.radius ?? radiusSetting || Math.floor(260 + random() * 80), 120, 380),
        lineWidth: clamp(overrides.lineWidth ?? lineWidthSetting || (1.5 + random() * 1.5), 0.6, 6),
        color: (overrides.color ?? baseColorSetting).toLowerCase(),
        accentColor: overrides.accentColor ?? lighten(baseColorSetting, 0.25 + random() * 0.2),
        coreColor: overrides.coreColor ?? lighten(baseColorSetting, 0.18),
        background: overrides.background ?? darken(baseColorSetting, 0.75),
        branchSpread: overrides.branchSpread ?? (0.28 + random() * 0.4),
        branchJitter: overrides.branchJitter ?? (0.1 + random() * 0.2),
        secondaryBranches: overrides.secondaryBranches ?? Math.max(1, Math.round(2 + random() * 3)),
        tipDetails: overrides.tipDetails ?? Math.max(2, Math.round(3 + random() * 3)),
        sparkleCount: overrides.sparkleCount ?? Math.round(14 + random() * 18),
        animate: overrides.animate ?? true,
        spinSpeed: overrides.spinSpeed ?? (0.00025 + random() * 0.00055),
        pulseSpeed: overrides.pulseSpeed ?? (0.00035 + random() * 0.00045),
        pulseStrength: overrides.pulseStrength ?? (0.06 + random() * 0.09),
        glow: overrides.glow ?? (0.4 + random() * 0.4),
        galaxyDensity: overrides.galaxyDensity ?? (0.45 + random() * 0.55),
        starBrightness: overrides.starBrightness ?? (0.55 + random() * 0.35),
        starFalloff: overrides.starFalloff ?? (1.8 + random() * 1.4),
        nebulaIntensity: overrides.nebulaIntensity ?? (0.35 + random() * 0.4),
        nebulaScale: overrides.nebulaScale ?? (1.1 + random() * 0.9),
    };

    return params;
}

function generateNodes(params, random) {
    const nodes = [];
    for (let layer = 0; layer < params.complexity; layer += 1) {
        const progress = (layer + 1) / (params.complexity + 1);
        const distance = params.radius * progress;
        const branchLength = params.radius * (0.28 + (1 - progress) * 0.62) * (0.85 + random() * 0.3);
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
        const crystal = crystalChance > 0.68 ? {
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
    return nodes;
}

function generateTipDecorations(params, random) {
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
    return tipDecorations;
}

function generateSparkles(params, random) {
    const sparkles = [];
    for (let i = 0; i < params.sparkleCount; i += 1) {
        const distance = params.radius * (0.25 + random() * 0.85);
        const angle = random() * TAU;
        const size = 1 + random() * 2.8;
        sparkles.push({
            x: Math.cos(angle) * distance,
            y: Math.sin(angle) * distance,
            size,
            baseAlpha: 0.22 + random() * params.starBrightness * 0.8,
            falloff: params.starFalloff * (0.4 + random() * 0.55),
            twinkleSpeed: 0.6 + random() * 1.4,
            twinklePhase: random() * TAU,
        });
    }
    return sparkles;
}

function generateRings(params, random) {
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
    return rings;
}

function generateStarField(params, random) {
    const maxRadius = params.radius * (2.1 + params.nebulaScale * 0.6);
    const baseCount = 80 + Math.round(params.galaxyDensity * 40);
    const stars = [];
    for (let i = 0; i < baseCount; i += 1) {
        const distance = Math.pow(random(), 0.35) * maxRadius;
        const angle = random() * TAU;
        const x = Math.cos(angle) * distance;
        const y = Math.sin(angle) * distance;
        const size = 0.65 + random() * 1.8;
        stars.push({
            x,
            y,
            size,
            brightness: params.starBrightness * (0.35 + random() * 0.65) * (1 - distance / (maxRadius * 1.2)),
            falloff: params.starFalloff * (0.6 + random() * 0.9),
            twinkleSpeed: 0.25 + random() * 1.1,
            twinklePhase: random() * TAU,
        });
    }
    return stars;
}

function generateParticles(params, random) {
    const count = Math.round(24 + params.radius * 0.08 + random() * 22);
    const particles = [];
    for (let i = 0; i < count; i += 1) {
        const distance = params.radius * (0.15 + random() * 0.75);
        const angle = random() * TAU;
        const x = Math.cos(angle) * distance;
        const y = Math.sin(angle) * distance;
        particles.push({
            x,
            y,
            size: 0.8 + random() * 1.6,
            brightness: 0.3 + random() * 0.45,
            falloff: 0.9 + random() * 1.1,
            twinkleSpeed: 0.9 + random() * 1.6,
            twinklePhase: random() * TAU,
        });
    }
    return particles;
}

function generateNebulaLayers(params, random) {
    const layerCount = Math.max(2, Math.round(3 + params.nebulaIntensity * 3));
    const layers = [];
    const maxRadius = params.radius * (1.9 + params.nebulaScale);

    for (let i = 0; i < layerCount; i += 1) {
        const distance = params.radius * (0.2 + random() * params.nebulaScale);
        const angle = random() * TAU;
        const x = Math.cos(angle) * distance;
        const y = Math.sin(angle) * distance;
        const radius = maxRadius * (0.25 + random() * 0.45);
        layers.push({
            x,
            y,
            radius,
            inner: lighten(params.coreColor, 0.32 + random() * 0.28),
            mid: lighten(params.accentColor, 0.22 + random() * 0.22),
            outer: darken(params.background, 0.08 + random() * 0.16),
            alpha: 0.22 + params.nebulaIntensity * (0.32 + random() * 0.2),
            stretch: 1.1 + random() * 1.1,
            drift: 0.00008 + random() * 0.00014,
            phase: random() * TAU,
        });
    }

    return layers;
}

export function buildStructure(params) {
    const random = createRandom((params.seed ^ 0x9e3779b9) >>> 0);

    const nodes = generateNodes(params, random);
    const tipDecorations = generateTipDecorations(params, random);
    const sparkles = generateSparkles(params, random);
    const rings = generateRings(params, random);
    const starfield = generateStarField(params, random);
    const particles = generateParticles(params, random);
    const nebula = generateNebulaLayers(params, random);

    return {
        nodes,
        tipDecorations,
        sparkles,
        rings,
        particles,
        galaxy: {
            starfield,
            nebula,
        },
    };
}

function createArmGradient(ctx, params) {
    const gradient = ctx.createLinearGradient(0, 0, params.radius, 0);
    gradient.addColorStop(0, rgba(params.coreColor, 0.9));
    gradient.addColorStop(0.45, params.color);
    gradient.addColorStop(1, lighten(params.color, 0.25));
    return gradient;
}

function withRadialSymmetry(ctx, count, draw) {
    const safeCount = Math.max(3, Math.round(count));
    for (let i = 0; i < safeCount; i += 1) {
        ctx.save();
        ctx.rotate((TAU / safeCount) * i);
        draw();
        ctx.restore();
    }
}

function drawBackground(ctx, params) {
    const { width, height } = ctx.canvas;
    const gradient = ctx.createRadialGradient(
        width / 2,
        height / 2,
        Math.min(width, height) * 0.12,
        width / 2,
        height / 2,
        Math.max(width, height) * 0.75,
    );
    gradient.addColorStop(0, rgba(lighten(params.background, 0.18), 1));
    gradient.addColorStop(0.45, rgba(params.background, 1));
    gradient.addColorStop(1, rgba(darken(params.background, 0.1), 1));

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
}

function drawNebula(ctx, params, nebulaLayers, time) {
    if (!nebulaLayers?.length) return;
    const t = time * 0.001;
    ctx.save();
    nebulaLayers.forEach((layer) => {
        ctx.save();
        const oscillation = Math.sin(layer.phase + t * layer.drift * 1200);
        ctx.translate(layer.x * (1 + oscillation * 0.06), layer.y * (1 + oscillation * 0.06));
        ctx.rotate(layer.phase * 0.25 + t * layer.drift);
        ctx.scale(layer.stretch * (1 + oscillation * 0.05), 1 + oscillation * 0.04);
        const gradient = ctx.createRadialGradient(0, 0, layer.radius * 0.15, 0, 0, layer.radius);
        gradient.addColorStop(0, rgba(layer.inner, layer.alpha));
        gradient.addColorStop(0.5, rgba(layer.mid, layer.alpha * 0.8));
        gradient.addColorStop(1, rgba(layer.outer, 0));
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(0, 0, layer.radius, 0, TAU);
        ctx.fill();
        ctx.restore();
    });
    ctx.restore();
}

function drawStarfield(ctx, params, stars, time) {
    if (!stars?.length) return;
    const t = time * 0.001;
    ctx.save();
    stars.forEach((star) => {
        const twinkle = 0.6 + 0.4 * Math.sin(t * star.twinkleSpeed * 6 + star.twinklePhase);
        const alpha = clamp(star.brightness * twinkle, 0, 1);
        const radius = star.size * star.falloff;
        const gradient = ctx.createRadialGradient(star.x, star.y, 0, star.x, star.y, radius);
        gradient.addColorStop(0, `rgba(255, 255, 255, ${alpha})`);
        gradient.addColorStop(0.35, rgba(lighten(params.coreColor, 0.4), alpha * 0.85));
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(star.x, star.y, radius, 0, TAU);
        ctx.fill();
    });
    ctx.restore();
}

function drawParticles(ctx, params, particles, time, pulse) {
    if (!particles?.length) return;
    const t = time * 0.001;
    ctx.save();
    particles.forEach((particle) => {
        const twinkle = 0.6 + 0.4 * Math.sin(t * particle.twinkleSpeed * 4 + particle.twinklePhase);
        const alpha = clamp(particle.brightness * twinkle + pulse * 0.18, 0, 1);
        const radius = particle.size * (1 + pulse * params.pulseStrength * 0.18);
        const falloffRadius = radius * particle.falloff;
        const gradient = ctx.createRadialGradient(particle.x, particle.y, 0, particle.x, particle.y, falloffRadius);
        gradient.addColorStop(0, rgba(params.accentColor, alpha));
        gradient.addColorStop(0.8, rgba(lighten(params.accentColor, 0.2), alpha * 0.4));
        gradient.addColorStop(1, rgba(params.accentColor, 0));
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, falloffRadius, 0, TAU);
        ctx.fill();
    });
    ctx.restore();
}

function drawSparkles(ctx, params, sparkles, time, pulse) {
    if (!sparkles?.length) return;
    const t = time * 0.001;
    ctx.save();
    sparkles.forEach((sparkle) => {
        const twinkle = 0.65 + 0.35 * Math.sin(t * sparkle.twinkleSpeed * 3 + sparkle.twinklePhase);
        const alpha = clamp(sparkle.baseAlpha * twinkle + pulse * 0.2, 0, 1);
        const radius = sparkle.size * (1 + pulse * params.pulseStrength * 0.25);
        const falloffRadius = radius * sparkle.falloff;
        const gradient = ctx.createRadialGradient(sparkle.x, sparkle.y, 0, sparkle.x, sparkle.y, falloffRadius);
        gradient.addColorStop(0, rgba(lighten(params.accentColor, 0.22), alpha));
        gradient.addColorStop(0.5, rgba(params.accentColor, alpha * 0.65));
        gradient.addColorStop(1, rgba(params.accentColor, 0));
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(sparkle.x, sparkle.y, falloffRadius, 0, TAU);
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
            ctx.lineTo(branchLength * detail.lengthFactor * (1 + pulse * params.pulseStrength * 0.1), 0);
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
    if (!structure.rings?.length) return;
    ctx.save();
    ctx.strokeStyle = rgba(params.accentColor, 0.45 + pulse * 0.2);
    structure.rings.forEach((ring) => {
        ctx.lineWidth = ring.thickness;
        ctx.globalAlpha = clamp(ring.alpha + pulse * 0.1, 0, 1);
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
    const { angle = 0, pulse = 0, time = 0 } = renderState;

    drawBackground(ctx, params);

    ctx.save();
    const { width, height } = ctx.canvas;
    ctx.translate(width / 2, height / 2);
    const scale = Math.min(width, height) / ((params.radius * 2) + 120);
    ctx.scale(scale, scale);
    ctx.rotate(angle);

    ctx.shadowColor = rgba(params.color, 0.35 + params.glow * 0.4);
    ctx.shadowBlur = 30 + params.glow * 20;

    drawNebula(ctx, params, structure.galaxy.nebula, time);
    drawStarfield(ctx, params, structure.galaxy.starfield, time);
    drawParticles(ctx, params, structure.particles, time, pulse);
    drawSparkles(ctx, params, structure.sparkles, time, pulse);
    drawRings(ctx, params, structure, pulse);

    const branchCount = params.radialSymmetry ?? params.branches;
    withRadialSymmetry(ctx, branchCount, () => {
        drawArm(ctx, params, structure, pulse);
    });

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

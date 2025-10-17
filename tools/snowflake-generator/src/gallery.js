import { createSnowflakeState, renderSnowflake, withLimit } from './snowflake.js';

const GALLERY_STORAGE_KEY = 'snowflake-gallery';
const THUMBNAIL_SIZE = 200;

export class GalleryManager {
    constructor() {
        this.entries = this.loadEntries();
        this.panel = document.getElementById('galleryPanel');
        this.grid = document.getElementById('galleryGrid');
        this.isOpen = false;
        this.onExportCallback = null;
        this.onApplyCallback = null;

        this.setupEventListeners();
    }

    setupEventListeners() {
        const closeBtn = document.getElementById('closeGalleryBtn');
        const exportAllBtn = document.getElementById('exportAllBtn');
        const clearAllBtn = document.getElementById('clearGalleryBtn');

        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.close());
        }

        if (exportAllBtn) {
            exportAllBtn.addEventListener('click', () => this.exportAll());
        }

        if (clearAllBtn) {
            clearAllBtn.addEventListener('click', () => this.clearAll());
        }
    }

    loadEntries() {
        if (typeof window === 'undefined' || typeof window.localStorage === 'undefined') {
            return [];
        }

        try {
            const stored = window.localStorage.getItem(GALLERY_STORAGE_KEY);
            if (!stored) return [];
            const parsed = JSON.parse(stored);
            return withLimit(Array.isArray(parsed) ? parsed : []);
        } catch (error) {
            console.error('Failed to load gallery entries:', error);
            return [];
        }
    }

    saveEntries() {
        if (typeof window === 'undefined' || typeof window.localStorage === 'undefined') {
            return;
        }

        try {
            const limited = withLimit(this.entries);
            window.localStorage.setItem(GALLERY_STORAGE_KEY, JSON.stringify(limited));
            this.entries = limited;
        } catch (error) {
            console.error('Failed to save gallery entries:', error);
            if (error.name === 'QuotaExceededError') {
                this.entries = this.entries.slice(0, Math.floor(this.entries.length / 2));
                this.saveEntries();
            }
        }
    }

    add(params) {
        const timestamp = Date.now();
        const id = `${timestamp}-${Math.random().toString(36).substring(2, 9)}`;

        const thumbnailCanvas = document.createElement('canvas');
        thumbnailCanvas.width = THUMBNAIL_SIZE;
        thumbnailCanvas.height = THUMBNAIL_SIZE;
        const thumbnailCtx = thumbnailCanvas.getContext('2d');

        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = 800;
        tempCanvas.height = 800;
        const tempCtx = tempCanvas.getContext('2d');

        const state = createSnowflakeState(params);
        renderSnowflake(tempCtx, state, { angle: 0, pulse: 0 });

        thumbnailCtx.drawImage(tempCanvas, 0, 0, 800, 800, 0, 0, THUMBNAIL_SIZE, THUMBNAIL_SIZE);
        const thumbnailData = thumbnailCanvas.toDataURL('image/png');

        const entry = {
            id,
            timestamp,
            params,
            thumbnail: thumbnailData,
        };

        this.entries.unshift(entry);
        this.entries = withLimit(this.entries);
        this.saveEntries();
        this.render();

        return entry;
    }

    remove(id) {
        this.entries = this.entries.filter((entry) => entry.id !== id);
        this.saveEntries();
        this.render();
    }

    clear() {
        this.entries = [];
        this.saveEntries();
        this.render();
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        if (this.panel) {
            this.isOpen = true;
            this.panel.classList.add('active');
        }
        this.render();
    }

    close() {
        this.isOpen = false;
        if (this.panel) {
            this.panel.classList.remove('active');
        }
    }

    render() {
        if (!this.grid) {
            return;
        }

        if (this.entries.length === 0) {
            this.grid.innerHTML = '<div class="gallery-empty">No snowflakes captured yet. Use "Add to Gallery" or press \'C\' to start collecting!</div>';
            return;
        }

        this.grid.innerHTML = '';

        this.entries.forEach((entry) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'gallery-item';
            itemDiv.dataset.id = entry.id;

            const img = document.createElement('img');
            img.src = entry.thumbnail;
            img.alt = 'Snowflake thumbnail';

            const actions = document.createElement('div');
            actions.className = 'gallery-item-actions';

            const applyBtn = document.createElement('button');
            applyBtn.textContent = 'Apply';
            applyBtn.className = 'btn btn-sm btn-primary';
            applyBtn.addEventListener('click', () => {
                if (this.onApplyCallback) {
                    this.onApplyCallback(entry.params);
                }
            });

            const exportBtn = document.createElement('button');
            exportBtn.textContent = 'Export';
            exportBtn.className = 'btn btn-sm btn-success';
            exportBtn.addEventListener('click', () => {
                if (this.onExportCallback) {
                    this.onExportCallback(entry.params, entry.id);
                }
            });

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.className = 'btn btn-sm btn-danger';
            deleteBtn.addEventListener('click', () => {
                if (confirm('Delete this snowflake from gallery?')) {
                    this.remove(entry.id);
                }
            });

            actions.appendChild(applyBtn);
            actions.appendChild(exportBtn);
            actions.appendChild(deleteBtn);

            const timestampDiv = document.createElement('div');
            timestampDiv.className = 'gallery-timestamp';
            const date = new Date(entry.timestamp);
            timestampDiv.textContent = date.toLocaleString();

            itemDiv.appendChild(img);
            itemDiv.appendChild(actions);
            itemDiv.appendChild(timestampDiv);

            this.grid.appendChild(itemDiv);
        });
    }

    exportAll() {
        if (this.entries.length === 0) {
            this.showNotification('No snowflakes to export', 'error');
            return;
        }

        this.entries.forEach((entry, index) => {
            setTimeout(() => {
                if (this.onExportCallback) {
                    this.onExportCallback(entry.params, `gallery-${index + 1}`);
                }
            }, index * 200);
        });

        this.showNotification(`Exporting ${this.entries.length} snowflakes...`, 'success');
    }

    clearAll() {
        if (this.entries.length === 0) return;

        if (confirm(`Delete all ${this.entries.length} snowflakes from gallery? This cannot be undone.`)) {
            this.clear();
            this.showNotification('Gallery cleared', 'success');
        }
    }

    showNotification(message, type = 'info') {
        const notificationEl = document.getElementById('notification');
        if (!notificationEl) return;

        notificationEl.textContent = message;
        notificationEl.className = `notification ${type}`;
        notificationEl.classList.add('show');

        setTimeout(() => {
            notificationEl.classList.remove('show');
        }, 3000);
    }

    onExport(callback) {
        this.onExportCallback = callback;
    }

    onApply(callback) {
        this.onApplyCallback = callback;
    }

    getCount() {
        return this.entries.length;
    }

    isEmpty() {
        return this.entries.length === 0;
    }
}

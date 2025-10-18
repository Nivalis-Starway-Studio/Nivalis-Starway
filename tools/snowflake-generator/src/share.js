import { createShareableHash } from './snowflake.js';

export async function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (error) {
            console.warn('Clipboard API failed, using fallback:', error);
        }
    }

    return fallbackCopy(text);
}

function fallbackCopy(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        return successful;
    } catch (error) {
        console.error('Fallback copy failed:', error);
        document.body.removeChild(textArea);
        return false;
    }
}

export class ShareManager {
    constructor() {
        this.menu = document.getElementById('shareMenu');
        this.button = document.getElementById('shareBtn');
        this.isOpen = false;

        this.setupEventListeners();
    }

    setupEventListeners() {
        if (this.button) {
            this.button.addEventListener('click', (event) => {
                event.stopPropagation();
                this.toggle();
            });
        }

        document.addEventListener('click', () => {
            if (this.isOpen) {
                this.close();
            }
        });

        if (this.menu) {
            this.menu.addEventListener('click', (event) => {
                event.stopPropagation();
            });
        }

        const options = document.querySelectorAll('.share-option');
        options.forEach((option) => {
            option.addEventListener('click', () => {
                const type = option.dataset.share;
                this.handleShare(type);
            });
        });
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        this.isOpen = true;
        if (this.menu) {
            this.menu.hidden = false;
        }
    }

    close() {
        this.isOpen = false;
        if (this.menu) {
            this.menu.hidden = true;
        }
    }

    async handleShare(type) {
        if (!this.getCurrentParams) {
            console.error('getCurrentParams callback not set');
            this.showNotification('Share failed: no parameters', 'error');
            return;
        }

        const params = this.getCurrentParams();
        if (!params) {
            this.showNotification('No parameters to share', 'error');
            return;
        }

        try {
            let textToCopy = '';

            if (type === 'json') {
                textToCopy = JSON.stringify(params, null, 2);
            } else if (type === 'link') {
                const hash = createShareableHash(params);
                if (window.history?.replaceState) {
                    window.history.replaceState(null, '', `#${hash}`);
                } else {
                    window.location.hash = hash;
                }

                const base = window.location.href.split('#')[0];
                textToCopy = `${base}#${hash}`;
            }

            const success = await copyToClipboard(textToCopy);

            if (success) {
                this.showNotification(`${type === 'json' ? 'Parameters JSON' : 'Shareable link'} copied to clipboard!`, 'success');
                this.close();
            } else {
                this.showNotification('Failed to copy to clipboard', 'error');
            }
        } catch (error) {
            console.error('Share error:', error);
            this.showNotification('Share failed', 'error');
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

    onGetCurrentParams(callback) {
        this.getCurrentParams = callback;
    }
}

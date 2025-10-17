const defaultFilter = (event) => {
    const target = event.target;
    if (!target) return true;
    const tag = target.tagName?.toLowerCase();
    const editable = target.isContentEditable;
    return !(tag === 'input' || tag === 'textarea' || editable);
};

export function registerKeyboardShortcuts(bindings, options = {}) {
    const filter = options.filter ?? defaultFilter;

    const handler = (event) => {
        if (!filter(event)) {
            return;
        }

        const { code, key, ctrlKey, metaKey, shiftKey } = event;
        const match = bindings.find((binding) => {
            if (binding.code && binding.code !== code) return false;
            if (binding.key && binding.key.toLowerCase() !== key.toLowerCase()) return false;
            if (binding.ctrl && !(ctrlKey || metaKey)) return false;
            if (!binding.ctrl && (ctrlKey || metaKey)) return false;
            if (binding.shift && !shiftKey) return false;
            if (!binding.shift && shiftKey) return false;
            return true;
        });

        if (match) {
            event.preventDefault();
            match.action(event);
        }
    };

    window.addEventListener('keydown', handler);

    return () => window.removeEventListener('keydown', handler);
}

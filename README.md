# Snowflake Generator

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Nivalis-Starway-Studio/Nivalis-Starway)

A beautiful, interactive snowflake generator with advanced features including keyboard shortcuts, sharing functionality, and gallery management.

## Features

- **Procedural Generation**: Create unique, algorithmically-generated snowflakes
- **Radial Symmetry**: 6-fold, 8-fold, or 12-fold symmetrical patterns
- **Galaxy Effects**: Nebula-style gradients and star field backgrounds
- **Real-time Animation**: Smooth rotation and pulsing effects with twinkling stars
- **Keyboard Shortcuts**: Quick access to common actions
- **Share Functionality**: Copy parameters as JSON or shareable links
- **Gallery System**: Save, manage, and export multiple snowflakes
- **High-Quality Export**: Export snowflakes as 2400x2400 PNG images
- **Responsive Canvas**: Auto-resizes to fit different screen sizes
- **Performance Optimized**: Efficient rendering with minimal CPU usage

## Quick Start

1. Open `index.html` in a modern web browser
2. Adjust parameters using the control sliders
3. Click "Generate New" or press `G` to create a new snowflake
4. Press `C` to save snowflakes to your gallery
5. Press `E` to export as a high-resolution PNG

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `G` | Generate new snowflake |
| `A` | Toggle animation on/off |
| `E` | Quick export as PNG |
| `S` | Open share menu |
| `C` | Capture to gallery |
| `V` | View/hide gallery |

## Features Documentation

For detailed documentation about all features, see [FEATURES.md](FEATURES.md).

## Parameters

- **Branches**: Number of symmetrical arms (3-12)
- **Complexity**: Level of detail and intricacy (1-10)
- **Size**: Overall radius of the snowflake (100-400px)
- **Line Width**: Thickness of the lines (1-5px)
- **Color**: Base color for the snowflake

## Browser Compatibility

Requires a modern web browser with support for:
- HTML5 Canvas API
- ES6+ JavaScript modules
- LocalStorage (for gallery persistence)
- Clipboard API (for sharing)

Tested on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Technology Stack

- Pure HTML5, CSS3, and JavaScript (ES6+)
- No external dependencies
- Canvas API for rendering
- LocalStorage for persistence
- ES6 modules for code organization

## Project Structure

```
├── index.html          # Main application page
├── styles/
│   └── main.css       # Complete styling
├── src/
│   ├── main.js        # Application controller
│   ├── snowflake.js   # Core snowflake generation
│   ├── gallery.js     # Gallery management
│   ├── keyboard.js    # Keyboard shortcuts
│   └── share.js       # Share functionality
├── FEATURES.md        # Detailed feature documentation
└── README.md          # This file
```

## Development

The application uses ES6 modules. To develop locally, you may need to serve the files through a local web server due to CORS restrictions on file:// URLs.

Simple options:
```bash
# Python 3
python3 -m http.server 8000

# Node.js (with npx)
npx serve

# PHP
php -S localhost:8000
```

Then open `http://localhost:8000` in your browser.

## Performance Considerations

- Gallery limited to 24 snowflakes to prevent memory issues
- Thumbnails stored at 200x200 for efficient storage
- Animation uses requestAnimationFrame for 60fps performance
- Exports use temporary canvases that are cleaned up immediately

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Credits

Developed by **Nivalis Starway Studio** (牧星雪缘工作室)

---

Enjoy creating beautiful snowflakes! ❄️

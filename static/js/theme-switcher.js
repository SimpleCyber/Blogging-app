// First, let's add our dark mode CSS variables to the existing root variables
document.querySelector(':root').style.cssText += `
    --light-primary-color: #2d3436;
    --light-secondary-color: #636e72;
    --light-accent-color: #0984e3;
    --light-background-color: #f5f6fa;
    --light-header-bg: #ffffff;
    --light-card-bg: #ffffff;
    --light-text-color: #2d3436;
    --light-border-color: #eee;

    --dark-primary-color: #f5f6fa;
    --dark-secondary-color: #b2bec3;
    --dark-accent-color: #74b9ff;
    --dark-background-color: #1a1a1a;
    --dark-header-bg: #2d3436;
    --dark-card-bg: #2d3436;
    --dark-text-color: #f5f6fa;
    --dark-border-color: #404040;
`;

// Theme switcher class
class ThemeSwitcher {
    constructor() {
        this.themeButton = document.querySelector('.fa-sun');
        this.isDarkMode = localStorage.getItem('darkMode') === 'true';
        this.init();
    }

    init() {
        // Apply initial theme
        this.applyTheme(this.isDarkMode);
        
        // Add click event listener
        this.themeButton.addEventListener('click', () => {
            this.isDarkMode = !this.isDarkMode;
            this.applyTheme(this.isDarkMode);
            localStorage.setItem('darkMode', this.isDarkMode);
        });
    }

    applyTheme(isDark) {
        const root = document.documentElement;
        
        // Update icon
        this.themeButton.className = isDark ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
        
        // Apply theme with transition
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        
        // Update CSS variables
        root.style.setProperty('--primary-color', isDark ? 'var(--dark-primary-color)' : 'var(--light-primary-color)');
        root.style.setProperty('--secondary-color', isDark ? 'var(--dark-secondary-color)' : 'var(--light-secondary-color)');
        root.style.setProperty('--accent-color', isDark ? 'var(--dark-accent-color)' : 'var(--light-accent-color)');
        root.style.setProperty('--background-color', isDark ? 'var(--dark-background-color)' : 'var(--light-background-color)');
        root.style.setProperty('--header-bg', isDark ? 'var(--dark-header-bg)' : 'var(--light-header-bg)');
        root.style.setProperty('--text-color', isDark ? 'var(--dark-text-color)' : 'var(--light-text-color)');
        
        // Update additional elements
        const cards = document.querySelectorAll('.post, .blog1');
        cards.forEach(card => {
            card.style.transition = 'background-color 0.3s ease';
            card.style.backgroundColor = isDark ? 'var(--dark-card-bg)' : 'var(--light-card-bg)';
        });

        // Update borders
        const borders = document.querySelectorAll('.post, .blog1, .achive');
        borders.forEach(border => {
            border.style.borderColor = isDark ? 'var(--dark-border-color)' : 'var(--light-border-color)';
        });

        // Add/remove dark mode class to body
        document.body.classList.toggle('dark-mode', isDark);
    }
}

// Initialize theme switcher
document.addEventListener('DOMContentLoaded', () => {
    new ThemeSwitcher();
});

// Add smooth transition for initial page load
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    }, 100);
});

// Handle dynamic content updates
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'childList') {
            const themeSwitcher = new ThemeSwitcher();
            themeSwitcher.applyTheme(localStorage.getItem('darkMode') === 'true');
        }
    });
});

// Start observing the document body for dynamic content changes
observer.observe(document.body, {
    childList: true,
    subtree: true
});
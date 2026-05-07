document.addEventListener('DOMContentLoaded', () => {

    // ── Sidebar Toggle ──
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mainWrapper = document.querySelector('.main-wrapper');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                // Mobile behavior: toggle open class
                sidebar.classList.toggle('open');
            } else {
                // Desktop behavior: toggle closed class and expand main wrapper
                sidebar.classList.toggle('closed');
                mainWrapper.classList.toggle('expanded');
            }
        });
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && 
            sidebar.classList.contains('open') && 
            !sidebar.contains(e.target) && 
            e.target !== sidebarToggle &&
            !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    });

    // ── Sidebar Accoridons ──
    const submenus = document.querySelectorAll('.has-submenu');
    submenus.forEach(menu => {
        menu.addEventListener('click', (e) => {
            e.preventDefault();
            // Toggle this submenu
            const isOpen = menu.classList.toggle('open');
            const submenu = menu.nextElementSibling;
            if (submenu && submenu.classList.contains('nav-submenu')) {
                submenu.classList.toggle('open');
            }
            // Close other open submenus
            document.querySelectorAll('.has-submenu.open').forEach(other => {
                if (other !== menu) {
                    other.classList.remove('open');
                    const otherSub = other.nextElementSibling;
                    if (otherSub && otherSub.classList.contains('nav-submenu')) {
                        otherSub.classList.remove('open');
                    }
                }
            });
        });
    });

    // Close any open submenu when clicking a non-submenu nav item
    document.addEventListener('click', (e) => {
        const target = e.target.closest('.nav-item');
        if (target && !target.classList.contains('has-submenu')) {
            document.querySelectorAll('.has-submenu.open').forEach(openMenu => {
                openMenu.classList.remove('open');
                const sub = openMenu.nextElementSibling;
                if (sub && sub.classList.contains('nav-submenu')) {
                    sub.classList.remove('open');
                }
            });
        }
    });

    // ── Form Clear Button ──
    const clearBtn = document.getElementById('clearBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            const form = document.getElementById('ptrForm');
            if (confirm('Are you sure you want to clear the entire form?')) {
                form.reset();
            }
        });
    }

    // ── Active Navigation State ──
    // Get the current URL path
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        // Find links that are NOT '#'
        if (href && href !== '#') {
            if (href === '/' && currentPath === '/') {
                document.querySelectorAll('.nav-item.active').forEach(old => old.classList.remove('active'));
                item.classList.add('active');
            } else if (href !== '/' && currentPath.includes(href)) {
                document.querySelectorAll('.nav-item.active').forEach(old => old.classList.remove('active'));
                item.classList.add('active');
            }
        }
    });

});

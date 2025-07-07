// main.js
// Entry point for AI Tutor web app: handles navigation, feature selection, and UI feedback

document.addEventListener('DOMContentLoaded', function () {
    // Navigation: highlight active feature in sidebar/menu
    const navLinks = document.querySelectorAll('.nav-feature-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Feature form auto-fill for demo/testing (optional)
    document.querySelectorAll('.feature-form').forEach(form => {
        const autofillBtn = form.querySelector('.autofill-demo');
        if (autofillBtn) {
            autofillBtn.addEventListener('click', function (e) {
                e.preventDefault();
                // Example: fill with demo data based on feature
                const key = form.dataset.featureKey;
                if (key === 'multi_grade') {
                    form.querySelector('[name=topic]').value = 'Photosynthesis';
                    form.querySelector('[name=grade_levels]').value = '["Grade 4", "Grade 5"]';
                } else if (key === 'voice_assistant') {
                    form.querySelector('[name=transcript]').value = 'What is the homework for today?';
                } // Add more demo data as needed
            });
        }
    });

    // Global notification system
    window.showNotification = function (msg, type = 'info') {
        let notif = document.getElementById('global-notification');
        if (!notif) {
            notif = document.createElement('div');
            notif.id = 'global-notification';
            notif.style.position = 'fixed';
            notif.style.top = '20px';
            notif.style.right = '20px';
            notif.style.zIndex = 9999;
            notif.style.padding = '12px 24px';
            notif.style.borderRadius = '6px';
            notif.style.background = type === 'error' ? '#f44336' : '#2196f3';
            notif.style.color = '#fff';
            notif.style.fontWeight = 'bold';
            document.body.appendChild(notif);
        }
        notif.textContent = msg;
        notif.style.display = 'block';
        setTimeout(() => { notif.style.display = 'none'; }, 3000);
    };
});

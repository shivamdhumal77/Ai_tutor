// feature.js
// Handles dynamic feature requests and UI updates for the AI Tutor app

document.addEventListener('DOMContentLoaded', function () {
    // Attach event listeners to all feature forms/buttons
    const featureForms = document.querySelectorAll('.feature-form');
    featureForms.forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const featureKey = form.dataset.featureKey;
            const endpoint = `/feature/${featureKey}`;
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                // Try to parse JSON fields, fallback to string
                try {
                    data[key] = JSON.parse(value);
                } catch {
                    data[key] = value;
                }
            });
            showLoading(form);
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                showFeatureResponse(form, result);
            } catch (err) {
                showFeatureResponse(form, { error: 'Network or server error.' });
            } finally {
                hideLoading(form);
            }
        });
    });
});

function showLoading(form) {
    let loader = form.querySelector('.feature-loader');
    if (!loader) {
        loader = document.createElement('div');
        loader.className = 'feature-loader';
        loader.textContent = 'Loading...';
        form.appendChild(loader);
    }
    loader.style.display = 'block';
}

function hideLoading(form) {
    const loader = form.querySelector('.feature-loader');
    if (loader) loader.style.display = 'none';
}

function showFeatureResponse(form, result) {
    let output = form.querySelector('.feature-output');
    if (!output) {
        output = document.createElement('div');
        output.className = 'feature-output';
        form.appendChild(output);
    }
    output.innerHTML = '';
    if (result.error) {
        output.innerHTML = `<span class="error">${result.error}</span>`;
    } else if (result.response) {
        if (typeof result.response === 'object') {
            output.innerHTML = `<pre>${JSON.stringify(result.response, null, 2)}</pre>`;
        } else {
            output.textContent = result.response;
        }
    } else {
        output.textContent = 'No response.';
    }
}

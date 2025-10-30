document.addEventListener('DOMContentLoaded', function() {
    // Handle logo loading
    const logoImg = document.getElementById('logoImg');
    const logoPlaceholder = document.getElementById('logoPlaceholder');

    if (logoImg) {
        logoImg.addEventListener('error', function() {
            // If logo fails to load, show the placeholder
            logoImg.style.display = 'none';
            if (logoPlaceholder) {
                logoPlaceholder.classList.add('show');
            }
            console.log('Logo not found - showing placeholder');
        });
    }

    const registrationForm = document.getElementById('registrationForm');
    const messageContainer = document.getElementById('messageContainer');

    // Handle form submission
    registrationForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get form values
        const formData = {
            first_name: document.getElementById('firstName').value.trim(),
            last_name: document.getElementById('lastName').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone_number: document.getElementById('phone').value.trim() || null,
            birth_date: document.getElementById('birthDate').value || null
        };

        // Disable submit button during submission
        const submitButton = registrationForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = 'Inscription en cours...';

        try {
            // Send data to server
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                // Show success message with celebration effect
                showSuccessMessage(result.message, result.student_code);

                // Reset form
                registrationForm.reset();

                // Auto-scroll to top to see success message
                messageContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });

                // Start countdown and redirect
                startCountdownRedirect();
            } else {
                // Error message
                showMessage(result.error, 'error');

                // Reset button
                submitButton.disabled = false;
                submitButton.textContent = 'S\'inscrire';
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Une erreur s\'est produite. Veuillez réessayer.', 'error');

            // Reset button
            submitButton.disabled = false;
            submitButton.textContent = 'S\'inscrire';
        }
    });

    // Show success message with celebration animation
    function showSuccessMessage(message, studentCode) {
        const successHTML = `
            <div class="message success success-expanded">
                <div class="success-content">
                    <div class="success-icon">✓</div>
                    <div class="success-text">
                        <strong>${message}</strong>
                        <p>Redirection en cours...</p>
                    </div>
                </div>
                <div class="countdown-container">
                    <span class="countdown-text">Redirection dans </span>
                    <span class="countdown-number" id="countdown">5</span>
                    <span class="countdown-text"> secondes</span>
                </div>
            </div>
        `;
        messageContainer.innerHTML = successHTML;
        messageContainer.style.display = 'block';

        // Trigger celebration effect
        celebrationEffect();
    }

    // Show regular message function
    function showMessage(message, type) {
        messageContainer.innerHTML = `<div class="message ${type}">${message}</div>`;
        messageContainer.style.display = 'block';

        // Auto-hide error messages after 5 seconds
        if (type === 'error') {
            setTimeout(() => {
                messageContainer.style.display = 'none';
            }, 5000);
        }
    }

    // Countdown and redirect
    function startCountdownRedirect() {
        let count = 5;
        const countdownElement = document.getElementById('countdown');

        const countdownInterval = setInterval(() => {
            count--;
            if (countdownElement) {
                countdownElement.textContent = count;
            }

            if (count <= 0) {
                clearInterval(countdownInterval);
                // Redirect to home page
                window.location.href = '/';
            }
        }, 1000);
    }

    // Celebration effect with confetti-like animation
    function celebrationEffect() {
        // Create confetti particles
        for (let i = 0; i < 30; i++) {
            createConfetti();
        }

        // Add pulse animation to success message
        const successMessage = messageContainer.querySelector('.message.success');
        if (successMessage) {
            successMessage.style.animation = 'pulse 0.6s ease-in-out';
        }
    }

    // Create confetti particles - Japanese color palette (red, white, black)
    function createConfetti() {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';

        // Random properties
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight - window.innerHeight;
        const size = Math.random() * 8 + 4;
        const duration = Math.random() * 2 + 2;
        const delay = Math.random() * 0.5;

        // Japanese color palette - Red, white, black
        const colors = ['#c41e3a', '#ffffff', '#1a1a1a'];
        const color = colors[Math.floor(Math.random() * colors.length)];

        // For white confetti, add a border
        let style = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            width: ${size}px;
            height: ${size}px;
            background-color: ${color};
            border-radius: 50%;
            pointer-events: none;
            animation: fall ${duration}s linear ${delay}s forwards;
            z-index: 9999;
        `;

        if (color === '#ffffff') {
            style += `border: 1px solid #1a1a1a;`;
        }

        confetti.style.cssText = style;

        document.body.appendChild(confetti);

        // Remove confetti after animation
        setTimeout(() => {
            confetti.remove();
        }, (duration + delay) * 1000);
    }

    // Clear message on input change
    const inputs = registrationForm.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            if (messageContainer.querySelector('.message.error')) {
                messageContainer.style.display = 'none';
            }
        });
    });
});

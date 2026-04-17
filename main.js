document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("theme-toggle");
    const body = document.body;

    function applyTheme(isDark) {
        if (isDark) {
            body.classList.add("dark");
            if (toggle) toggle.textContent = "☀️";
        } else {
            body.classList.remove("dark");
            if (toggle) toggle.textContent = "🌓";
        }
    }

    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        applyTheme(true);
    }

    if (toggle) {
        toggle.addEventListener("click", () => {
            const isDark = !body.classList.contains("dark");
            applyTheme(isDark);
            localStorage.setItem("theme", isDark ? "dark" : "light");
        });
    }

    // Particle Background
    const canvas = document.getElementById('bg-particles');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        let particlesArray = [];
        let mouse = { x: null, y: null, radius: 100 };

        window.addEventListener('mousemove', function(event) {
            mouse.x = event.x;
            mouse.y = event.y;
        });

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 1;
                this.baseX = this.x;
                this.baseY = this.y;
                this.density = (Math.random() * 30) + 1;
            }
            draw() {
                ctx.fillStyle = body.classList.contains('dark') ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.1)';
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.closePath();
                ctx.fill();
            }
            update() {
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < mouse.radius) {
                    this.x -= dx / 10;
                    this.y -= dy / 10;
                } else {
                    if (this.x !== this.baseX) this.x -= (this.x - this.baseX) / 10;
                    if (this.y !== this.baseY) this.y -= (this.y - this.baseY) / 10;
                }
                this.draw();
            }
        }

        function init() {
            particlesArray = [];
            for (let i = 0; i < 80; i++) particlesArray.push(new Particle());
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particlesArray.length; i++) particlesArray[i].update();
            requestAnimationFrame(animate);
        }
        init();
        animate();
    }
});

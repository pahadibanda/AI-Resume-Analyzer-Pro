/**
 * Premium tsParticles Galaxy Configuration
 * Luxury AI/SaaS Background Design
 * 
 * Customize colors, speed, density, and interactive events below.
 */

(function() {
  function initParticles() {
    // Safety check if tsParticles library is fully loaded
    if (typeof tsParticles === 'undefined') {
      setTimeout(initParticles, 100);
      return;
    }

    // Initialize tsParticles on the container with ID "tsparticles"
    tsParticles.load("tsparticles", {
      // 60 FPS limit ensures battery efficiency and smooth render
      fpsLimit: 60,
      
      // Particle Properties
      particles: {
        // Particle Count & Density Rules
        number: {
          value: window.innerWidth < 768 ? 150 : 380, // Responsive count reduction
          density: {
            enable: true,
            area: 800
          }
        },
        
        // Color (White stars)
        color: {
          value: "#ffffff"
        },
        
        // Shape (Simple clean circular stars)
        shape: {
          type: "circle"
        },
        
        // Opacity animation (twinkle glow)
        opacity: {
          value: { min: 0.15, max: 0.85 },
          animation: {
            enable: true,
            speed: 0.6,
            sync: false
          }
        },
        
        // Random star sizes (1px to 3.5px)
        size: {
          value: { min: 1, max: 3.5 }
        },
        
        // Slow drifting movement
        move: {
          enable: true,
          speed: 0.45,
          direction: "none",
          random: true,
          straight: false,
          outModes: {
            default: "out"
          }
        },
        
        // Star Twinkling settings (Pulsing violet twinkle colors)
        twinkle: {
          particles: {
            enable: true,
            color: "#c084fc", // Soft purple twinkle highlight
            frequency: 0.05,
            opacity: 1
          }
        }
      },
      
      // Mouse Interaction Settings
      interactivity: {
        detectsOn: "window",
        events: {
          onHover: {
            enable: true,
            mode: "grab" // Draws light digital links on hover
          },
          onClick: {
            enable: true,
            mode: "push" // Burst effect on mouse click
          },
          resize: true
        },
        modes: {
          grab: {
            distance: 130,
            links: {
              opacity: 0.15,
              color: "#c084fc"
            }
          },
          push: {
            quantity: 4 // Create 4 new particles on click
          }
        }
      },
      
      // Enable Retina Display optimization
      detectRetina: true
    });
  }

  // Execute initialization when document structure is active
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    initParticles();
  } else {
    document.addEventListener('DOMContentLoaded', initParticles);
  }
})();

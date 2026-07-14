from streamlit_option_menu import option_menu
import streamlit as st
import streamlit.components.v1 as components


def render_navbar(default_index=0, key=None):
    # Suppress the outer container gap / border artifact
    st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] > div:first-child {
  flex: unset !important;
}
/* Remove the rectangular box that appears above the nav */
.st-emotion-cache-nakbow, .st-emotion-cache-1uelh5h {
  padding: 0 !important;
  margin: 0 !important;
  border: none !important;
  background: transparent !important;
}
div[data-testid="stHorizontalBlock"]:has(nav) {
  margin-bottom: 0 !important;
}

/* Centered transparent container wrapper for option_menu horizontal navbar */
div.stElementContainer:has(iframe[title*="streamlit_option_menu"]),
div.stElementContainer:has(iframe[title*="streamlit_option_menu"]) > div {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    padding: 0 !important;
    margin: 0 auto 20px auto !important;
    max-width: 1100px !important;
    width: 100% !important;
}

/* Force the option_menu iframe itself to be transparent */
div.stElementContainer:has(iframe[title*="streamlit_option_menu"]) iframe {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
}
/* Hide the helper components.html iframe container completely */
div.stElementContainer:has(iframe[srcdoc*="makeIframeTransparent"]) {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

    # Use components.html to execute Javascript in the parent DOM (pierces option_menu iframe)
    components.html("""
<script>
const makeIframeTransparent = () => {
    try {
        const parentDoc = window.parent.document;
        const iframes = parentDoc.querySelectorAll('iframe[title*="streamlit_option_menu"]');
        iframes.forEach(iframe => {
            try {
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                if (doc && doc.body) {
                    doc.body.style.setProperty('background', 'transparent', 'important');
                    doc.body.style.setProperty('background-color', 'transparent', 'important');
                    
                    const root = doc.getElementById('root');
                    if (root) {
                        root.style.setProperty('background', 'transparent', 'important');
                        root.style.setProperty('background-color', 'transparent', 'important');
                    }
                    
                    // Inject responsive CSS into iframe head for premium styling
                    let styleTag = doc.getElementById('custom-navbar-iframe-style');
                    if (!styleTag) {
                        styleTag = doc.createElement('style');
                        styleTag.id = 'custom-navbar-iframe-style';
                        styleTag.innerHTML = `
                            .container-fluid {
                                background: rgba(255, 255, 255, 0.03) !important;
                                backdrop-filter: blur(12px) saturate(120%) !important;
                                -webkit-backdrop-filter: blur(12px) saturate(120%) !important;
                                border: 1px solid rgba(255, 255, 255, 0.05) !important;
                                border-radius: 12px !important;
                                padding: 4px 8px !important;
                                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
                                display: flex !important;
                                align-items: center !important;
                                justify-content: center !important;
                                height: 46px !important;
                                box-sizing: border-box !important;
                            }
                            nav, .nav, .navbar, #root > div {
                                background: transparent !important;
                                background-color: transparent !important;
                                display: flex !important;
                                align-items: center !important;
                                justify-content: center !important;
                                width: 100% !important;
                                height: 100% !important;
                                margin: 0 !important;
                                padding: 0 !important;
                            }
                            .nav-link {
                                font-family: 'Inter', sans-serif !important;
                                font-size: 13px !important;
                                font-weight: 600 !important;
                                padding: 4px 10px !important;
                                margin: 0 6px !important;
                                border-radius: 10px !important;
                                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
                                color: #94A3B8 !important;
                                border: 1.5px solid transparent !important;
                                display: inline-flex !important;
                                align-items: center !important;
                                justify-content: center !important;
                                text-align: center !important;
                                height: 34px !important;
                            }
                            .nav-link:hover {
                                color: #ffffff !important;
                                background: rgba(255, 255, 255, 0.05) !important;
                                border-color: rgba(255, 255, 255, 0.1) !important;
                            }
                            .nav-link.active {
                                background: linear-gradient(135deg, #a855f7 0%, #6d28d9 100%) !important;
                                color: #ffffff !important;
                                box-shadow: 0 0 12px rgba(168, 85, 247, 0.3) !important;
                                border-color: rgba(168, 85, 247, 0.2) !important;
                            }
                        `;
                        doc.head.appendChild(styleTag);
                    }
                }
            } catch (e) {
                // Same-origin browser restriction if ports mismatch temporarily
            }
        });
    } catch (e) {
        // Parent access error
    }
};

// Start transparency loop
if (!window.parent.iframeTransparencyInterval) {
    window.parent.iframeTransparencyInterval = setInterval(makeIframeTransparent, 80);
}
</script>
""", height=0)

    selected = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Dashboard",
            "Resume Review",
            "JD Match",
            "Interview",
            "Settings"
        ],
        icons=[
            "house-fill",
            "speedometer2",
            "file-earmark-person-fill",
            "clipboard-data-fill",
            "person-workspace",
            "gear-fill"
        ],
        orientation="horizontal",
        default_index=default_index,
        key=key,
        styles={
            "container": {
                "padding": "4px 8px!important",
                "background-color": "rgba(255, 255, 255, 0.03)!important",
                "backdrop-filter": "blur(12px) saturate(120%)!important",
                "-webkit-backdrop-filter": "blur(12px) saturate(120%)!important",
                "border": "1px solid rgba(255, 255, 255, 0.05)!important",
                "border-radius": "12px!important",
                "box-shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.2)!important",
                "display": "flex!important",
                "align-items": "center!important",
                "justify-content": "center!important",
                "height": "46px!important",
                "box-sizing": "border-box!important",
            },
            "icon": {
                "color": "#a78bfa",
                "font-size": "14px!important",
                "margin-right": "6px!important",
            },
            "nav-link": {
                "font-family": "'Inter', sans-serif!important",
                "font-size": "13px!important",
                "font-weight": "600!important",
                "text-align": "center!important",
                "margin": "0 4px!important",
                "padding": "4px 10px!important",
                "color": "#94a3b8!important",
                "border-radius": "10px!important",
                "display": "inline-flex!important",
                "align-items": "center!important",
                "justify-content": "center!important",
                "text-align": "center!important",
                "height": "34px!important",
                "transition": "all 0.25s ease!important",
                "--hover-color": "rgba(255, 255, 255, 0.05)",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #a855f7 0%, #6d28d9 100%)!important",
                "color": "#ffffff!important",
                "font-weight": "700!important",
                "box-shadow": "0 0 12px rgba(168, 85, 247, 0.3)!important",
                "border": "1.5px solid rgba(168, 85, 247, 0.2)!important",
            },
        }
    )

    return selected

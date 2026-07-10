from streamlit_option_menu import option_menu


def render_navbar():
    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Resume Review",
            "JD Match",
            "Interview",
            "Settings"
        ],
        icons=[
            "house-fill",
            "file-earmark-person-fill",
            "clipboard-data-fill",
            "person-workspace",
            "gear-fill"
        ],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {
                "padding": "8px",
                "background-color": "#111827",
                "border-radius": "15px",
            },
            "icon": {
                "color": "#7C3AED",
                "font-size": "20px",
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "color": "white",
                "--hover-color": "#1F2937",
            },
            "nav-link-selected": {
                "background-color": "#7C3AED",
                "color": "white",
            },
        }
    )

    return selected
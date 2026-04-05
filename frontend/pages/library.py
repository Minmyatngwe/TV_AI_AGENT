import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="TV AI Agent - TV Display", layout="wide")

# ----------------------------
# CONFIG
# ----------------------------
OUTPUT_ROOT = Path("/home/user/persistent/TV_AI_AGENT/backend/output")
TV_PUBLISH_URL = "http://tv-device.local/api/publish"  # placeholder


# ----------------------------
# LOAD CSS
# ----------------------------
def load_css():
    css_path = Path(__file__).resolve().parents[1] / "styles" / "library.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ----------------------------
# HELPERS
# ----------------------------
def format_time(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def find_layout_images(output_root: Path):
    if not output_root.exists():
        return []

    allowed_exts = {".png", ".jpg", ".jpeg", ".webp"}
    items = []

    for image_path in output_root.rglob("*"):
        if image_path.is_file() and image_path.suffix.lower() in allowed_exts:
            parts_lower = [p.lower() for p in image_path.parts]

            if "image" not in parts_lower:
                continue

            try:
                stat = image_path.stat()
                parent_folder = image_path.parent.parent.name if image_path.parent.name == "image" else image_path.parent.name

                items.append(
                    {
                        "name": image_path.stem,
                        "display_name": f"{parent_folder} / {image_path.name}",
                        "path": str(image_path),
                        "project": parent_folder,
                        "modified": stat.st_mtime,
                        "modified_text": format_time(stat.st_mtime),
                    }
                )
            except Exception:
                pass

    items.sort(key=lambda x: x["modified"], reverse=True)
    return items


def load_sample_layouts():
    return [
        {
            "name": "summer_campaign_01",
            "display_name": "summer_campaign / layout_01.png",
            "path": "",
            "project": "summer_campaign",
            "modified": 0,
            "modified_text": "Sample data",
        },
        {
            "name": "tech_event_hero",
            "display_name": "tech_event / hero_slide.png",
            "path": "",
            "project": "tech_event",
            "modified": 0,
            "modified_text": "Sample data",
        },
        {
            "name": "restaurant_promo",
            "display_name": "restaurant_promo / menu_display.png",
            "path": "",
            "project": "restaurant_promo",
            "modified": 0,
            "modified_text": "Sample data",
        },
    ]


def publish_to_tv(layout_item):
    # Replace later with actual TV-side API call
    return True, f"Sample publish success for: {layout_item['display_name']}"


# ----------------------------
# SESSION STATE
# ----------------------------
if "selected_tv_layout" not in st.session_state:
    st.session_state.selected_tv_layout = None

if "last_publish_message" not in st.session_state:
    st.session_state.last_publish_message = ""


# ----------------------------
# LOAD DATA
# ----------------------------
layouts = find_layout_images(OUTPUT_ROOT)
using_sample_data = False

if not layouts:
    layouts = load_sample_layouts()
    using_sample_data = True


# ----------------------------
# HEADER
# ----------------------------
st.markdown('<div class="main-title">TV AI Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Browse generated layouts, preview them in a TV-style view, and publish the selected layout to the display.</div>',
    unsafe_allow_html=True,
)

if using_sample_data:
    st.info("No generated layout history was found, so sample layout data is being shown for the UI preview.")


# ----------------------------
# FILTERS
# ----------------------------
projects = sorted(list({item["project"] for item in layouts}))
left_filter, mid_filter, right_filter = st.columns([2, 2, 1])

with left_filter:
    selected_project = st.selectbox("Filter by project", ["All"] + projects)

with mid_filter:
    search_text = st.text_input("Search layout name", placeholder="Type part of the layout name...")

with right_filter:
    sort_option = st.selectbox("Sort", ["Newest first", "Oldest first", "Project"])

filtered_layouts = layouts

if selected_project != "All":
    filtered_layouts = [x for x in filtered_layouts if x["project"] == selected_project]

if search_text.strip():
    q = search_text.strip().lower()
    filtered_layouts = [
        x for x in filtered_layouts
        if q in x["display_name"].lower() or q in x["name"].lower()
    ]

if sort_option == "Newest first":
    filtered_layouts = sorted(filtered_layouts, key=lambda x: x["modified"], reverse=True)
elif sort_option == "Oldest first":
    filtered_layouts = sorted(filtered_layouts, key=lambda x: x["modified"])
elif sort_option == "Project":
    filtered_layouts = sorted(filtered_layouts, key=lambda x: (x["project"].lower(), x["display_name"].lower()))


# ----------------------------
# MAIN LAYOUT
# ----------------------------
left_col, right_col = st.columns([1.1, 1.9], gap="large")

with left_col:
    st.markdown('<div class="section-title">Layout History</div>', unsafe_allow_html=True)

    if not filtered_layouts:
        st.markdown(
            '<div class="empty-box">No layouts matched your filters.</div>',
            unsafe_allow_html=True,
        )
    else:
        for idx, item in enumerate(filtered_layouts):
            st.markdown('<div class="layout-card">', unsafe_allow_html=True)

            if item["path"] and Path(item["path"]).exists():
                st.image(item["path"], use_container_width=True)
            else:
                st.markdown(
                    """
                    <div class="placeholder-preview">
                        Layout Preview
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(f"**{item['display_name']}**")
            st.markdown(
                f"<div class='meta-text'>Project: {item['project']}<br>Updated: {item['modified_text']}</div>",
                unsafe_allow_html=True,
            )

            if st.button(
                "Select Layout",
                key=f"select_layout_{idx}_{item['display_name']}",
                use_container_width=True,
            ):
                st.session_state.selected_tv_layout = item

            st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    preview_wrapper = st.container()

    with preview_wrapper:
        st.markdown('<div class="tv-preview-marker"></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">TV Preview</div>', unsafe_allow_html=True)

        selected = st.session_state.selected_tv_layout

        if selected is None and filtered_layouts:
            selected = filtered_layouts[0]
            st.session_state.selected_tv_layout = selected

        if selected is None:
            st.markdown(
                '<div class="empty-box">No layout selected yet.</div>',
                unsafe_allow_html=True,
            )
        else:
            top_a, top_b = st.columns([2, 1])

            with top_a:
                st.markdown(f"### {selected['display_name']}")
                st.caption(f"Project: {selected['project']}")

            st.markdown('<div class="tv-frame">', unsafe_allow_html=True)

            if selected["path"] and Path(selected["path"]).exists():
                st.image(selected["path"], use_container_width=True)
            else:
                st.markdown(
                    """
                    <div class="tv-placeholder">
                        TV Fullscreen Preview
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)

            action_col1, action_col2, action_col3 = st.columns([1, 1, 1])

            with action_col1:
                if st.button("Publish to TV", type="primary", use_container_width=True):
                    success, message = publish_to_tv(selected)
                    st.session_state.last_publish_message = message
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

            with action_col2:
                if st.button("Refresh History", use_container_width=True):
                    st.rerun()

            # with st.expander("Selected Layout Details"):
            #     st.write(
            #         {
            #             "layout_name": selected["name"],
            #             "display_name": selected["display_name"],
            #             "project": selected["project"],
            #             "path": selected["path"],
            #             "updated": selected["modified_text"],
            #             "publish_api_placeholder": TV_PUBLISH_URL,
            #         }
            #     )

if st.session_state.last_publish_message:
    st.info(f"Last publish result: {st.session_state.last_publish_message}")
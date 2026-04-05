"""GIX Campus Wayfinder — Streamlit app for new students."""

import streamlit as st

CATEGORIES = [
    "Makerspace",
    "Study Space",
    "Printing",
    "Storage",
    "Food & Drink",
    "Services",
]

resources = [
    {
        "name": "GIX Prototyping Lab",
        "category": "Makerspace",
        "location": "Steve Ballmer Building, Level 2 makerspace bay",
        "hours": "Mon–Fri 8:00 AM–10:00 PM; card access after 6:00 PM",
        "description": "Shared workbenches, hand tools, and basic fabrication gear for "
        "course projects and rapid iteration. Check in with staff on first visit for a "
        "short safety orientation.",
        "free": True,
        "tips": "Book heavy equipment early during sprint weeks; bring your own "
        "eye protection if you prefer a fitted pair.",
    },
    {
        "name": "Electronics & Soldering Bench",
        "category": "Makerspace",
        "location": "Ballmer Building, makerspace — electronics corner",
        "hours": "Same as Prototyping Lab; supervised hours posted on the door",
        "description": "Soldering stations, multimeters, and common components for "
        "IoT and hardware coursework. Consumables like solder and flux are stocked "
        "for class use.",
        "free": True,
        "tips": "Power down boards before measuring; the shared tip tinner saves "
        "frustration if your iron stops wetting.",
    },
    {
        "name": "Reservable Team Rooms",
        "category": "Study Space",
        "location": "Ballmer Building, study wing near the atrium stairs",
        "hours": "Building access hours; rooms released if no check-in after 15 minutes",
        "description": "Small glass rooms with whiteboards and HDMI for team syncs, "
        "user interviews, and quiet calls. Reserve through the campus room system.",
        "free": True,
        "tips": "Grab the corner rooms for less foot traffic; bring a USB-C HDMI "
        "adapter—adapters disappear fast during midterms.",
    },
    {
        "name": "Open Collaboration Lounge",
        "category": "Study Space",
        "location": "Ballmer atrium, soft seating clusters",
        "hours": "Typically 7:00 AM–11:00 PM on class days",
        "description": "Casual seating for ideation, casual critiques, and cross-cohort "
        "meetups. Whiteboard towers are first-come, first-served.",
        "free": True,
        "tips": "Great for quick stand-ups; avoid confidential sponsor work here "
        "without headphones.",
    },
    {
        "name": "Large-Format Poster Printer",
        "category": "Printing",
        "location": "Ballmer Building, print hub (signage near student services)",
        "hours": "Staff-assisted prints Mon–Fri 9:00 AM–5:00 PM",
        "description": "Plotter-style printing for demo posters and showcase events. "
        "Submit PDFs at the correct dimensions; ICC profiles are linked on the wiki.",
        "free": False,
        "tips": "Proof at 100% zoom before submitting; rush jobs during showcase "
        "week cost extra and queue fast.",
    },
    {
        "name": "Multi-Function Print & Scan Station",
        "category": "Printing",
        "location": "Ballmer Level 1, across from the main elevators",
        "hours": "24/7 with GIX badge during active quarters",
        "description": "Color and black-and-white printing, duplex, and high-speed "
        "scan to email. Quotas reset each term.",
        "free": True,
        "tips": "Use scan-to-PDF for sponsor NDAs instead of leaving paper in the tray; "
        "double-sided saves quota on long readings.",
    },
    {
        "name": "Graduate Day Lockers",
        "category": "Storage",
        "location": "Ballmer basement corridor, locker bank B",
        "hours": "Combination issued per academic year; cleared over summer break",
        "description": "Personal lockers for laptops, prototypes, and gym gear. "
        "Assignment forms are at the welcome desk.",
        "free": True,
        "tips": "Label the inside of your door with contact info; combo locks are "
        "reset between tenants.",
    },
    {
        "name": "Short-Term Project Cubbies",
        "category": "Storage",
        "location": "Makerspace perimeter shelving",
        "hours": "Tagged storage reviewed weekly; unlabeled items go to lost-and-found",
        "description": "Temporary labeled storage for in-progress physical prototypes "
        "between work sessions. Not for long-term personal storage.",
        "free": True,
        "tips": "Use neon tape and a cohort-wide naming scheme so teams stop "
        "mistaking your chassis for scrap.",
    },
    {
        "name": "GIX Grounds Espresso Bar",
        "category": "Food & Drink",
        "location": "Ballmer atrium café counter",
        "hours": "Mon–Fri 7:30 AM–4:00 PM (hours shorten during breaks)",
        "description": "Espresso drinks, pastries, and light snacks. Accepts Husky Card "
        "and major cards.",
        "free": False,
        "tips": "The morning rush hits right before studio; order ahead if the app is "
        "enabled that quarter.",
    },
    {
        "name": "Student Kitchenette & Microwaves",
        "category": "Food & Drink",
        "location": "Ballmer Level 1, near the east stairwell",
        "hours": "Building hours; cleaned nightly",
        "description": "Microwaves, hot water, and fridge space for labeled items. "
        "Dish soap and towels are provided—please wipe surfaces.",
        "free": True,
        "tips": "Friday afternoons the fridge gets purged; use a Sharpie date on "
        "anything you care about.",
    },
    {
        "name": "Welcome Desk & Mail Hold",
        "category": "Services",
        "location": "Ballmer main lobby",
        "hours": "Mon–Fri 8:30 AM–5:00 PM",
        "description": "Badge issues, package pickup, guest check-in, and general "
        "campus questions. Official mail and small parcels are held here.",
        "free": True,
        "tips": "Use your legal name on Amazon orders; couriers reject fuzzy "
        "nicknames and delay pickup.",
    },
    {
        "name": "IT & AV Support Window",
        "category": "Services",
        "location": "Ballmer Level 1, adjacent to the large classroom",
        "hours": "Walk-in Mon–Thu 10:00 AM–4:00 PM; ticket system after hours",
        "description": "Laptop imaging, Wi-Fi troubleshooting, HDMI kits, and "
        "microphone checks for presentations. Loaner laptops subject to availability.",
        "free": True,
        "tips": "Before demo day, test your adapter in the actual room—HDCP and "
        "resolution surprises are common.",
    },
]

assert all("name" in r and "category" in r and "location" in r
           for r in resources), "Data integrity check failed: missing required fields"

st.set_page_config(page_title="GIX Campus Wayfinder", layout="wide")

st.title("GIX Campus Wayfinder")
st.caption("Find makerspace gear, study spots, printing, storage, food, and services on campus.")

st.header("Filters")

search_query = st.text_input(
    "Search",
    placeholder="Filter by name or description…",
    help="Matches anywhere in the resource name or description.",
)
selected_categories = st.multiselect(
    "Categories",
    options=CATEGORIES,
    default=CATEGORIES,
    help="Show resources in any of the selected categories.",
)
free_only = st.checkbox("Show only free resources", value=False)

# Real-time filtering: Streamlit reruns on each widget change.
q = search_query.strip().lower()
filtered = []
for r in resources:
    if q and q not in r["name"].lower() and q not in r["description"].lower():
        continue
    if not selected_categories or r["category"] not in selected_categories:
        continue
    if free_only and not r["free"]:
        continue
    filtered.append(r)

st.header("Results")
count = len(filtered)
st.metric("Matching resources", count)

if count == 0:
    st.info(
        "No resources match your filters. Try clearing the search text, selecting "
        "more categories in the multiselect, or unchecking “Show only free resources.”"
    )
else:
    for r in filtered:
        with st.expander(r["name"], expanded=False):
            st.subheader(r["name"])
            st.write(f"**Category:** {r['category']}")
            st.write(f"**Location:** {r['location']}")
            st.write(f"**Hours:** {r['hours']}")
            st.write(f"**Description:** {r['description']}")
            st.write(f"**Free to use:** {'Yes' if r['free'] else 'No'}")
            st.write(f"**Tips:** {r['tips']}")

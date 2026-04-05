# GIX Purchase Request Tracker — built with Streamlit for TECHIN 510 Week 1.
# This app lets GIX students submit purchase requests and lets coordinator Dorothy
# view, filter, and update order status, which replaces the current Google Form + Excel workflow.
# I manually replaced st.markdown("### Navigation") with st.subheader("Navigation")
# to fix semantic heading structure.

"""GIX Purchase Request Tracker — student submissions and coordinator overview."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

CSV_PATH = Path(__file__).resolve().parent / "requests.csv"

# About page — set your name for the assignment / portfolio.
DEVELOPER_NAME = "Your Name"
DEVELOPER_COURSE = "TECHIN 510 · University of Washington Global Innovation Exchange (GIX)"

COLUMNS = [
    "id",
    "submitted_at",
    "student_name",
    "class_name",
    "team_number",
    "supplier",
    "item_name",
    "quantity",
    "unit_price",
    "product_link",
    "notes",
    "instructor_approval",
    "status",
]

SUPPLIER_OPTIONS = ["Amazon", "non-Amazon"]
APPROVAL_OPTIONS = ["Approved", "Pending"]
STATUS_OPTIONS = ["Pending", "Ordered", "Delivered", "Back-ordered", "Returned"]


def load_requests() -> pd.DataFrame:
    if not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0:
        return pd.DataFrame(columns=COLUMNS)
    df = pd.read_csv(CSV_PATH)
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    out = df.reindex(columns=COLUMNS)
    out["status"] = out["status"].fillna("Pending")
    return out


def save_requests(df: pd.DataFrame) -> None:
    df = df.reindex(columns=COLUMNS)
    df.to_csv(CSV_PATH, index=False)


def next_request_id(df: pd.DataFrame) -> int:
    if df.empty or "id" not in df.columns:
        return 1
    ids = pd.to_numeric(df["id"], errors="coerce").dropna()
    return int(ids.max()) + 1 if len(ids) else 1


def estimated_line_cost(row) -> float:
    try:
        q = float(row["quantity"])
        p = float(row["unit_price"])
        return q * p
    except (TypeError, ValueError):
        return 0.0


def page_submit_request() -> None:
    st.header("Submit a Request")
    st.caption("Fill in the details below. Your request will be saved for the coordinator.")

    with st.form("purchase_request_form", clear_on_submit=False):
        student_name = st.text_input("Your name", placeholder="e.g., Alex Kim")
        class_name = st.text_input("Class name", placeholder="e.g., L510 Prototyping")
        team_number = st.text_input("Team number (optional)", placeholder="e.g., 4")
        supplier = st.selectbox("Supplier", SUPPLIER_OPTIONS, index=0)
        item_name = st.text_input("Item name", placeholder="Short description of the item")
        c1, c2 = st.columns(2)
        with c1:
            quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
        with c2:
            unit_price = st.number_input("Unit price (USD)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        product_link = st.text_input("Product link", placeholder="https://...")
        notes = st.text_area("Notes (optional)", placeholder="Any extra context for Dorothy")
        instructor_approval = st.radio(
            "Instructor approval status",
            APPROVAL_OPTIONS,
            horizontal=True,
            index=1,
        )
        submitted = st.form_submit_button("Submit request", type="primary")

    if not submitted:
        return

    if not (student_name or "").strip():
        st.error("Please enter your name.")
        return
    if not (class_name or "").strip():
        st.error("Please enter your class name.")
        return
    if not (item_name or "").strip():
        st.error("Please enter the item name.")
        return
    if not (product_link or "").strip():
        st.error("Please enter a product link.")
        return

    df = load_requests()
    new_id = next_request_id(df)
    row = {
        "id": new_id,
        "submitted_at": datetime.now().isoformat(timespec="seconds"),
        "student_name": student_name.strip(),
        "class_name": class_name.strip(),
        "team_number": (team_number or "").strip(),
        "supplier": supplier,
        "item_name": item_name.strip(),
        "quantity": int(quantity),
        "unit_price": float(unit_price),
        "product_link": product_link.strip(),
        "notes": (notes or "").strip(),
        "instructor_approval": instructor_approval,
        "status": "Pending",
    }
    save_requests(pd.concat([df, pd.DataFrame([row])], ignore_index=True))
    st.success("Request submitted. Thank you — Dorothy can review it under **View All Requests**.")


def page_view_requests() -> None:
    st.header("View All Requests")
    df = load_requests()

    if df.empty:
        st.info("No requests yet. When students submit entries from **Submit a Request**, they will appear here.")
        return

    df = df.copy()
    df["_cost"] = df.apply(estimated_line_cost, axis=1)
    total_cost = float(df["_cost"].sum())

    st.subheader("Summary")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total requests", len(df))
    m2.metric("Total estimated cost", f"${total_cost:,.2f}")
    pending_coord = int((df["status"] == "Pending").sum())
    m3.metric("Fulfillment: still pending", pending_coord)

    st.divider()

    search_query = st.text_input(
        "Search requests",
        placeholder="Type to filter by student, item, or class…",
        key="view_search",
        help="Matches any part of student name, item name, or class name (not case-sensitive).",
    )
    q = (search_query or "").strip().lower()
    if q:
        sn = df["student_name"].fillna("").astype(str).str.lower()
        it = df["item_name"].fillna("").astype(str).str.lower()
        cl = df["class_name"].fillna("").astype(str).str.lower()
        search_mask = sn.str.contains(q, regex=False) | it.str.contains(q, regex=False) | cl.str.contains(q, regex=False)
        after_search = df[search_mask].copy()
    else:
        after_search = df

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        supplier_filter = st.multiselect(
            "Filter by supplier",
            options=SUPPLIER_OPTIONS,
            default=SUPPLIER_OPTIONS,
        )
    with col_f2:
        approval_filter = st.multiselect(
            "Filter by instructor approval",
            options=APPROVAL_OPTIONS,
            default=APPROVAL_OPTIONS,
        )

    view = after_search[
        after_search["supplier"].isin(supplier_filter) & after_search["instructor_approval"].isin(approval_filter)
    ].copy()
    filtered_cost = float(view["_cost"].sum()) if not view.empty else 0.0
    st.caption(f"Showing **{len(view)}** request(s) · Filtered estimated cost: **${filtered_cost:,.2f}**")

    if view.empty:
        st.warning("No rows match your search or filters. Try different text or filter choices.")
        return

    display_cols = [
        "id",
        "submitted_at",
        "student_name",
        "class_name",
        "team_number",
        "supplier",
        "item_name",
        "quantity",
        "unit_price",
        "product_link",
        "notes",
        "instructor_approval",
        "status",
    ]
    show = view[display_cols].copy()
    show["est_line_total"] = view["_cost"].map(lambda x: f"${x:,.2f}")

    st.subheader("Requests")
    st.dataframe(
        show,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", format="%d"),
            "product_link": st.column_config.LinkColumn("Product link"),
            "quantity": st.column_config.NumberColumn("Qty", format="%d"),
            "unit_price": st.column_config.NumberColumn("Unit $", format="$%.2f"),
            "est_line_total": st.column_config.TextColumn("Est. line total"),
        },
    )

    st.divider()
    st.subheader("Update fulfillment status (coordinator)")
    st.caption("Choose **status** for each row, then click **Save status changes** to update `requests.csv`.")

    rid_to_status: dict[int, str] = {}
    header = st.columns([0.7, 2.2, 2.5, 2.2])
    header[0].markdown("**ID**")
    header[1].markdown("**Student**")
    header[2].markdown("**Item**")
    header[3].markdown("**Status**")

    view_sorted = view.sort_values("id", kind="stable")
    for _, row in view_sorted.iterrows():
        rid = int(row["id"])
        cols = st.columns([0.7, 2.2, 2.5, 2.2])
        cols[0].write(rid)
        cols[1].write(row["student_name"])
        cols[2].write(row["item_name"])
        cur = str(row["status"]) if pd.notna(row["status"]) else "Pending"
        if cur not in STATUS_OPTIONS:
            cur = "Pending"
        status_idx = STATUS_OPTIONS.index(cur)
        rid_to_status[rid] = cols[3].selectbox(
            "Status",
            options=STATUS_OPTIONS,
            index=status_idx,
            key=f"coord_status_{rid}",
            label_visibility="collapsed",
        )

    if st.button("Save status changes", type="primary"):
        full = load_requests()
        full["id"] = pd.to_numeric(full["id"], errors="coerce").astype("Int64")
        for rid, new_status in rid_to_status.items():
            mask = full["id"] == rid
            if mask.any() and new_status in STATUS_OPTIONS:
                full.loc[mask, "status"] = new_status
        save_requests(full)
        st.success("Saved.")
        st.rerun()


def page_about() -> None:
    st.header("About This App")
    st.markdown(
        """
        This app was built for **TECHIN 510** to help **GIX students** submit purchase requests
        and to help coordinator **Dorothy** track and manage orders in one place. It is intended
        to replace the current **Google Form and Excel** workflow with a single Streamlit tool.
        """
    )
    st.markdown(
        f"- **GIX website:** [gix.uw.edu](https://www.gix.uw.edu)\n"
        f"- **Developer:** Xin Luo\n"
        f"- **Course:** {DEVELOPER_COURSE}"
    )


def main() -> None:
    st.set_page_config(
        page_title="GIX Purchase Request Tracker",
        page_icon="📦",
        layout="wide",
    )
    st.title("GIX Purchase Request Tracker")
    st.caption("Students: fill in your request below. Coordinator: switch to View All Requests to manage orders.")

    with st.sidebar:
        st.subheader("Navigation")
        page = st.radio(
            "Section",
            ["Submit a Request", "View All Requests", "About"],
            label_visibility="collapsed",
        )

    if page == "Submit a Request":
        page_submit_request()
    elif page == "View All Requests":
        page_view_requests()
    else:
        page_about()


if __name__ == "__main__":
    main()

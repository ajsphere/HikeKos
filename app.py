
import os

import pandas as pd
import streamlit as st
from supabase import create_client


st.set_page_config(
    page_title="HikeKos | Zbulo Kosovën",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7f2;
    }

    h1, h2, h3 {
        color: #183b2b;
    }

    .hero {
        padding: 30px;
        border-radius: 18px;
        background: linear-gradient(120deg, #163d2b, #427a51);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 42px;
    }

    .hero p {
        color: #edf5ec;
        font-size: 18px;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e0e8de;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


SAMPLE_TRAILS = [
    {
        "name": "Maja e Hajlës",
        "location": "Rugovë",
        "difficulty": "E vështirë",
        "distance_km": 12.0,
        "duration_hours": 7.0,
        "elevation_m": 2403,
        "latitude": 42.68,
        "longitude": 20.08,
        "description": "Një destinacion malor për ecës me përvojë.",
    },
    {
        "name": "Gjeravica",
        "location": "Bjeshkët e Nemuna",
        "difficulty": "E vështirë",
        "distance_km": 15.0,
        "duration_hours": 8.0,
        "elevation_m": 2656,
        "latitude": 42.53,
        "longitude": 20.14,
        "description": "Një nga destinacionet më të njohura alpine në Kosovë.",
    },
    {
    "name": "Maja e Korabit",
    "location": "Kufiri Kosovë–Maqedoni e Veriut",
    "difficulty": "E vështirë",
    "distance_km": 18.0,
    "duration_hours": 8.0,
    "elevation_m": 2764,
    "latitude": 41.79,
    "longitude": 20.55,
    "description": "Ngjitje malore drejt majës më të lartë të Maqedonisë së Veriut, me pamje panoramike të bjeshkëve përreth."
},
{
    "name": "Maja e Vërtopit",
    "location": "Malet e Sharrit",
    "difficulty": "E vështirë",
    "distance_km": 15.0,
    "duration_hours": 6.5,
    "elevation_m": 2555,
    "latitude": 42.08,
    "longitude": 20.85,
    "description": "Destinacion malor për ecës me përvojë, me peizazhe dhe pamje të bukura malore."
},
    {
        "name": "Maja e Lubotenit",
        "location": "Malet e Sharrit",
        "difficulty": "E vështirë",
        "distance_km": 10.0,
        "duration_hours": 6.0,
        "elevation_m": 2498,
        "latitude": 42.20,
        "longitude": 21.12,
        "description": "Ecje malore me pamje të bukura të Sharrit.",
    },
    {
        "name": "Maja e Pashtrikut",
        "location": "Pashtrik",
        "difficulty": "E vështirë",
        "distance_km": 12.0,
        "duration_hours": 6.0,
        "elevation_m": 1986,
        "latitude": 42.08,
        "longitude": 20.55,
        "description": "Eksploro terrenin malor dhe peizazhet e Pashtrikut.",
    },
    {
        "name": "Maja e Oshlakut",
        "location": "Malet e Sharrit",
        "difficulty": "E vështirë",
        "distance_km": 9.0,
        "duration_hours": 5.0,
        "elevation_m": 2212,
        "latitude": 42.18,
        "longitude": 20.99,
        "description": "Një destinacion malor për ecësit me përvojë.",
    },
    {
        "name": "Guri i Kuq",
        "location": "Rugovë",
        "difficulty": "Mesatare",
        "distance_km": 8.0,
        "duration_hours": 4.0,
        "elevation_m": 2522,
        "latitude": 42.70,
        "longitude": 20.05,
        "description": "Terren malor me pamje panoramike.",
    },
    {
        "name": "Maja e Strellcit",
        "location": "Deçan",
        "difficulty": "E vështirë",
        "distance_km": 10.0,
        "duration_hours": 6.0,
        "elevation_m": 2377,
        "latitude": 42.58,
        "longitude": 20.30,
        "description": "Ecje në zonën malore të Deçanit.",
    },
    {
        "name": "Liqeni i Jazhincës",
        "location": "Malet e Sharrit",
        "difficulty": "E vështirë",
        "distance_km": 12.0,
        "duration_hours": 7.0,
        "elevation_m": 2180,
        "latitude": 42.17,
        "longitude": 20.82,
        "description": "Ecje malore drejt një liqeni akullnajor.",
    },
]


@st.cache_resource
def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        return None

    return create_client(url, key)


def load_trails():
    client = get_supabase_client()

    if client is None:
        return pd.DataFrame(SAMPLE_TRAILS), True

    try:
        response = client.table("trails").select("*").execute()

        if response.data:
            return pd.DataFrame(response.data), False

        return pd.DataFrame(SAMPLE_TRAILS), True

    except Exception:
        st.warning(
            "Databaza nuk mund të lexohej. "
            "Po shfaqen të dhënat testuese."
        )
        return pd.DataFrame(SAMPLE_TRAILS), True


st.sidebar.title("⛰️ HikeKos")
st.sidebar.caption("Zbulo shtigjet e Kosovës")

page = st.sidebar.radio(
    "Navigimi",
    [
        "Ballina",
        "Eksploro shtigjet",
        "Harta",
        "Rreth projektit",
    ],
)

st.sidebar.divider()
st.sidebar.info(
    "Platformë për eksploruesit e natyrës dhe aventurave malore."
)

trails, using_sample_data = load_trails()

if using_sample_data:
    st.sidebar.caption("ℹ️ Modaliteti testues: të dhëna shembull")


if page == "Ballina":
    st.markdown(
        """
        <div class="hero">
            <h1>HikeKos ⛰️</h1>
            <p>
                Gjej shtigje të bukura dhe planifiko ecjen tënde në mal.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Shtigje në katalog", len(trails))

    with col2:
        locations = (
            trails["location"].nunique()
            if "location" in trails.columns
            else 0
        )
        st.metric("Lokacione", locations)

    with col3:
        difficulties = (
            trails["difficulty"].nunique()
            if "difficulty" in trails.columns
            else 0
        )
        st.metric("Nivele vështirësie", difficulties)

    st.subheader("Shtigjet e rekomanduara")

    for start in range(0, len(trails), 2):
        columns = st.columns(2)

        for column, index in zip(
            columns,
            range(start, min(start + 2, len(trails))),
        ):
            trail = trails.iloc[index]

            with column:
                with st.container(border=True):
                    st.subheader(trail["name"])
                    st.caption(f"📍 {trail['location']}")
                    st.write(
                        trail.get(
                            "description",
                            "Eksploro këtë destinacion malor.",
                        )
                    )
                    st.write(f"**Vështirësia:** {trail['difficulty']}")
                    st.write(f"**Distanca:** {trail['distance_km']} km")
                    st.write(
                        f"**Kohëzgjatja:** {trail['duration_hours']} orë"
                    )


elif page == "Eksploro shtigjet":
    st.title("🔎 Eksploro shtigjet")

    search = st.text_input(
        "Kërko sipas emrit ose lokacionit",
        placeholder="P.sh. Rugovë...",
    )

    difficulty_options = [
        "Të gjitha",
        *sorted(trails["difficulty"].dropna().unique()),
    ]

    difficulty = st.selectbox(
        "Niveli i vështirësisë",
        difficulty_options,
    )

    filtered = trails.copy()

    if search:
        mask = (
            filtered["name"].astype(str).str.contains(
                search, case=False, na=False
            )
            | filtered["location"].astype(str).str.contains(
                search, case=False, na=False
            )
        )
        filtered = filtered[mask]

    if difficulty != "Të gjitha":
        filtered = filtered[filtered["difficulty"] == difficulty]

    st.write(f"U gjetën **{len(filtered)}** shtigje.")

    if filtered.empty:
        st.info("Nuk u gjet asnjë shteg.")
    else:
        display_columns = [
            column
            for column in [
                "name",
                "location",
                "difficulty",
                "distance_km",
                "duration_hours",
                "elevation_m",
            ]
            if column in filtered.columns
        ]

        st.dataframe(
            filtered[display_columns],
            use_container_width=True,
            hide_index=True,
        )


elif page == "Harta":
    st.title("🗺️ Harta e shtigjeve")
    st.write("Shiko lokacionet e shtigjeve në hartë.")

    if not trails.empty:
        map_data = trails[["latitude", "longitude"]].copy()

        map_data = map_data.rename(
            columns={
                "latitude": "lat",
                "longitude": "lon",
            }
        ).dropna()

        if not map_data.empty:
            st.map(
                map_data,
                latitude="lat",
                longitude="lon",
                size=100,
            )
        else:
            st.info("Nuk ka koordinata për t'u shfaqur.")

        st.caption(
            "Koordinatat janë orientuese. Kontrollo itinerarin "
            "dhe kushtet lokale para çdo ecjeje."
        )






elif page == "Rreth projektit":
    st.title("Rreth HikeKos")


st.write(
    """
    HikeKos sjell në një vend shtigjet malore dhe destinacionet
    natyrore të Kosovës. Platforma të ndihmon të gjesh shtigje,
    të informohesh për distancën dhe vështirësinë e tyre, si dhe
    të shohësh lokacionet në hartë për ta planifikuar më lehtë
    ecjen tënde.
    """
)

st.subheader("Eksploro shtigjet e Kosovës")

st.write(
    """
    Zbulo vende të reja, shijo natyrën dhe gjej destinacionin
    tënd të radhës për ecje malore.
    """
)

st.success("HikeKos — Zbulo shtigje, përjeto natyrën.")

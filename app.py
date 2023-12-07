import streamlit as st

st.set_page_config(page_title="steamlit" ,page_icon=":smiley:" ,layout="wide" ,initial_sidebar_state="expanded")

st.subheader("Speed")
st.title("E")
st.write("Object speed comparison")
# //bulet points
st.markdown("""<ul>
<li>OOM 0: about <b>1 m/s or 3 km/h</b> - Walking speed.</li>
<li>OOM 1: about <b>10 m/s or 30 km/h</b> - A fast runner or a slow-moving car.</li>
<li>OOM 2: about <b>100 m/s or 300 km/h or Mach 0.3</b> - High-speed trains or race cars.</li>
<li>OOM 3: about <b>1 km/s or 3,000 km/h or Mach 3</b> - Some military jets.</li>
<li>OOM 4: about <b>10 km/s or 30,000 km/h or Mach 30</b> - Earth's escape velocity, or some space probes like New Horizons.</li>
<li>OOM 5: about <b>100 km/s 0.03pc</b> - Solar wind particles </li>
<li>OOM 6: about <b>1,000 km/s 0.3pc</b> - Very high-energy cosmic rays or certain astrophysical jets.</li>
<li>OOM 7: about <b>10,000 km/s 3pc</b> - Speeds inside the core of a supernova explosion.</li>
<li>OOM 8: about <b>100,000 km/s 30pc</b> - Not commonly achieved by known objects; approaching a significant fraction of the speed of light.</li>
</ul>
            """, unsafe_allow_html=True)
# fastest man made object is the probe that was sent to space in 1977 and is still traveling at 17.1 km/s (61,560 km/h; 38,290 mph) relative to the Sun.


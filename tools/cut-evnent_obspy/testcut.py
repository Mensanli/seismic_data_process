from obspy.core import UTCDateTime
from obspy import read

cut_time = UTCDateTime("2022-10-20T07:45:46")
st = read("./BHZ.D/YQ.AG.00.BHZ.D.2022.293.050724.SAC")
st_cut = st.slice(cut_time, cut_time + 30)
st.plot()
st_cut.plot()

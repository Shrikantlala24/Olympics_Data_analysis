import streamlit as st

st.text('Fixed width text')
st.markdown('_Markdown_') # see #*




st.caption('Balloons. Hundreds of them...')
st.latex(r''' e^{i\pi} + 1 = \sin^2 \theta + \cos^2 \theta ''')

st.write('Most objects') # df, err, func, keras!
st.write(['st', 'is <', 3]) # see *
st.title('My title')
st.header('My header')
st.subheader('My sub')
st.code('for i in range(8): foo()')

# * optional kwarg unsafe_allow_html = True

import time

with st.spinner(text='Wait for 3sec', show_time=True):
    time.sleep(3)
    st.success('Done')


# Insert containers separated into tabs:
tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")

# You can also use "with" notation:
with tab1:
  st.radio('Select one:', [1, 2])

  st.markdown("Check out the [Streamlit Documentation](https://docs.streamlit.io/)")

# Alternatively, using st.write
url = "https://www.example.org"
st.write("Visit our [website](%s)" % url)
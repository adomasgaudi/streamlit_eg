import streamlit as st 
current_photo_num = 0

def create_photo(circuit):
    global current_photo_num
    file_name = f"photos/circuitf_{current_photo_num}.png"
    
    figure = circuit.draw("mpl")
    figure.savefig(file_name)
    st.image(file_name)

    current_photo_num += 1
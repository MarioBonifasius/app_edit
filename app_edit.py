# Sistem Persamaan Linear
# Eliminasi Gauss 

# Komputasi Numerik Kemlompok 6

# Mario Bonifasius Dikarta Baha Tolok
# Ahmad Zeda Rajhi
# Florence Agnes
import streamlit as st
import numpy as np
import re

# Fungsi untuk melakukan eliminasi Gauss dengan pengecekan solusi
def gauss_elimination_with_check(A, b):
    n = len(b)

    # Membuat matriks augmented
    augmented_matrix = np.hstack((A, b.reshape(-1, 1)))
    
    # Eliminasi Gauss
    for i in range(n):

        # Pivoting
        max_row = np.argmax(np.abs(augmented_matrix[i:, i])) + i
        augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]
        
        # Jika elemen diagonal utama adalah nol setelah pivoting, maka tidak ada solusi
        if np.isclose(augmented_matrix[i, i], 0):
            return "Sistem tidak memiliki solusi"
        
        # Eliminasi ke bawah
        for j in range(i + 1, n):
            ratio = augmented_matrix[j, i] / augmented_matrix[i, i]
            augmented_matrix[j, i:] -= ratio * augmented_matrix[i, i:]
    
    # Substitusi balik
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        if np.isclose(augmented_matrix[i, i], 0):
            return "Sistem tidak memiliki solusi"
        x[i] = (augmented_matrix[i, -1] - np.dot(augmented_matrix[i, i + 1:n], x[i + 1:])) / augmented_matrix[i, i]
    
    return x

# Fungsi untuk memparsing persamaan dari teks menjadi bentuk matriks
def parse_equations(equations):
    variable_set = set()
    A = []
    b = []
    for eq in equations.split('\n'):
        eq = eq.replace(' ', '').replace('-', ' -').replace('+', ' +')
        lhs, rhs = eq.split('=')
        rhs = float(rhs)
        b.append(rhs)
        
        # Menemukan variabel dan koefisiennya
        terms = re.findall(r'([+-]?\d*\.?\d*[a-z])', lhs)
        coefficients = {}
        for term in terms:
            match = re.match(r'([+-]?\d*\.?\d*)([a-z])', term)
            if match:
                coefficient = match.group(1)
                variable = match.group(2)
                variable_set.add(variable)
                if coefficient in ['+', '']:
                    coefficient = '1'
                elif coefficient == '-':
                    coefficient = '-1'
                coefficients[variable] = float(coefficient)
        
        A.append(coefficients)
    
    variables = sorted(list(variable_set))
    A_matrix = []
    for coef_dict in A:
        row = [coef_dict.get(var, 0) for var in variables]
        A_matrix.append(row)
    
    return np.array(A_matrix), np.array(b), variables

# Membuat tampilan Streamlit
st.title("SPL - Metode Gauss")
st.subheader("Masukkan persamaan linear dalam bentuk 'x + y + z = C'.")

# Input untuk persamaan
equations_input = st.text_area("Masukkan persamaan linear (pisahkan persamaan dengan enter)", "4x -3y +10z = 6\n3x -2y +7z = 3\n2x -y +5z = 4")

# Tombol untuk menghitung
if st.button("Hitung Solusi"):

    # Mengambil Koefisien dari tiap Variavel
    A, b, variables = parse_equations(equations_input)
    
    if len(A) != len(variables):

        # Mengecek jumlah variabel sesuai dengan jumlah persamaan
        st.write(f"Jumlah persamaan tidak sesuai dengan jumlah variabel. Anda memiliki {len(variables)} variabel: {', '.join(variables)} dan {len(A)} persamaan.")
    else:
        # Psoses Eliminasi
        solusi = gauss_elimination_with_check(A, b)
        st.write("Solusi dari sistem persamaan adalah:")
        for i, val in enumerate(solusi):
            st.write(f"{variables[i]} = {val}")


st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px 0;'>
        <small>-- Komputasi Numerik Kelompok 6 (Mario, Zeda, Florence)--<br>by : @zaid.rajhi.01 | 24 - 06 - 2024</small>
    </div>
    """, unsafe_allow_html=True)

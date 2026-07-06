///////////////import streamlit as st/
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Polynomial Grapher", page_icon="📈", layout="centered")

# ----------------------------
# Session state setup
# ----------------------------
if "terms" not in st.session_state:
    st.session_state.terms = []          # list of dicts: {"sign": 1 or -1, "coeff": float, "power": int}
if "selected_power" not in st.session_state:
    st.session_state.selected_power = None

st.title("📈 Interactive Polynomial Grapher")
st.write(
    "Build a polynomial term-by-term using the buttons below, then click **Graph It** "
    "to see the plot. Example: `8x³ + 6x² + 3`"
)

# ----------------------------
# STEP 1: Pick the power (x^n) for the next term
# ----------------------------
st.subheader("Step 1 — Pick a power of x")

MAX_POWER = 8
cols = st.columns(MAX_POWER + 1)  # +1 for constant
for i, col in enumerate(cols):
    power = MAX_POWER - i
    label = f"x^{power}" if power > 1 else ("x" if power == 1 else "const")
    if col.button(label, key=f"power_btn_{power}"):
        st.session_state.selected_power = power

if st.session_state.selected_power is not None:
    p = st.session_state.selected_power
    st.info(f"Selected power: {'constant' if p == 0 else f'x^{p}' if p > 1 else 'x'}")

    # ----------------------------
    # STEP 2: Sign + coefficient, then add the term
    # ----------------------------
    st.subheader("Step 2 — Set sign & coefficient, then add the term")

    c1, c2, c3 = st.columns([1, 1, 1])
    sign = c1.radio("Sign", ["+", "−"], horizontal=True, key="sign_choice")
    coeff = c2.number_input("Coefficient", min_value=0.0, value=1.0, step=1.0, key="coeff_input")

    if c3.button("➕ Add Term"):
        st.session_state.terms.append({
            "sign": 1 if sign == "+" else -1,
            "coeff": coeff,
            "power": p
        })
        st.session_state.selected_power = None
        st.rerun()

st.divider()

# ----------------------------
# Current equation display
# ----------------------------
st.subheader("Your equation so far")

def format_equation(terms):
    if not terms:
        return "(empty — add some terms above)"
    parts = []
    for i, t in enumerate(terms):
        sign_str = "-" if t["sign"] < 0 else ("" if i == 0 else "+")
        coeff = t["coeff"]
        power = t["power"]
        if power == 0:
            term_str = f"{coeff:g}"
        elif power == 1:
            term_str = f"{coeff:g}x" if coeff != 1 else "x"
        else:
            term_str = f"{coeff:g}x^{power}" if coeff != 1 else f"x^{power}"
        parts.append(f"{sign_str}{term_str}")
    eq = " ".join(parts)
    eq = eq.replace("+ -", "- ")
    return eq

equation_str = format_equation(st.session_state.terms)
st.code(f"f(x) = {equation_str}", language=None)

# Let user remove individual terms
if st.session_state.terms:
    remove_idx = st.selectbox(
        "Remove a term (optional)",
        options=list(range(len(st.session_state.terms))),
        format_func=lambda i: format_equation([st.session_state.terms[i]]),
    )
    rc1, rc2 = st.columns(2)
    if rc1.button("🗑️ Remove selected term"):
        st.session_state.terms.pop(remove_idx)
        st.rerun()
    if rc2.button("🧹 Clear all terms"):
        st.session_state.terms = []
        st.rerun()

st.divider()

# ----------------------------
# STEP 3: Graph range + Graph button
# ----------------------------
st.subheader("Step 3 — Graph it")

r1, r2 = st.columns(2)
x_min = r1.number_input("x min", value=-10.0)
x_max = r2.number_input("x max", value=10.0)

if st.button("📊 Graph It", type="primary", disabled=(len(st.session_state.terms) == 0)):
    x = np.linspace(x_min, x_max, 500)
    y = np.zeros_like(x)
    for t in st.session_state.terms:
        y += t["sign"] * t["coeff"] * (x ** t["power"])

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(x, y, linewidth=2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(f"f(x) = {equation_str}")
    st.pyplot(fig)

st.caption("Built with Streamlit, NumPy, and Matplotlib.")***

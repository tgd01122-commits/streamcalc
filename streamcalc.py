import math
import re

import streamlit as st

st.set_page_config(page_title="Simple Calc", page_icon="🧮", layout="centered")

# 계산에 허용할 함수들 (sin/cos/tan은 degree 단위, 원본과 동일)
SAFE_NAMES = {
    "__builtins__": {},
    "pi": math.pi,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "sqrt": math.sqrt,
    "root": lambda n, x: x ** (1 / n),  # n제곱근: root(n,x)
    "abs": abs,
}

# (표시 글자, 입력될 값)
ROWS = [
    [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("π", "π"), ("abs", "abs("), ("ⁿ√", "root(")],
    [("√", "√("), ("x²", "^2"), ("xⁿ", "^"), ("(", "("), (")", ")"), (",", ",")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"), ("DEL", None), ("C", None)],
    [("4", "4"), ("5", "5"), ("6", "6"), ("×", "*")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("−", "-")],
    [("0", "0"), (".", "."), ("=", None), ("+", "+")],
]


def calculate(expr):
    try:
        expr = expr.replace("π", "pi").replace("^", "**").replace("√", "sqrt")
        expr = re.sub(r"(\d|\))(pi|\(|sin|cos|tan|sqrt|root|abs)", r"\1*\2", expr)
        open_b, close_b = expr.count("("), expr.count(")")
        expr += ")" * max(0, open_b - close_b)
        res = eval(expr, SAFE_NAMES)  # 버튼 입력만 들어오고 builtins는 막아둠
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        return str(res)
    except Exception:
        return "0"


# 전역변수: 수식 문자열 (global.py의 st.session_state.x = 0 과 같은 방식)
# 페이지 전체가 처음 실행될 때만 0으로 초기화된다.
st.session_state.expr = "0"

st.title("🧮 Simple Calc")


@st.fragment()
def calculator():
    display = st.empty()  # 버튼 처리 후 결과를 채울 자리

    for r, row in enumerate(ROWS):
        cols = st.columns(len(row))
        for c, (label, value) in enumerate(row):
            kind = "primary" if label == "=" else "secondary"
            if cols[c].button(label, key=f"btn_{r}_{c}", type=kind, use_container_width=True):
                expr = st.session_state.expr
                if label == "DEL":
                    st.session_state.expr = "0" if len(expr) <= 1 else expr[:-1]
                elif label == "C":
                    st.session_state.expr = "0"
                elif label == "=":
                    st.session_state.expr = calculate(expr)
                else:
                    st.session_state.expr = value if expr == "0" else expr + value

    display.code(st.session_state.expr, language=None)


calculator()
st.caption("sin/cos/tan은 각도(degree) 기준 · n제곱근은 root(n,x) 형태 (예: root(3,8) = 2)")

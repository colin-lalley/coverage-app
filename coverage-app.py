import streamlit as st

st.set_page_config(page_title="Business Insurance Assessment", page_icon="🛡️", layout="centered")

# ----------------------------
# Questions (mirrors your React version)
# ----------------------------
QUESTIONS = [
    {
        "id": "industry",
        "question": "What industry is your company in?",
        "type": "select",
        "options": [
            "Technology/SaaS",
            "Professional Services",
            "E-commerce/Retail",
            "Healthcare",
            "Financial Services",
            "Manufacturing",
            "Construction",
            "Food & Beverage",
            "Other",
        ],
    },
    {
        "id": "employees",
        "question": "How many employees do you have?",
        "type": "select",
        "options": ["1-10", "11-50", "51-200", "201-500", "500+"],
    },
    {
        "id": "revenue",
        "question": "What is your annual revenue?",
        "type": "select",
        "options": ["Under $1M", "$1M-$5M", "$5M-$10M", "$10M-$50M", "Over $50M"],
    },
    {"id": "hasPhysicalLocation", "question": "Do you have a physical office or storefront?", "type": "boolean"},
    {"id": "handlesCustomerData", "question": "Do you collect or store customer data?", "type": "boolean"},
    {"id": "hasBoard", "question": "Do you have a board of directors or outside investors?", "type": "boolean"},
    {"id": "providesAdvice", "question": "Do you provide professional advice or services to clients?", "type": "boolean"},
    {"id": "hasVehicles", "question": "Does your business own or use vehicles?", "type": "boolean"},
]


def init_state():
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "show_results" not in st.session_state:
        st.session_state.show_results = False
    if "answers" not in st.session_state:
        st.session_state.answers = {
            "industry": "",
            "employees": "",
            "revenue": "",
            "hasPhysicalLocation": None,
            "handlesCustomerData": None,
            "hasBoard": None,
            "providesAdvice": None,
            "hasVehicles": None,
        }


def reset_assessment():
    st.session_state.step = 0
    st.session_state.show_results = False
    st.session_state.answers = {
        "industry": "",
        "employees": "",
        "revenue": "",
        "hasPhysicalLocation": None,
        "handlesCustomerData": None,
        "hasBoard": None,
        "providesAdvice": None,
        "hasVehicles": None,
    }


def answer_current(value):
    q = QUESTIONS[st.session_state.step]
    st.session_state.answers[q["id"]] = value

    if st.session_state.step < len(QUESTIONS) - 1:
        st.session_state.step += 1
    else:
        st.session_state.show_results = True


def get_recommendations(answers):
    recs = []

    # General Liability - recommended for almost all businesses
    recs.append(
        {
            "name": "General Liability Insurance",
            "priority": "Essential",
            "reason": (
                "Protects against claims of bodily injury, property damage, and advertising injury. "
                "Required by most commercial leases and client contracts."
            ),
        }
    )

    # Workers Compensation
    if answers["employees"] != "1-10" or bool(answers["hasPhysicalLocation"]):
        recs.append(
            {
                "name": "Workers Compensation Insurance",
                "priority": "Essential",
                "reason": (
                    "Required by law in most states when you have employees. "
                    "Covers medical costs and lost wages for work-related injuries."
                ),
            }
        )

    # Professional Liability
    if bool(answers["providesAdvice"]) or answers["industry"] in [
        "Technology/SaaS",
        "Professional Services",
        "Financial Services",
    ]:
        recs.append(
            {
                "name": "Professional Liability Insurance (E&O)",
                "priority": "Essential",
                "reason": (
                    "Protects against claims of negligence, errors, or failure to deliver promised services. "
                    "Critical for service-based businesses."
                ),
            }
        )

    # Cyber Liability
    if bool(answers["handlesCustomerData"]) or answers["industry"] in [
        "Technology/SaaS",
        "Healthcare",
        "Financial Services",
        "E-commerce/Retail",
    ]:
        recs.append(
            {
                "name": "Cyber Liability Insurance",
                "priority": "Highly Recommended",
                "reason": (
                    "Covers data breaches, ransomware attacks, and regulatory fines. "
                    "Essential for any business handling customer data."
                ),
            }
        )

    # D&O
    if bool(answers["hasBoard"]) or answers["revenue"] != "Under $1M":
        recs.append(
            {
                "name": "Directors & Officers (D&O) Insurance",
                "priority": "Highly Recommended",
                "reason": (
                    "Protects company leadership from personal liability for business decisions. "
                    "Important for attracting board members and investors."
                ),
            }
        )

    # Commercial Property
    if bool(answers["hasPhysicalLocation"]):
        recs.append(
            {
                "name": "Commercial Property Insurance",
                "priority": "Recommended",
                "reason": (
                    "Covers damage to your building, equipment, and inventory from fire, theft, or natural disasters."
                ),
            }
        )

    # Business Interruption
    if answers["revenue"] != "Under $1M" and bool(answers["hasPhysicalLocation"]):
        recs.append(
            {
                "name": "Business Interruption Insurance",
                "priority": "Recommended",
                "reason": (
                    "Covers lost income and operating expenses if your business is forced to close temporarily "
                    "due to a covered event."
                ),
            }
        )

    # Commercial Auto
    if bool(answers["hasVehicles"]):
        recs.append(
            {
                "name": "Commercial Auto Insurance",
                "priority": "Essential",
                "reason": "Required by law if your business owns vehicles. Covers accidents involving company vehicles.",
            }
        )

    # EPLI
    if answers["employees"] != "1-10":
        recs.append(
            {
                "name": "Employment Practices Liability (EPLI)",
                "priority": "Recommended",
                "reason": (
                    "Protects against claims of discrimination, wrongful termination, and harassment by employees."
                ),
            }
        )

    return recs


def pill(priority: str) -> str:
    # Simple “badge” rendering via markdown
    if priority == "Essential":
        return "🔴 **Essential**"
    if priority == "Highly Recommended":
        return "🟠 **Highly Recommended**"
    return "🔵 **Recommended**"


# ----------------------------
# App
# ----------------------------
init_state()

st.title("Business Insurance Assessment")
st.caption("Answer a few questions to get recommended insurance policies for your business.")

if st.session_state.show_results:
    st.subheader("Your Insurance Recommendations")

    recs = get_recommendations(st.session_state.answers)

    st.info("Based on your responses, here are the insurance policies we recommend for your business:")

    for r in recs:
        with st.container(border=True):
            st.markdown(f"### {r['name']}")
            st.markdown(pill(r["priority"]))
            st.write(r["reason"])

    st.warning(
        "This assessment provides general guidance only. Every business is unique, and your specific needs may vary. "
        "Consult with an insurance professional for personalized advice."
    )

    if st.button("Start New Assessment"):
        reset_assessment()
        st.rerun()

else:
    step = st.session_state.step
    q = QUESTIONS[step]
    progress = int(((step + 1) / len(QUESTIONS)) * 100)

    st.write(f"**Question {step + 1} of {len(QUESTIONS)}**")
    st.progress(progress)

    st.subheader(q["question"])

    if q["type"] == "select":
        # Use a radio to mimic “click an option”
        choice = st.radio(
            label="Select one:",
            options=q["options"],
            index=None,
            key=f"radio_{q['id']}_{step}",
        )
        col1, col2 = st.columns([1, 1])
        with col1:
            if step > 0 and st.button("Back"):
                st.session_state.step -= 1
                st.rerun()
        with col2:
            if st.button("Next", disabled=(choice is None)):
                answer_current(choice)
                st.rerun()

    elif q["type"] == "boolean":
        colA, colB = st.columns(2)
        with colA:
            if st.button("Yes"):
                answer_current(True)
                st.rerun()
        with colB:
            if st.button("No"):
                answer_current(False)
                st.rerun()

        if step > 0:
            if st.button("Back"):
                st.session_state.step -= 1
                st.rerun()

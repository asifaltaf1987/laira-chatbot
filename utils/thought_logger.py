def display_thoughts(query, tool_used=None):
    st.markdown("---")
    msg = f"🧠 **Thoughts**: Retrieved relevant context for: *{query}*"
    if tool_used:
        msg += f" using **{tool_used}**."
    st.markdown(msg)

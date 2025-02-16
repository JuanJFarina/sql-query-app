import streamlit as st
import requests
import json

# Configuration
TEXT_TO_SQL_SERVICE = "http://text_to_sql_service:8000"
DATABASE_SERVICE = "http://database_service:8000"
LLM_SERVICE = "http://llm_service:8000"  # Optional

st.title("Natural Language to SQL Query System")
st.markdown("Enter your question in plain English:")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Input form
with st.form("query_form"):
    question = st.text_input(
        "Your question:",
        placeholder="E.g., What is the most bought product on Fridays?",
    )
    use_llm = st.checkbox("Convert result to natural language (LLM)", value=False)
    submitted = st.form_submit_button("Submit")

if submitted and question:
    try:
        # Step 1: Generate SQL
        with st.spinner("Generating SQL query..."):
            sql_response = requests.post(
                f"{TEXT_TO_SQL_SERVICE}/generate_sql", json={"question": question}
            )
            sql_response.raise_for_status()
            sql_data = sql_response.json()
            generated_sql = sql_data["sql"]

        # Step 2: Execute SQL
        with st.spinner("Executing query..."):
            db_response = requests.post(
                f"{DATABASE_SERVICE}/execute_query", json={"query": generated_sql}
            )
            db_response.raise_for_status()
            result = db_response.json().get("result", [])

        # Step 3: Optional LLM processing
        final_output = ""
        if use_llm and LLM_SERVICE:
            with st.spinner("Generating natural language response..."):
                llm_response = requests.post(
                    f"{LLM_SERVICE}/generate_response",
                    json={"question": question, "sql_result": result},
                )
                llm_response.raise_for_status()
                final_output = llm_response.json().get("answer", "")
        else:
            final_output = json.dumps(result, indent=2)

        # Display results
        st.subheader("Generated SQL:")
        st.code(generated_sql, language="sql")

        st.subheader("Result:")
        if isinstance(final_output, str) and final_output.startswith("{"):
            st.json(final_output)
        else:
            st.markdown(final_output)

        # Add to history
        st.session_state.history.append(
            {"question": question, "sql": generated_sql, "result": final_output}
        )

    except requests.exceptions.RequestException as e:
        st.error(f"Error processing request: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

# Display query history
st.sidebar.title("Query History")
for idx, entry in enumerate(st.session_state.history[::-1]):
    with st.sidebar.expander(f"Query {len(st.session_state.history) - idx}"):
        st.markdown(f"**Question:** {entry['question']}")
        st.markdown(f"**SQL:** ```sql\n{entry['sql']}\n```")
        st.markdown("**Result:**")
        st.write(entry["result"])

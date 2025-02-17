import os
import json
import requests
import streamlit as st

TEXT_TO_SQL_SERVICE = os.environ.get("TEXT_TO_SQL_SERVICE")
TEXT_TO_SQL_PORT = os.environ.get("TEXT_TO_SQL_PORT")
DATABASE_SERVICE = os.environ.get("DATABASE_SERVICE")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
LLM_SERVICE = os.environ.get("LLM_SERVICE")
LLM_PORT = os.environ.get("LLM_PORT")

st.title("Natural Language to SQL Query System")
st.markdown("Enter your question in plain English:")

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("query_form"):
    question = st.text_input(
        "Your question:",
        placeholder="E.g., What is the most bought product on Fridays?",
    )
    use_llm = st.checkbox("Convert result to natural language (LLM)", value=False)
    submitted = st.form_submit_button("Submit")

if submitted and question:
    try:
        with st.spinner("Generating SQL query..."):
            sql_response = requests.post(
                f"http://{TEXT_TO_SQL_SERVICE}:{TEXT_TO_SQL_PORT}/generate_sql",
                json={"question": question},
            )
            sql_response.raise_for_status()
            sql_data = sql_response.json()
            generated_sql = sql_data["sql"]

        final_output = f"SQL query: {generated_sql}\n"
        print(f"Generated SQL query: {generated_sql}")

        with st.spinner("Executing query..."):
            db_response = requests.post(
                f"http://{DATABASE_SERVICE}:{DATABASE_PORT}/execute_query",
                json={"query": generated_sql},
            )
            db_response.raise_for_status()
            result = db_response.json().get("result", [])

        final_output += f"Result: {result}\n"

        if use_llm and LLM_SERVICE:
            with st.spinner("Generating natural language response..."):
                llm_response = requests.post(
                    f"http://{LLM_SERVICE}:{LLM_PORT}/generate_response",
                    json={"question": question, "sql_result": result},
                )
                llm_response.raise_for_status()
                final_output = llm_response.json().get("answer", "")
        else:
            final_output += f"In Natural Language: {json.dumps(result, indent=2)}"

        st.subheader("Generated SQL:")
        st.code(generated_sql, language="sql")

        st.subheader("Result:")
        if isinstance(final_output, str) and final_output.startswith("{"):
            st.json(final_output)
        else:
            st.markdown(final_output)

        st.session_state.history.append(
            {"question": question, "sql": generated_sql, "result": final_output}
        )

    except requests.exceptions.RequestException as e:
        st.error(f"Error processing request: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

st.sidebar.title("Query History")
for idx, entry in enumerate(st.session_state.history[::-1]):
    with st.sidebar.expander(f"Query {len(st.session_state.history) - idx}"):
        st.markdown(f"**Question:** {entry['question']}")
        st.markdown(f"**SQL:** ```sql\n{entry['sql']}\n```")
        st.markdown("**Result:**")
        st.write(entry["result"])

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from database.database import create_task, read_tasks, update_task, delete_task


def show_home_page(database_path):
    st.title("To-Do Application")

    # Add new task section
    task = st.text_input("Enter a new task")
    if st.button("Add Task"):
        if task:
            create_task(task, database_path)
            st.success("Task added!")
            st.rerun()

    # Get tasks and create dataframe
    tasks = read_tasks(database_path)
    if tasks:
        df = pd.DataFrame(tasks, columns=["id", "task"])

        # Configure grid options
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_column(
            "id",
            headerName="ID",
            width=50,
        )
        gb.configure_column(
            "task",
            editable=True,
            headerName="Task",
            width=400,
            cellStyle={"cursor": "pointer"},
        )
        # Add selection column
        gb.configure_selection(
            selection_mode="multiple",
            use_checkbox=True,
        )
        gridOptions = gb.build()

        # Create columns for buttons
        col1, col2 = st.columns([4, 1])

        with col1:
            grid_response = AgGrid(
                df,
                gridOptions=gridOptions,
                update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.VALUE_CHANGED,
                fit_columns_on_grid_load=True,
                theme="streamlit",
            )

        with col2:
            # Save Changes Button
            if st.button("Save Changes"):
                updated_df = pd.DataFrame(grid_response["data"])
                if not updated_df.empty:
                    for _, row in updated_df.iterrows():
                        original_task = df[df["id"] == row["id"]]["task"].iloc[0]
                        if row["task"] != original_task:
                            update_task(row["id"], row["task"], database_path)
                    st.success("Changes saved!")
                    st.rerun()

            # Handle selected rows for deletion
            selected_rows = grid_response.get("selected_rows")

            # Convert selected rows to list if we have selections
            if selected_rows is not None:
                if isinstance(selected_rows, pd.DataFrame):
                    selected_rows = selected_rows.to_dict("records")

                if len(selected_rows) > 0:
                    st.write(f"Selected {len(selected_rows)} task(s)")
                    if st.button("Delete Selected", type="primary"):
                        try:
                            for row in selected_rows:
                                task_id = row.get("id")
                                if task_id is not None:
                                    delete_task(task_id, database_path)
                            st.success(f"Deleted {len(selected_rows)} task(s)")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting tasks: {str(e)}")

    else:
        st.write("No tasks available.")

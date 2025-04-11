import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
from database.database import create_task, read_tasks, update_task, delete_task


def show_home_page(database_path):
    st.title("To-Do Application")

    # Add new task section
    task = st.text_input("Enter a new task")
    if st.button("Add Task"):
        if task:  # Only add if task is not empty
            create_task(task, database_path)
            st.success("Task added!")
            st.rerun()

    # Get tasks and create dataframe
    tasks = read_tasks(database_path)
    if tasks:
        df = pd.DataFrame(tasks, columns=["id", "task"])

        # Custom delete button renderer with callback
        delete_btn_renderer = JsCode(
            """
        class DeleteButtonRenderer {
            init(params) {
                this.params = params;
                this.eGui = document.createElement('button');
                this.eGui.innerHTML = '🗑️';
                this.eGui.className = 'btn-delete';
                this.eGui.style = 'border: none; background: none; color: red; cursor: pointer;';
                this.eGui.addEventListener('click', () => this.onClick());
            }

            getGui() {
                return this.eGui;
            }

            onClick() {
                const task_id = this.params.data.id;
                this.params.api.applyTransaction({
                    remove: [this.params.data]
                });
            }
        }
        """
        )

        # Configure grid options
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_column("id", hide=True)
        gb.configure_column(
            "task",
            editable=True,
            headerName="Task",
            width=400,
            cellStyle={"cursor": "pointer"},
        )
        gb.configure_column(
            "actions",
            headerName="",
            cellRenderer=delete_btn_renderer,
            width=70,
            lockPosition=True,
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
                allow_unsafe_jscode=True,
                theme="streamlit",
                height=400,
                custom_css={
                    ".ag-cell-inline-editing": {"padding": "10px !important"},
                    ".ag-header-cell-text": {"color": "#495057"},
                },
            )

        with col2:
            if st.button("Save Changes"):
                updated_df = pd.DataFrame(grid_response["data"])
                if not updated_df.equals(df):
                    # Handle updates
                    for _, row in updated_df.iterrows():
                        original_task = df[df["id"] == row["id"]]["task"].iloc[0]
                        if row["task"] != original_task:
                            update_task(row["id"], row["task"], database_path)

                    # Handle deletions
                    deleted_ids = set(df["id"]) - set(updated_df["id"])
                    for task_id in deleted_ids:
                        delete_task(task_id, database_path)

                    st.success("Changes saved!")
                    st.rerun()

    else:
        st.write("No tasks available.")

# %%writefile app.py
import streamlit as st
import pandas as pd

# Initialize book data
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Title", "Author", "Genre", "Year", "Status"])

# Load existing data or initialize
if "library_data" not in st.session_state:
    st.session_state.library_data = load_data()

# Application title
st.title("📚 Automatic Library Management System")

# Menu
menu = st.sidebar.radio("📋 Menu", ["Add Book", "View Books", "Search Book", "Delete Book", "Check Out/Return Book"])

# Add Book
if menu == "Add Book":
    st.header("Add a New Book to the Library")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.selectbox("Genre",["Horror","Drama","Fantasy","Thiriler","Comedy"])
        year = st.number_input("Year", min_value=1900, max_value=2025)
        submit = st.form_submit_button("Add Book")

        if submit:
            if title and author:
                new_book = {"Title": title, "Author": author, "Genre": genre, "Year": year, "Status": "Available"}
                st.session_state.library_data = pd.concat([st.session_state.library_data, pd.DataFrame([new_book])], ignore_index=True)
                st.success("Book added successfully!")
            else:
                st.error("Please fill in all required fields.")

# View Books
elif menu == "View Books":
    st.header("Library Books")
    st.dataframe(st.session_state.library_data)

# Search Book
elif menu == "Search Book":
    st.header("Search for a Book")
    search_option = st.radio("Search by:", ("Title", "Author"))
    query = st.text_input(f"Enter {search_option}:")

    if query:
        filtered_data = st.session_state.library_data[
            st.session_state.library_data[search_option].str.contains(query, case=False, na=False)
        ]
        if not filtered_data.empty:
            st.dataframe(filtered_data)
        else:
            st.warning(f"No books found with {search_option} matching '{query}'.")

# Delete Book
elif menu == "Delete Book":
    st.header("Delete a Book")

    if not st.session_state.library_data.empty:
            selected_book = st.selectbox("Select a book to remove:", st.session_state.library_data["Title"])
    if st.button("Delete"):
            st.session_state.library_data = st.session_state.library_data[st.session_state.library_data["Title"] != selected_book]
            st.success("Book deleted successfully!")
   
   
# Check Out / Return Book
elif menu == "Check Out/Return Book":
    st.header("Manage Book Status")
    with st.form("manage_status_form"):
        book_title = st.text_input("Enter Book Title")
        action = st.selectbox("Action", ["Check Out", "Return"])
        submit = st.form_submit_button("Update Status")

        if submit:
            if book_title:
                book_index = st.session_state.library_data[
                    st.session_state.library_data["Title"].str.lower() == book_title.lower()
                ].index

                if not book_index.empty:
                    idx = book_index[0]
                    current_status = st.session_state.library_data.at[idx, "Status"]
                    if action == "Check Out" and current_status == "Available":
                        st.session_state.library_data.at[idx, "Status"] = "Checked Out"
                        st.success("Book checked out successfully!")
                    elif action == "Return" and current_status == "Checked Out":
                        st.session_state.library_data.at[idx, "Status"] = "Available"
                        st.success("Book returned successfully!")
                    else:
                        st.error(f"Cannot perform action. Current status: {current_status}")
                else:
                    st.error("Book not found. Please check the title and try again.")
            else:
                st.error("Please enter a book title.")

import streamlit as st
import json
import os

# ========== Utility Functions ==========

LIBRARY_FILE = "library.json"

def load_library():
    """Load the library from a JSON file."""
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

def save_library(data):
    """Save the library to a JSON file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(data, file, indent=4)

# ========== Main App ==========

# Page configuration
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Initialize
library = load_library()

# Title
st.title("📚 Personal Library Manager")
st.caption("Manage your books with ease — add, view, search, or remove from your personal collection.")

# Sidebar Menu
menu = st.sidebar.radio("Menu", ["📖 View Library", "➕ Add Book", "❌ Remove Book", "🔍 Search Book", "💾 Save and Exit"])

# ========== View Library ==========
if menu == "📖 View Library":
    st.subheader("Your Book Collection")
    if library:
        for book in library:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                **📘 Title:** {book['title']}  
                **✍️ Author:** {book['author']}  
                **📅 Year:** {book['year']}  
                **🏷️ Genre:** {book['genre']}  
                """)
            with col2:
                badge = "✅ Read" if book['read_status'] else "📕 Unread"
                st.markdown(f"<div style='margin-top: 1.5em;'>{badge}</div>", unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.info("No books in your library yet. Add some from the sidebar!")

# ========== Add Book ==========
elif menu == "➕ Add Book":
    st.subheader("Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Year", min_value=1000, max_value=2100, step=1, format="%d")
        genre = st.text_input("Genre")
        read_status = st.checkbox("Mark as Read")
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if title and author:
                library.append({
                    "title": title.strip(),
                    "author": author.strip(),
                    "year": year,
                    "genre": genre.strip(),
                    "read_status": read_status
                })
                save_library(library)
                st.success(f"✅ '{title}' added to your library!")
                st.balloons()
                st.rerun()
            else:
                st.error("Title and Author fields cannot be empty!")

# ========== Remove Book ==========
elif menu == "❌ Remove Book":
    st.subheader("Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        selected_title = st.selectbox("Choose a book to remove", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != selected_title]
            save_library(library)
            st.success(f"❌ '{selected_title}' removed from your library.")
            st.rerun()
    else:
        st.info("No books available to remove.")

# ========== Search Book ==========
elif menu == "🔍 Search Book":
    st.subheader("Search Your Library")
    query = st.text_input("Enter a title or author name")
    if st.button("Search"):
        results = [
            book for book in library
            if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()
        ]
        if results:
            st.success(f"Found {len(results)} matching result(s):")
            st.table(results)
        else:
            st.warning("No books found matching your search.")

# ========== Save and Exit ==========
elif menu == "💾 Save and Exit":
    save_library(library)
    st.success("✅ Your library has been saved successfully!")
    st.stop()

import tkinter as tk
from tkinter import messagebox
from database import init_db, add_book, get_all_books


def refresh_book_list(listbox):
    listbox.delete(0, tk.END)
    for book in get_all_books():
        book_id, title, author = book
        display_text = f"{title} — {author}"
        listbox.insert(tk.END, display_text)


def open_add_book_window(parent, book_listbox):
    window = tk.Toplevel(parent)
    window.title("Add Book")
    window.geometry("300x200")

    tk.Label(window, text="Title").pack(pady=(10, 0))
    title_entry = tk.Entry(window, width=30)
    title_entry.pack()

    tk.Label(window, text="Author").pack(pady=(10, 0))
    author_entry = tk.Entry(window, width=30)
    author_entry.pack()

    def save_book():
        title = title_entry.get().strip()
        author = author_entry.get().strip()

        if not title:
            messagebox.showerror("Error", "Title is required")
            return

        add_book(title, author)
        refresh_book_list(book_listbox)
        window.destroy()

    tk.Button(window, text="Save", command=save_book).pack(pady=15)


def main():
    init_db()

    root = tk.Tk()
    root.title("Book Annotator")
    root.geometry("800x500")

    # Left frame (books)
    left_frame = tk.Frame(root, width=250)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(left_frame, text="Books").pack()

    book_listbox = tk.Listbox(left_frame, width=40)
    book_listbox.pack(fill=tk.BOTH, expand=True)

    tk.Button(
        left_frame,
        text="Add Book",
        command=lambda: open_add_book_window(root, book_listbox)
    ).pack(pady=10)

    refresh_book_list(book_listbox)

    root.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import messagebox
from database import (
    init_db,
    add_book,
    get_all_books,
    get_annotations_for_book,
)

books_cache = []


def refresh_book_list(listbox):
    global books_cache
    listbox.delete(0, tk.END)
    books_cache = get_all_books()

    for book in books_cache:
        _, title, author = book
        listbox.insert(tk.END, f"{title} — {author}")


def refresh_annotation_list(listbox, book_id):
    listbox.delete(0, tk.END)
    annotations = get_annotations_for_book(book_id)

    for annotation in annotations:
        _, quote, created_at = annotation
        preview = quote[:50] + "..." if quote and len(quote) > 50 else quote
        listbox.insert(tk.END, f"{created_at} | {preview}")


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


def on_book_selected(event, annotation_listbox):
    selection = event.widget.curselection()
    if not selection:
        return

    index = selection[0]
    book_id, _, _ = books_cache[index]
    refresh_annotation_list(annotation_listbox, book_id)


def main():
    init_db()

    root = tk.Tk()
    root.title("Book Annotator")
    root.geometry("900x500")

    # Left frame (books)
    left_frame = tk.Frame(root, width=250)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(left_frame, text="Books").pack()

    book_listbox = tk.Listbox(left_frame)
    book_listbox.pack(fill=tk.BOTH, expand=True)

    tk.Button(
        left_frame,
        text="Add Book",
        command=lambda: open_add_book_window(root, book_listbox),
    ).pack(pady=10)

    # Right frame (annotations)
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(right_frame, text="Annotations").pack()

    annotation_listbox = tk.Listbox(right_frame)
    annotation_listbox.pack(fill=tk.BOTH, expand=True)

    book_listbox.bind(
        "<<ListboxSelect>>",
        lambda event: on_book_selected(event, annotation_listbox),
    )

    refresh_book_list(book_listbox)

    root.mainloop()


if __name__ == "__main__":
    main()

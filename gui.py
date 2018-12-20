import scrap
import tkinter as tk
from tkinter import ttk
from tkinter import Menu


def _quit():
    """
    function closes main window
    """
    win.quit()
    win.destroy()
    exit()


data_dict = {
    "rating": "",
    "author": "",
    "new_books": "",
    "new_linkes": "",
    "most_books": "",
    "most_links": ""
}

# create main window:
win = tk.Tk()
win.title("Good Reads")

# add minue bar:
menubar = Menu()
win.config(menu=menubar)
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label='Exit', command=_quit)
menubar.add_cascade(label='File', menu=fileMenu)

# creat tab:
tabControl = ttk.Notebook(win)

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Tab 1')
tabControl.pack(expand=1, fill='both')

# choose genres:
choose_genres = ttk.LabelFrame(tab1, text='Choose genre    ')
choose_genres.grid(column=0, row=0, padx=8, pady=4)

ttk.Label(choose_genres, text='genre: ').grid(column=0,
                                              row=0, sticky='E')
genres = tk.StringVar()
genre_selected = ttk.Combobox(choose_genres, width=60, textvariable=genres)
genre_selected['values'] = scrap.getting_genres()[:-1]
genre_selected.grid(column=1, row=0)
genre_selected.current(0)
genre_selected.grid_configure(padx=10, pady=5)

# initialize dict values for combobox:
genre = genre_selected.get()
new_books, new_links = scrap.getting_new_releases(genre.replace("'", ''))
most_books, most_links = scrap.getting_most_read(genre.replace("'", ''))

data_dict["new_books"] = new_books
data_dict["most_books"] = most_books


# New releases:

choose_book = ttk.LabelFrame(tab1, text="NEW RELEASES", width=60)
choose_book.grid(column=0, row=1, padx=5, pady=4)

ttk.Label(choose_book, text='book: ').grid(column=0,
                                           row=0, sticky='E')
new_books = tk.StringVar()
new_book_selected = ttk.Combobox(choose_book, width=40, textvariable=new_books)
new_book_selected['values'] = data_dict["new_books"]
new_book_selected.grid(column=1, row=0)
new_book_selected.grid_configure(padx=15, pady=5)

# Most read this week:
choose_book2 = ttk.LabelFrame(tab1, text="MOST READ THIS WEEK", width=60)
choose_book2.grid(column=0, row=2, padx=5, pady=4)

ttk.Label(choose_book2, text='book: ').grid(column=0,
                                            row=0, sticky='E')
most_books = tk.StringVar()
most_book_selected = ttk.Combobox(choose_book2, 
                                  width=40, textvariable=most_books)
most_book_selected['values'] = data_dict["most_books"]
most_book_selected.grid(column=1, row=0)
most_book_selected.grid_configure(padx=15, pady=5)

# book info:
book_infos = ttk.LabelFrame(tab1, text='About Book  ')
book_infos.grid(column=0, row=3, padx=8, pady=4)

# author name:
ttk.Label(book_infos, text='by: ').grid(column=0,
                                        row=1, sticky='E')
name = tk.StringVar()
nameEntry = ttk.Entry(book_infos, width=63,
                      textvariable=name, state='readonly')

nameEntry.grid(column=1, row=1, sticky='W')

# rating:
ttk.Label(book_infos, text='rating: ').grid(column=0,
                                            row=2, sticky='E')

rate = tk.StringVar()
rateEntry = ttk.Entry(book_infos, width=63,
                      textvariable=rate, state='readonly')

rateEntry.grid(column=1, row=2, sticky='W')

# title:
ttk.Label(book_infos, text='title: ').grid(column=0,
                                           row=3, sticky='E')
title = tk.StringVar()
titleEntry = ttk.Entry(book_infos, width=63,
                       textvariable=title, state='readonly')

titleEntry.grid(column=1, row=3, sticky='W')

for child in book_infos.winfo_children():
    child.grid_configure(padx=4, pady=2)


def update_books_new():
    """
    function updates values for new releases section
    """
    genre = genre_selected.get()
    new_books, new_links = scrap.getting_new_releases(genre.replace("'", ''))

    data_dict["new_books"] = new_books
    data_dict["new_links"] = new_links

    new_book_selected['values'] = data_dict["new_books"]
    new_book_selected.current(0)


def update_books_most():
    """
    function updates values for most read this week section
    """
    genre = genre_selected.get()
    most_books, most_links = scrap.getting_most_read(genre.replace("'", ''))

    data_dict["most_books"] = most_books
    data_dict["most_links"] = most_links

    most_book_selected['values'] = data_dict["most_books"]
    most_book_selected.current(0)


def update_info():
    """
    function updates about book section for new releases
    """
    book = new_book_selected.get()
    rating, author = scrap.get_info(data_dict["new_links"][data_dict["new_books"].index(book)])
    data_dict["rating"] = rating
    data_dict["author"] = author
    name.set(data_dict["author"])
    rate.set(data_dict["rating"])
    title.set(book)


def update_info2():
    """
    function updates about book section for most read this week
    """
    book = most_book_selected.get()
    rating, author = scrap.get_info(data_dict["most_links"][data_dict["most_books"].index(book)])
    data_dict["rating"] = rating
    data_dict["author"] = author
    name.set(data_dict["author"])
    rate.set(data_dict["rating"])
    title.set(book)


# add buttons:
get_releases_btn = ttk.Button(choose_genres,
                              text='NEW RELEASES ',
                              width=30,
                              command=update_books_new)
get_releases_btn.grid(column=1, row=1)
                                                             
get_most_btn = ttk.Button(choose_genres,
                          text='MOST READ THIS WEEK ',
                          width=30,
                          command=update_books_most)
get_most_btn.grid(column=1, row=2, padx=20)

get_info_btn = ttk.Button(choose_book,
                          text='ABOUT BOOK ',
                          command=update_info).grid(column=2, row=0, padx=5)
get_info1_btn = ttk.Button(choose_book2,
                           text='ABOUT BOOK ',
                           command=update_info2).grid(column=2, row=0, padx=5)

win.mainloop()

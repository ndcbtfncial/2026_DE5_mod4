# print("hello world")

# def agecalc(dob):
from fastapi import FastAPI
from pydantic import BaseModel #standarised object creation and handling
from typing import List

app = FastAPI()

# Data Model - #basemodel is a format and a structure. A book is going to have the following formart (id, title, author)
class Book(BaseModel): 
    id: int
    title: str
    author: str

# Fake DB - list is using the typing library and importing the List
#so we are creating an empty list, but every thing in this list should come in the format of our 'Book' class.
#Typing library is used to describe the expected data types in python, so we dont have to validate ourself.

books: List[Book] = [
    Book(id=1, title="Alice", author="Lewis"),
    Book(id=2, title="BFG", author="Dahl")
]

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the library"}

# get all books
@app.get("/books", response_model=List[Book])
def get_books():
    return books

# get book by id
@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    # Find the first book that matches the ID
    book = next((b for b in books if b.id == book_id), None)
    
    # If no book is found, return a 404 error
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
        
    return book

# Create a new book
@app.post("/books", response_model=Book)
def create_book(book: Book):
    # check if ID already exists to avoid duplicates
    if any(b.id == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    
    books.append(book)
    return book

# Update a books info
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    # Find the index of the book to update
    for index, book in enumerate(books):
        if book.id == book_id:
            # Update the list with the new data
            books[index] = updated_book
            return updated_book
            
    # If the ID wasn't found in the loop
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book (by the ID)
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    global books  # Access the list in the global scope
    
    # Check if the book exists
    book_to_delete = next((b for b in books if b.id == book_id), None)
    
    if book_to_delete is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Filter the list to exclude the book with the matching ID
    books = [b for b in books if b.id != book_id]
    
    return {"message": f"Book with ID {book_id} has been deleted"}

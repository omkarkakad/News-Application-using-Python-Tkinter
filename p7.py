from tkinter import *
from tkinter import ttk
import requests 
import webbrowser


API_KEY = "1e66544b2b2b40e8ada2c75dfe9c2bf1"
BASE_URL = "https://newsapi.org/v2/everything"
root = Tk()
root.title("📰 News Application")
root.geometry("1000x700+200+50")
root.configure(bg="#f2f2f2")
root.resizable(False, False)

#fonts declaration
HEADER_FONT = ("Helvetica", 30, "bold")
SUBHEADER_FONT = ("Helvetica", 20, "bold")
TEXT_FONT = ("Helvetica", 12)

#UI setup
Label(root, text="Today's News", font=HEADER_FONT, fg="#333", bg="#f2f2f2").pack(pady=20)

# UI Setup
search_frame = Frame(root, bg="#f2f2f2")
search_frame.pack(pady=10)

Label(search_frame, text="🔍 Search News: ", font=SUBHEADER_FONT, bg="#f2f2f2").grid(row=0, column=0, padx=5)
search_entry = Entry(search_frame, font=SUBHEADER_FONT, width=30, bd=2, relief=SUNKEN)
search_entry.grid(row=0, column=1, padx=5)

Label(search_frame, text="🗂️ Category:", font=SUBHEADER_FONT, bg="#f2f2f2").grid(row=1, column=0, padx=5, pady=10)
category_cb = ttk.Combobox(search_frame, values=["general", "business", "technology", "sports", "health", "entertainment"], font=SUBHEADER_FONT, state="readonly")
category_cb.set("general")
category_cb.grid(row=1, column=1, padx=5, pady=10)

search_btn = Button(search_frame, text="Search", font=SUBHEADER_FONT, bg="#333", fg="white", width=10)
search_btn.grid(row=0, column=2, padx=10)

# News Display Frame 
news_frame = Frame(root, bg="#ffffff", bd=2, relief=RIDGE)
news_frame.pack(fill=BOTH, expand=True, padx=30, pady=20)

news_canvas = Canvas(news_frame, bg="#ffffff")
scrollbar = Scrollbar(news_frame, orient=VERTICAL, command=news_canvas.yview)
scrollable_frame = Frame(news_canvas, bg="#ffffff")

scrollable_frame.bind("<Configure>", lambda e: news_canvas.configure(scrollregion=news_canvas.bbox("all")))
news_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
news_canvas.configure(yscrollcommand=scrollbar.set)

news_canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

# Add News Card
def add_news_card(title, description, url):
    frame = Frame(scrollable_frame, bg="white", bd=1, relief=SOLID, padx=10, pady=10)
    frame.pack(fill=X, pady=5, padx=10)

    Label(frame, text=title, font=("Helvetica", 16, "bold"), fg="#1a237e", bg="white", wraplength=800, justify=LEFT).pack(anchor="w")
    Label(frame, text=description, font=TEXT_FONT, bg="white", wraplength=850, justify=LEFT).pack(anchor="w", pady=5)
    Button(frame, text="Read More", font=("Helvetica", 10, "bold"), fg="white", bg="#1a237e", cursor="hand2", command=lambda: webbrowser.open(url)).pack(anchor="e")

# Fetch news
def fetch_news():
    query = search_entry.get().strip()
    category = category_cb.get()
    
    #Clear previous results
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Base Parameters

    params = {
        "apiKey": API_KEY,
        "q": query if query else "India",  # fallback search term
        "pageSize": 20,
        "sortBy": "publishedAt",
        "language": "en"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        print("DEBUG RESPONSE:", data)

        if data["status"] == "ok":
            articles = data.get("articles", [])
            print("Articles Found:", len(articles))

            if not articles:
                add_news_card("No Results Found", "Try a different keyword or category.", "#")
            else:
                for article in articles:
                    title = article.get("title", "No Title")
                    description = article.get("description", "No Description")
                    url = article.get("url", "#")
                    add_news_card(title, description, url)
        else:
            add_news_card("API Error", data.get("message", "Something went wrong."), "#")

    except Exception as e:
        add_news_card("Error", str(e), "#")

# Bind Button
search_btn.config(command=fetch_news)

# Start with default fetch
fetch_news()
root.mainloop()

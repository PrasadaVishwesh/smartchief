import tkinter as tk
import requests
from PIL import Image, ImageTk
import webbrowser

def get_top_5_recipes():
    recipe_name = entry_recipe_name.get()
    if recipe_name:
        api_url = "https://api.edamam.com/search"
        app_id = "031629c4"
        app_key = "582e098bc644ad2a44f1bbbd6978807e"
        params = {
            "q": recipe_name,
            "app_id": app_id,
            "app_key": app_key,
            "from": 0,
            "to": 5,
        }

        response = requests.get(api_url, params=params)
        data = response.json()
        clear_recipe_list()

        if "hits" in data and data["hits"]:
            for i, hit in enumerate(data["hits"]):
                recipe = hit["recipe"]
                recipe_list.append(recipe)
                recipe_name = recipe["label"]
                recipe_link = recipe["url"]
                image_url = recipe["image"]

                recipe_title_label = tk.Label(
                    canvas_frame,
                    text=f"{i+1}. {recipe_name}",
                    font=("Helvetica", 12, "bold"),
                )
                recipe_title_label.pack(pady=(5, 0), anchor=tk.CENTER)

                image_response = requests.get(image_url, stream=True)
                image = Image.open(image_response.raw)
                image = image.resize((200, 200), Image.LANCZOS)
                photo_image = ImageTk.PhotoImage(image)
                image_label = tk.Label(canvas_frame, image=photo_image)
                image_label.image = photo_image
                image_label.pack(pady=(0, 5), anchor=tk.CENTER)

                link_label = tk.Label(
                    canvas_frame, text=recipe_link, fg="blue", cursor="hand2"
                )
                link_label.pack(pady=(0, 10), anchor=tk.CENTER)
                link_label.bind(
                    "<Button-1>", lambda event, link=recipe_link: open_link(link)
                )

                recipe_labels.append(recipe_title_label)
                recipe_images.append(photo_image)
                recipe_links.append(link_label)


def clear_recipe_list():
    recipe_list.clear()
    for label in recipe_labels:
        label.pack_forget()
    recipe_labels.clear()
    for image_label in recipe_images:
        image_label.pack_forget()
    recipe_images.clear()
    for link_label in recipe_links:
        link_label.pack_forget()
    recipe_links.clear()


def open_link(link):
    webbrowser.open(link)


root = tk.Tk()
root.title("Recipe Finder")
root.geometry("600x600")
root.configure(bg="#F1F1F1")

frame = tk.Frame(root, bg="#F1F1F1")
frame.pack(fill=tk.BOTH, expand=tk.YES, padx=20, pady=20)

label_recipe_name = tk.Label(
    frame, text="Enter Recipe Name:", font=("Helvetica", 14, "bold"), bg="#F1F1F1"
)
label_recipe_name.pack()

entry_recipe_name = tk.Entry(frame, font=("Helvetica", 12))
entry_recipe_name.pack(pady=5)

search_button = tk.Button(
    frame,
    text="Search Recipes",
    font=("Helvetica", 12, "bold"),
    command=get_top_5_recipes,
)
search_button.pack(pady=10)

canvas = tk.Canvas(frame, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

canvas_frame = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_frame, anchor=tk.NW)
canvas_frame.bind(
    "<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
)

recipe_list = []
recipe_labels = []
recipe_images = []
recipe_links = []


# Your existing functions here...
'''
def add_background_image(root, image_path):
    image = Image.open(image_path)
    image = image.resize((600, 600), Image.LANCZOS)
    photo_image = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(root, width=600, height=1000, bg="white")
    canvas.pack(fill=tk.BOTH, expand=tk.YES)
    canvas.create_image(0, 0, image=photo_image, anchor=tk.NW)
    return photo_image

background_image = add_background_image(root, "/Users/abhi/Desktop/fresh-colourful-ingredients-mexican-cuisine_23-2148254294.jpg copy.tiff") 


'''
root.mainloop()

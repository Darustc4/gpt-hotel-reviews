import os
import openai
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from PIL import Image

from gpt_reviewer import Analyzer, Review, Scoring

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

header_label_color = "#327ab3"
header_font_color = "#DCE4EE"
container_background_color = "#f0f0f0"

class Reviewer(ctk.CTk):
    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        self.analyzer = Analyzer()

        self.hygiene_score = 0
        self.food_score = 0
        self.reception_score = 0
        self.bar_score = 0
        self.other_comments_score = 0

        self.create_tk()

    def create_tk(self):
        super().__init__()

        self.title("GPT Reviewer")
        self.geometry("800x1000")

        self.create_frames()
        self.create_widgets()

    def create_frames(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Scoring Frame
        self.grid_rowconfigure(1, weight=8) # Review Frame
        self.grid_rowconfigure(2, weight=1) # Submit Frame

        # Scoring Frame
        self.tk_scoring_frame = ctk.CTkFrame(self, corner_radius=0)
        self.tk_scoring_frame.grid(row=0, column=0, sticky="nsew")

        # 10 Columns, 2 for each score (Hygiene, Food, Reception, Bar, Other Comments)
        self.tk_scoring_frame.grid_columnconfigure(0, weight=0)
        self.tk_scoring_frame.grid_columnconfigure(1, weight=1)
        self.tk_scoring_frame.grid_columnconfigure(2, weight=0)
        self.tk_scoring_frame.grid_columnconfigure(3, weight=1)
        self.tk_scoring_frame.grid_columnconfigure(4, weight=0)
        self.tk_scoring_frame.grid_columnconfigure(5, weight=1)
        self.tk_scoring_frame.grid_columnconfigure(6, weight=0)
        self.tk_scoring_frame.grid_columnconfigure(7, weight=1)
        self.tk_scoring_frame.grid_columnconfigure(8, weight=0)
        self.tk_scoring_frame.grid_columnconfigure(9, weight=1)
        self.tk_scoring_frame.grid_rowconfigure(0, weight=0)
        self.tk_scoring_frame.grid_rowconfigure(1, weight=0)

        # Review Frame
        self.tk_review_frame = ctk.CTkFrame(self, corner_radius=0)
        self.tk_review_frame.grid(row=1, column=0, sticky="nsew")

        self.tk_review_frame.grid_columnconfigure(0, weight=1)
        self.tk_review_frame.grid_columnconfigure(1, weight=8)
        self.tk_review_frame.grid_rowconfigure(0, weight=0)
        self.tk_review_frame.grid_rowconfigure(1, weight=1)
        self.tk_review_frame.grid_rowconfigure(2, weight=0)
        self.tk_review_frame.grid_rowconfigure(3, weight=1)
        self.tk_review_frame.grid_rowconfigure(4, weight=0)
        self.tk_review_frame.grid_rowconfigure(5, weight=1)
        self.tk_review_frame.grid_rowconfigure(6, weight=0)
        self.tk_review_frame.grid_rowconfigure(7, weight=1)
        self.tk_review_frame.grid_rowconfigure(8, weight=0)
        self.tk_review_frame.grid_rowconfigure(9, weight=1)

        # Submit Frame
        self.tk_submit_frame = ctk.CTkFrame(self, corner_radius=0)
        self.tk_submit_frame.grid(row=2, column=0, sticky="nsew")

        self.tk_submit_frame.grid_columnconfigure(0, weight=1)
        self.tk_submit_frame.grid_columnconfigure(1, weight=8)
        self.tk_submit_frame.grid_rowconfigure(0, weight=1)

    def create_widgets(self):
        # Scoring Frame
        self.tk_score_hygiene_label = ctk.CTkLabel(self.tk_scoring_frame, text="Hygiene Score", bg_color=header_label_color, text_color=header_font_color)
        self.tk_score_hygiene_label.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.tk_score_food_label = ctk.CTkLabel(self.tk_scoring_frame, text="Food Score", bg_color=header_label_color, text_color=header_font_color)
        self.tk_score_food_label.grid(row=0, column=2, sticky="nsew", columnspan=2)
        self.tk_score_reception_label = ctk.CTkLabel(self.tk_scoring_frame, text="Reception Score", bg_color=header_label_color, text_color=header_font_color)
        self.tk_score_reception_label.grid(row=0, column=4, sticky="nsew", columnspan=2)
        self.tk_score_bar_label = ctk.CTkLabel(self.tk_scoring_frame, text="Bar Score", bg_color=header_label_color, text_color=header_font_color)
        self.tk_score_bar_label.grid(row=0, column=6, sticky="nsew", columnspan=2)
        self.tk_score_other_label = ctk.CTkLabel(self.tk_scoring_frame, text="Other Comments", bg_color=header_label_color, text_color=header_font_color)
        self.tk_score_other_label.grid(row=0, column=8, sticky="nsew", columnspan=2)

        self.tk_score_hygiene_image = ctk.CTkImage(light_image=Image.open("gui_assets/safe.png"), dark_image=Image.open("gui_assets/safe.png"), size=(60,60))
        self.tk_score_hygiene_image_label = ctk.CTkLabel(self.tk_scoring_frame, image=self.tk_score_hygiene_image, text="")
        self.tk_score_hygiene_image_label.grid(row=1, column=0, sticky="nsew", padx=7, pady=7)

        self.tk_score_hygiene_count_var = tk.IntVar(self.tk_scoring_frame, value=0)
        self.tk_score_hygiene_count_label = ctk.CTkLabel(self.tk_scoring_frame, textvariable=self.tk_score_hygiene_count_var)
        self.tk_score_hygiene_count_label.grid(row=1, column=1, sticky="nsew")

        self.tk_score_food_image = ctk.CTkImage(light_image=Image.open("gui_assets/restaurant.png"), dark_image=Image.open("gui_assets/restaurant.png"), size=(60,60))
        self.tk_score_food_image_label = ctk.CTkLabel(self.tk_scoring_frame, image=self.tk_score_food_image, text="")
        self.tk_score_food_image_label.grid(row=1, column=2, sticky="nsew", padx=7, pady=7)

        self.tk_score_food_count_var = tk.IntVar(self.tk_scoring_frame, value=0)
        self.tk_score_food_count_label = ctk.CTkLabel(self.tk_scoring_frame, textvariable=self.tk_score_food_count_var)
        self.tk_score_food_count_label.grid(row=1, column=3, sticky="nsew")

        self.tk_score_reception_image = ctk.CTkImage(light_image=Image.open("gui_assets/reception.png"), dark_image=Image.open("gui_assets/reception.png"), size=(60,60))
        self.tk_score_reception_image_label = ctk.CTkLabel(self.tk_scoring_frame, image=self.tk_score_reception_image, text="")
        self.tk_score_reception_image_label.grid(row=1, column=4, sticky="nsew", padx=7, pady=7)

        self.tk_score_reception_count_var = tk.IntVar(self.tk_scoring_frame, value=0)
        self.tk_score_reception_count_label = ctk.CTkLabel(self.tk_scoring_frame, textvariable=self.tk_score_reception_count_var)
        self.tk_score_reception_count_label.grid(row=1, column=5, sticky="nsew")

        self.tk_score_bar_image = ctk.CTkImage(light_image=Image.open("gui_assets/martini.png"), dark_image=Image.open("gui_assets/martini.png"), size=(60,60))
        self.tk_score_bar_image_label = ctk.CTkLabel(self.tk_scoring_frame, image=self.tk_score_bar_image, text="")
        self.tk_score_bar_image_label.grid(row=1, column=6, sticky="nsew", padx=7, pady=7)

        self.tk_score_bar_count_var = tk.IntVar(self.tk_scoring_frame, value=0)
        self.tk_score_bar_count_label = ctk.CTkLabel(self.tk_scoring_frame, textvariable=self.tk_score_bar_count_var)
        self.tk_score_bar_count_label.grid(row=1, column=7, sticky="nsew")

        self.tk_score_other_image = ctk.CTkImage(light_image=Image.open("gui_assets/more-information.png"), dark_image=Image.open("gui_assets/more-information.png"), size=(60,60))
        self.tk_score_other_image_label = ctk.CTkLabel(self.tk_scoring_frame, image=self.tk_score_other_image, text="")
        self.tk_score_other_image_label.grid(row=1, column=8, sticky="nsew", padx=7, pady=7)

        self.tk_score_other_count_var = tk.IntVar(self.tk_scoring_frame, value=0)
        self.tk_score_other_count_label = ctk.CTkLabel(self.tk_scoring_frame, textvariable=self.tk_score_other_count_var)
        self.tk_score_other_count_label.grid(row=1, column=9, sticky="nsew")

        self.tk_scoring_frame_separator = ttk.Separator(self.tk_scoring_frame, orient="horizontal")
        self.tk_scoring_frame_separator.grid(row=2, column=0, sticky="nsew", columnspan=10)

        # Review Frame
        self.tk_hygiene_review_label = ctk.CTkLabel(self.tk_review_frame, text="Hygiene Review", bg_color=header_label_color, text_color=header_font_color)
        self.tk_hygiene_review_label.grid(row=0, column=0, sticky="nsew")
        self.tk_hygiene_review_clarification_label = ctk.CTkLabel(self.tk_review_frame, text="Describe the hygiene, maintenance and cleanliness of the hotel.")
        self.tk_hygiene_review_clarification_label.grid(row=0, column=1, sticky="nsew")

        self.tk_hygiene_review_text = tk.Text(self.tk_review_frame, height=5)
        self.tk_hygiene_review_text.grid(row=1, column=0, sticky="nsew", columnspan=2)

        self.tk_food_review_label = ctk.CTkLabel(self.tk_review_frame, text="Food Review", bg_color=header_label_color, text_color=header_font_color)
        self.tk_food_review_label.grid(row=2, column=0, sticky="nsew")
        self.tk_food_review_clarification_label = ctk.CTkLabel(self.tk_review_frame, text="Describe the food and restaurant experience.")
        self.tk_food_review_clarification_label.grid(row=2, column=1, sticky="nsew")

        self.tk_food_review_text = tk.Text(self.tk_review_frame, height=5)
        self.tk_food_review_text.grid(row=3, column=0, sticky="nsew", columnspan=2)

        self.tk_reception_review_label = ctk.CTkLabel(self.tk_review_frame, text="Reception Review", bg_color=header_label_color, text_color=header_font_color)
        self.tk_reception_review_label.grid(row=4, column=0, sticky="nsew")
        self.tk_reception_review_clarification_label = ctk.CTkLabel(self.tk_review_frame, text="Describe your experience with the reception and service staff.")
        self.tk_reception_review_clarification_label.grid(row=4, column=1, sticky="nsew")

        self.tk_reception_review_text = tk.Text(self.tk_review_frame, height=5)
        self.tk_reception_review_text.grid(row=5, column=0, sticky="nsew", columnspan=2)

        self.tk_bar_review_label = ctk.CTkLabel(self.tk_review_frame, text="Bar Review", bg_color=header_label_color, text_color=header_font_color)
        self.tk_bar_review_label.grid(row=6, column=0, sticky="nsew")
        self.tk_bar_review_clarification_label = ctk.CTkLabel(self.tk_review_frame, text="Describe your experience at the bar and other entertainment facilities.")
        self.tk_bar_review_clarification_label.grid(row=6, column=1, sticky="nsew")

        self.tk_bar_review_text = tk.Text(self.tk_review_frame, height=5)
        self.tk_bar_review_text.grid(row=7, column=0, sticky="nsew", columnspan=2)

        self.tk_other_review_label = ctk.CTkLabel(self.tk_review_frame, text="Other Review", bg_color=header_label_color, text_color=header_font_color)
        self.tk_other_review_label.grid(row=8, column=0, sticky="nsew")
        self.tk_other_review_clarification_label = ctk.CTkLabel(self.tk_review_frame, text="Include any other comments that do not fit in the above categories.")
        self.tk_other_review_clarification_label.grid(row=8, column=1, sticky="nsew")

        self.tk_other_review_text = tk.Text(self.tk_review_frame, height=5)
        self.tk_other_review_text.grid(row=9, column=0, sticky="nsew", columnspan=2)

        self.tk_review_frame_separator = ttk.Separator(self.tk_review_frame, orient="horizontal")
        self.tk_review_frame_separator.grid(row=10, column=0, sticky="nsew", columnspan=2)

        # Submit Frame
        self.tk_submit_button = ctk.CTkButton(self.tk_submit_frame, text="Submit", command=self.submit)
        self.tk_submit_button.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)

        self.tk_gpt_comment_text = tk.Text(self.tk_submit_frame, height=3)
        self.tk_gpt_comment_text.grid(row=0, column=1, sticky="nsew")

        self.set_feedback_text("You will receive feedback on your review here.")

    def set_feedback_text(self, text):
        self.tk_gpt_comment_text.configure(state="normal")
        self.tk_gpt_comment_text.delete(1.0, tk.END)
        self.tk_gpt_comment_text.insert(tk.END, text)
        self.tk_gpt_comment_text.see(tk.END)
        self.tk_gpt_comment_text.configure(state="disabled")

    def submit(self):
        review = Review(
            hygiene_review=self.tk_hygiene_review_text.get("1.0", "end-1c"),
            food_review=self.tk_food_review_text.get("1.0", "end-1c"),
            reception_review=self.tk_reception_review_text.get("1.0", "end-1c"),
            bar_review=self.tk_bar_review_text.get("1.0", "end-1c"),
            other_comments=self.tk_other_review_text.get("1.0", "end-1c")
        )

        results = self.analyzer.validate(review)

        if results.is_valid:
            new_scoring = self.analyzer.score(review)
            self.change_score(new_scoring)

            self.set_feedback_text("Thank you for your review!")

        else:
            self.set_feedback_text(results.explanation)

    def change_score(self, scores):
        def score_reward(score):
            if score == 1:      return -50
            elif score == 2:    return -25
            elif score == 3:    return 0
            elif score == 4:    return 50
            elif score == 5:    return 100
            else:               return 0

        self.hygiene_score += score_reward(scores.hygiene_score)
        self.food_score += score_reward(scores.food_score)
        self.reception_score += score_reward(scores.reception_score)
        self.bar_score += score_reward(scores.bar_score)
        self.other_comments_score += score_reward(scores.other_comments_score)

        self.tk_score_hygiene_count_var.set(self.hygiene_score)
        self.tk_score_food_count_var.set(self.food_score)
        self.tk_score_reception_count_var.set(self.reception_score)
        self.tk_score_bar_count_var.set(self.bar_score)
        self.tk_score_other_count_var.set(self.other_comments_score)



if __name__ == "__main__":
    app = Reviewer()
    app.mainloop()

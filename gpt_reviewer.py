import argparse
import json
import numpy as np
import pandas as pd
import openai
import os
import re

openai.api_key = os.environ.get("OPENAI_API_KEY")

class Results:
    def __init__(self, review, is_valid, explanation):
        self.review = review
        self.is_valid = is_valid
        self.explanation = explanation

    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Scoring:
    def __init__(self, hygiene_score, food_score, reception_score, bar_score, other_comments_score):
        self.hygiene_score = hygiene_score
        self.food_score = food_score
        self.reception_score = reception_score
        self.bar_score = bar_score
        self.other_comments_score = other_comments_score

    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return self.get_json()

class Review:
    def __init__(self, hygiene_review, food_review, reception_review, bar_review, other_comments):
        self.hygiene_review = hygiene_review
        self.food_review = food_review
        self.reception_review = reception_review
        self.bar_review = bar_review
        self.other_comments = other_comments

    def get_review_text(self):
        return '\n'.join((
            f"Hygiene review: {self.hygiene_review}",
            f"Food review: {self.food_review}",
            f"Reception review: {self.reception_review}",
            f"Bar review: {self.bar_review}",
            f"Other comments: {self.other_comments}"
        ))

    def get_gpt_validation_promt(self):
        return '\n'.join((
            "We would like to know if the following customer review for their stay at our hotel is legitimate and informative, since they are being rewarded for making a good review.",
            "The form the customer filled in contains fields for hygiene and cleaning, food, reception, bar and other comments. A review is valid if each review item offers some explanations for complaints or praises. Answer with 'valid' if the review is acceptable or 'invalid' otherwise. If the review is invalid, follow your answer after a dash ('-') with a single very brief explanation that will be directly displayed to the user for them to amend their review, and answer with no explanation if valid. Do not be too pedantic with the validity of the review.\n",
            self.get_review_text()
        ))

    def get_gpt_scoring_promt(self):
        return '\n'.join((
            "We would like to know how the customer felt about their stay at our hotel, for which they made a review.",
            "The form the customer filled in contains fields for hygiene, food, reception, bar and other comments. Please score from 1 to 5 how satisfied the customer was with each of these services (3 meaning neutral or no opinion) in the following format: ",
            "H: (1-5) F: (1-5) R: (1-5) B: (1-5) O: (1-5)",
            "Do not include any other text in the answer, and do not make any further clarifications.",
            self.get_review_text()
        ))

class Analyzer:
    def __init__(self):
        pass

    def validate(self, review):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful abedient assistant"},
                {"role": "user", "content": review.get_gpt_validation_promt()}
            ],
            temperature=0.0,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        response = response["choices"][0]["message"]["content"]

        response = response.split("-")
        is_valid = "invalid" not in response[0].lower()
        explanation = " ".join(response[1:]).lstrip()

        return Results(review, is_valid, explanation)

    def score(self, review):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful abedient assistant"},
                {"role": "user", "content": review.get_gpt_scoring_promt()}
            ],
            temperature=0.0,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        response = response["choices"][0]["message"]["content"]

        # Format 'H: 4 F: 4 R: 3 B: 4 O: 2'
        # Extract the scores using regex
        hygiene_score = int(re.search(r"H: (\d)", response).group(1))
        food_score = int(re.search(r"F: (\d)", response).group(1))
        reception_score = int(re.search(r"R: (\d)", response).group(1))
        bar_score = int(re.search(r"B: (\d)", response).group(1))
        other_comments_score = int(re.search(r"O: (\d)", response).group(1))

        return Scoring(hygiene_score, food_score, reception_score, bar_score, other_comments_score)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze a review with a LLM model and attriutes credit to the reviewed employees.')
    args = parser.parse_args()

    bad_review = Review(
        hygiene_review="The hotel was very clean and the staff were very friendly.",
        food_review="The food was very good and the staff were very friendly.",
        reception_review="The reception staff were very friendly.",
        bar_review="The bar staff were very friendly.",
        other_comments="The hotel was very clean and the staff were very friendly."
    )

    good_review = Review(
        hygiene_review="The hotel was very clean and the staff were very friendly. The cleaning staff was a bit annoying as they would knock on the door every day at 8am to ask if we wanted our room cleaned.",
        food_review="The food was good, I specially liked the breakfast. They had a good selection of all kinds of food and the staff were very friendly.",
        reception_review="Could have been better, they didn't change our electronic keys after it malfunctioned like 5 times in a day.",
        bar_review="The bar staff were nice to my family.",
        other_comments="The car park is tiny, it was horrible."
    )

    good_spanish_review = Review(
        hygiene_review="El hotel estaba limpio pero los limpiadores era un poco maleducados al llamar a la puerta todos los dias a las 8 de la mañana para limpiar, deberían únicamente limpiar cuando no estamos en el hotel.",
        food_review="La comida estaba buena, me gustó especialmente el desayuno. Había una buena selección de comidas y los camareros eran muy majos.",
        reception_review="Podría haber sido mejor, no nos cambiaron las llaves electrónicas incluso despues de que no funcionases multiples veces al día y la puesta se quedase bloqueada.",
        bar_review="Los baristas muy graciosos.",
        other_comments="El parking es demasiado pequeño y encontrar aparcamiento era imposible."
    )

    review = good_review

    analyzer = Analyzer()
    results = analyzer.validate(review)

    if results.is_valid:
        print("Review is valid")

        scoring = analyzer.score(review)

        print("Scoring:")
        print(scoring)
    else:
        print("Review is invalid")
        print(results.explanation)

        print()
        print("Review:")
        print(review.get_review_text())

# BiaSight - Gender Bias Detection on Websites using AI

![logo](doc/logo.png)

Words matter. In a world where gender inequality persists despite decades of progress, BiaSight addresses one of the
most pervasive yet often overlooked aspects of discrimination: the language we use in our digital spaces. BiaSight uses
the power of Google's cutting-edge AI, including Gemini, to analyze and improve the inclusivity of online content.

While content creators and website authors often focus on performance, usability, and visual appeal, the impact of words
on discrimination against women and girls and how this impacts equality is frequently underestimated. BiaSight aims to
change this by providing an intuitive, AI-driven analysis of web content across various equality categories, much like
how Google PageSpeed Insights has become an indispensable tool for web performance optimization.

The vision of BiaSight is to make gender-inclusive language as integral to web development as responsive design or SEO
optimization and to inspire creators for change.

Remember, words matter. They shape perceptions, influence behaviors, and can either reinforce or challenge the gender
inequalities that persist in our society.

**Try it yourself**: [biasight.com](https://biasight.com/)

This project was created as part of the [She Builds AI Hackathon 2024](https://womentechmakers.devpost.com/).

![mockup](doc/mockup.png)

---

## Backend

The BiaSight backend is a powerful engine built with FastAPI and Python. It leverages BeautifulSoup to extract readable
content from web pages, preparing it for analysis. Using Jinja templating, prompt generation is modularized, allowing
seamless integration of web content into advanced prompts for Google’s Gemini LLM.

To ensure both accurate and deterministic results, Gemini is configured to use JSON mode for structured output and a
low-temperature setting is applied to minimize variability in its generation. Pydantic ensures robust data modeling and
validation, while Poetry manages dependencies efficiently. Docker streamlines deployment, and Ruff, combined with
GitHub Actions, maintains high code quality through automated testing and linting.

For optimal performance and user experience, the backend employs a TTLCache, reducing analysis time by caching recent
results. This architecture fosters easy and secure extensibility, allowing for future enhancements and integrations as
BiaSight continues to evolve.

## Frontend

The frontend is powered by Vue 3 and Vite, supported by daisyUI and Tailwind CSS for efficient frontend development.
Together, these tools provide users with a sleek and modern interface for seamless interaction with the backend.

![architecture](doc/architecture.png)

This is the backend part of the project. **Frontend**: [biasight-ui](https://github.com/vojay-dev/biasight-ui)

---


## Tech stack

- Python 3.12 + [FastAPI](https://fastapi.tiangolo.com/) API development
- [Jinja](https://jinja.palletsprojects.com/) templating for modular prompt generation
- [Pydantic](https://docs.pydantic.dev/latest/) for data modeling and validation
- [Poetry](https://python-poetry.org/) for dependency management
- [Docker](https://www.docker.com/) for deployment
- [Gemini](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini) via [VertexAI](https://cloud.google.com/vertex-ai) for evaluating web content
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for extracting content from web pages
- [Ruff](https://docs.astral.sh/ruff/) as linter and code formatter together with [pre-commit](https://pre-commit.com/) hooks
- [Github Actions](https://github.com/features/actions) to automatically run tests and linter on every push

## Makefile

The project includes a `Makefile` with common tasks like setting up the virtual environment with Poetry, running the
service locally and within Docker, running test, linter and more. Simply run:
```sh
make help
```
to get an overview of all available tasks.

![make help](doc/make-help.png)

## Configuration

**Prerequisite**

- GCP project with VertexAI API enabled and access to Gemini (recommended: `gemini-1.5-flash-002` or `gemini-1.5-pro-002`)
- JSON credentials file for GCP Service Account with VertexAI permissions

The API is configured via environment variables. If a `.env` file is present in the project root, it will be loaded
automatically. You can copy the `.env.dist` file from the repository as a basis.

The following variables must be set:

- `GCP_PROJECT_ID`: The ID of the Google Cloud Platform (GCP) project used for VertexAI and Gemini.
- `GCP_LOCATION`: The location used for prediction processes.
- `GCP_SERVICE_ACCOUNT_FILE`: The path to the service account file used for authentication with GCP.

**Gemini model**

The default model used for Gemini is `gemini-1.5-flash-002`. To use a different model, simply adjust the `GCP_GEMINI_MODEL`
config in the `.env` file. For this use-case, the Flash model delivers good and cost-efficient results.

## Project setup

**(Optional) Configure poetry to use in-project virtualenvs**:
```sh
poetry config virtualenvs.in-project true
```

**Install dependencies**:
```sh
poetry install
```

**Run**:

*Please check the Configuration section to ensure all requirements are met.*
```sh
curl -s -X POST localhost:8000/analyze \
  -H 'Content-Type: application/json' \
  -d '{"uri": "https://womentechmakers.devpost.com/"}' | jq .
```

![example](doc/example.png)

## Docker

All Docker commands are also encapsulated in the `Makefile` for convenience.

### Build

```sh
docker build -t biasight .
```

### Run

```sh
docker run -d --rm --name biasight -p 9091:9091 biasight
curl -s -X POST localhost:9091/analyze \
  -H 'Content-Type: application/json' \
  -d '{"uri": "https://womentechmakers.devpost.com/"}' | jq .
docker stop biasight
```

### Save image for deployment

```sh
docker save biasight:latest | gzip > biasight_latest.tar.gz
```

## Gemini interaction

Gemini interaction is encapsulated in the `GeminiClient` class. To ensure a high quality of prompt responses and to
avoid unnecessary parsing issues. The `GeminiClient` class uses the Gemini JSON format mode.

See: [https://ai.google.dev/gemini-api/docs/structured-output?lang=python](https://ai.google.dev/gemini-api/docs/structured-output?lang=python)

This ensures Gemini replies with valid JSON, whereas the schema is attached to the individual prompt, for example:
```
Return your analysis in this JSON format:

{
  "summary": str,
  "stereotyping_feedback": str,
  "stereotyping_score": int,
  "stereotyping_example": str,
  "representation_feedback": str,
  "representation_score": int,
  "representation_example": str,
  "language_feedback": str,
  "language_score": int,
  "language_example": str,
  "framing_feedback": str,
  "framing_score": int,
  "framing_example": str,
  "positive_aspects": str,
  "improvement_suggestions": str,
  "male_to_female_mention_ratio": float,
  "gender_neutral_language_percentage": float
}
```

This approach is then combined with Pydantic models to ensure the correctness of datatypes and the overall structure:
```py
    def analyze(self, text: str) -> AnalyzeResult:
        prompt = self._render_template(text)
        chat: ChatSession = self.gemini_client.start_chat()
        chat_response: str = self.gemini_client.get_chat_response(chat, prompt)

        analyze_result = AnalyzeResult.model_validate(from_json(chat_response))

        # overall score is calculated via Python instead of using the LLM to ensure deterministic results
        analyze_result.overall_score = self._calculate_score(analyze_result)

        return analyze_result
```

This is a great example how to programmatically interact with Gemini, ensure the quality of the responses and use a LLM
to cover core business logic.

## Score calculation

As a first step, a score is assigned by Gemini for each of the four bias categories: stereotyping, representation,
language, and framing. The overall score is then calculated using the average of the four categories.

Then, two additional factors are applied:

* **Ratio Boost**: A bonus is added to the base score based on the male-to-female mention ratio. The closer the ratio is  
  to 1 (meaning equal mentions), the higher the bonus, with a maximum boost of 30% when the ratio is exactly 1.
* **Neutral Language Boost**: A bonus is added based on the percentage of gender-neutral language used in the text. The
  higher the percentage of gender-neutral language, the higher the bonus, with a maximum boost of 10% when the language
  is 100% gender-neutral.

These boosts aim to acknowledge and reward content with a more balanced gender representation and inclusive language.

The final overall score is then capped between 1 (extremely biased) and 100 (completely free of bias), providing a
comprehensive evaluation of the content's inclusivity.

$$
\begin{align*}
\text{Base Score} &= \frac{Stereotyping Score + Representation Score + Language Score + Framing Score}{4} \\
\\
\text{Ratio Boost} &= \begin{cases}
30 \times (1 - |1 - Male To Female Mention Ratio|) & \text{if } Male To Female Mention Ratio > 0 \\
0 & \text{if } Male To Female Mention Ratio = 0
\end{cases} \\
\\
\text{Neutral Language Boost} &= \frac{Gender Neutral Language Percentage}{100} \times 10 \\
\\
\text{Boosted Score} &= \text{Base Score} \times \left( 1 + \frac{\text{Ratio Boost}}{100} + \frac{\text{Neutral Language Boost}}{100} \right) \\
\\
\text{Final Score} &= \text{round}(\text{max}(1, \text{min}(100, \text{Boosted Score})))
\end{align*}
$$

## Example

```sh
curl -s -X POST localhost:8000/analyze \
  -H 'Content-Type: application/json' \
  -d '{"uri": "https://womentechmakers.devpost.com/"}' | jq .
```

```json
{
  "uri": "https://womentechmakers.devpost.com/",
  "result": {
    "summary": "The webpage shows a strong commitment to gender equality through its focus on a hackathon addressing UN SDG 5.  However, while the language used is largely inclusive, the high number of mentions related to women and girls compared to men could be perceived as unbalanced.  Further improvements could enhance the overall inclusivity.",
    "overall_score": 96,
    "stereotyping_feedback": "The webpage avoids reinforcing traditional gender stereotypes. The focus is on addressing gender inequality, not perpetuating it.",
    "stereotyping_score": 95,
    "stereotyping_example": "The hackathon's theme directly challenges gender inequality by focusing on UN SDG 5.",
    "representation_feedback": "While the hackathon aims for inclusivity, the overwhelming focus on women and girls in the description might inadvertently overshadow the participation of other genders.",
    "representation_score": 75,
    "representation_example": "The repeated emphasis on \"women and girls\" in the description and prize categories.",
    "language_feedback": "The language used is largely gender-neutral and inclusive, using terms like \"participants\" instead of gendered terms. However, the frequent mention of \"women and girls\" could be balanced.",
    "language_score": 85,
    "language_example": "The use of \"participants\" instead of gender-specific terms like \"participants\" and the explicit statement that the hackathon is open to all genders.",
    "framing_feedback": "The framing of the hackathon positively promotes gender equality and empowerment.  There is no victim-blaming or minimization of women's experiences.",
    "framing_score": 90,
    "framing_example": "The hackathon's focus on UN SDG 5 and its emphasis on addressing real-world challenges faced by women and girls.",
    "positive_aspects": "The webpage's clear commitment to gender equality through its focus on a hackathon addressing UN SDG 5 is commendable. The use of inclusive language and the explicit statement welcoming participants of all genders are positive steps.",
    "improvement_suggestions": "1. Balance the focus on women and girls with more inclusive language that acknowledges the participation and contributions of all genders. 2.  Highlight success stories and contributions from participants of all genders in promotional materials. 3.  Ensure that judging criteria are equally applicable and unbiased towards all participants regardless of gender.",
    "male_to_female_mention_ratio": 0.1,
    "gender_neutral_language_percentage": 80.0
  }
}
```

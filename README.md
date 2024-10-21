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

## Example

```shell
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

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
    "summary": "The text demonstrates a strong commitment to gender equality and empowering women in tech. However, there are areas for improvement in terms of language and representation. While the hackathon is explicitly open to all genders, the focus on \"Women Techmakers\" and \"She Builds AI\" might inadvertently exclude men from participating.",
    "overall_score": 100,
    "stereotyping_feedback": "The text avoids reinforcing traditional gender stereotypes. It emphasizes the importance of gender equality and encourages participants to address real-world challenges faced by women and girls.",
    "stereotyping_score": 90,
    "stereotyping_example": "The hackathon's mission statement emphasizes the importance of addressing gender equity challenges and empowering women and girls.",
    "representation_feedback": "While the hackathon is open to all genders, the focus on \"Women Techmakers\" and \"She Builds AI\" might inadvertently exclude men from participating. The text could benefit from more inclusive language that acknowledges the contributions of all genders.",
    "representation_score": 75,
    "representation_example": "The hackathon is titled \"She Builds AI\" and is presented as a \"Women Techmakers\" initiative.",
    "language_feedback": "The text uses gender-neutral language for the most part, but there are instances where it could be more inclusive. For example, using \"participants\" instead of \"women\" when referring to the target audience.",
    "language_score": 85,
    "language_example": "The text uses phrases like \"women and girls\" and \"gender equity challenges\" which could be replaced with more inclusive language like \"individuals\" or \"equity challenges.\"",
    "framing_feedback": "The text frames gender-related issues in a positive and empowering way, highlighting the importance of addressing gender inequality and promoting women's leadership in STEM. It avoids victim-blaming or minimizing the experiences of women.",
    "framing_score": 95,
    "framing_example": "The hackathon encourages participants to \"harness the power of AI to build a more equitable future!\" and emphasizes the importance of addressing UN Sustainable Development Goal 5.",
    "positive_aspects": "The text explicitly states that the hackathon is open to participants of all genders and emphasizes the importance of gender equality and empowering women in tech. It also highlights the use of Google AI tools and technologies to address real-world challenges.",
    "improvement_suggestions": "Consider using more inclusive language that acknowledges the contributions of all genders. For example, instead of \"Women Techmakers,\" use \"Techmakers\" or \"Tech Leaders.\"  Also, consider using gender-neutral language when referring to participants, such as \"individuals\" or \"hackathoners.\" ",
    "male_to_female_mention_ratio": 1.5,
    "gender_neutral_language_percentage": 80.0
  }
}
```

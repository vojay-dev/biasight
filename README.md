# BiaSight - Gender Bias Detection on Websites using AI

Project for the She Builds AI Hackathon: https://womentechmakers.devpost.com/

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

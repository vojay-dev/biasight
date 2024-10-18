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
  "uri": "https://www.rbb24.de/panorama/beitrag/2024/10/berlin-biden-besuch-freitag-sperrungen-sbahn-bahn.html",
  "result": {
    "stereotyping_feedback": "The text does not explicitly reinforce gender stereotypes. However, it focuses heavily on the security measures surrounding Biden's visit, which could be interpreted as reinforcing the stereotype of men as powerful and needing protection, while women are largely absent from the narrative.",
    "stereotyping_score": 3,
    "representation_feedback": "The text heavily focuses on male figures, particularly Biden and other political leaders. Women are primarily mentioned as victims of violence or as participants in the public discourse through comments. There's a lack of diverse perspectives and experiences from women, particularly in relation to the security measures and their impact.",
    "representation_score": 2,
    "language_feedback": "The language used is generally neutral, with no obvious instances of gendered language or loaded language. However, the text refers to \"Passant\" (passerby) in the context of a man disrupting a live broadcast, which could be interpreted as implicitly gendering the perpetrator.",
    "language_score": 4,
    "framing_feedback": "The text frames the security measures surrounding Biden's visit as necessary and justified due to his high security status. This framing reinforces the existing power structures and potentially minimizes the inconvenience and disruption experienced by residents and commuters. There's no mention of the impact on women specifically, potentially reinforcing the idea that their experiences are less important.",
    "framing_score": 3,
    "overall_score": 3
  }
}
```

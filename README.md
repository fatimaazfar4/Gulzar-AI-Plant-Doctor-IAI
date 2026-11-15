# Gulzar-AI Plant Doctor

Gulzar-AI is a Streamlit-based plant-care decision-support app for Pakistani
home gardens. It helps a gardener connect visible plant symptoms and growing
conditions with possible causes, then offers practical treatment and
prevention suggestions.

The app is a transparent, rule-based expert system. It does not use a trained
machine-learning model, image recognition, or an external AI service. Its
recommendations come from the facts entered in the form and the rules written
in the project's knowledge base.

## What the app does

1. The user selects a plant and describes its symptoms and growing conditions.
2. The app translates those answers into internal facts such as
   `plant_tomato`, `yellow_lower`, or `soil_soggy`.
3. The inference engine checks those facts against the knowledge-base rules.
4. Matching rules produce possible diagnoses and supporting evidence.
5. Evidence for the same diagnosis is combined into a certainty-factor score,
   and diagnoses are sorted from highest to lowest score.
6. The app displays up to five results with an explanation, urgency, treatment
   steps, and a prevention tip.

If none of the rules match the submitted facts, the app explains that there is
not enough evidence for a specific diagnosis and suggests adding symptoms.

## What you can enter

The plant choice is required. Other dropdowns include a **Not sure / skip**
option, and symptom and extra-condition checklists can be left empty.

- **Plant and place:** one of 10 supported plants, whether it is in a pot or
  the ground, and whether it is indoors, on a balcony, or on a rooftop.
- **Symptoms:** leaf colour and damage, whole-plant changes, stem or root
  signs, and visible pests.
- **Care and soil:** watering frequency, drainage, soil feel, fertilizer
  history, and whether the pot is too small.
- **Environment:** season, humidity, airflow, water source, approximate hours
  of direct sun, and approximate daytime temperature.
- **Extra conditions:** issues such as water pooling, compacted soil, leaves
  staying wet overnight, AC or fan drafts, recent heavy rain, and sea breeze.

Sun and temperature are entered with sliders. Their values are converted to
threshold facts: sun below 3 hours or at least 6 hours, and temperature at
least 28, 35, 38, or 40 °C, or at most 10 °C.

## Supported plants and topics

The knowledge base includes money plant, mint (pudina), rose (gulab), hibiscus
(gudhal), curry leaf (kari patta), chili (mirch), tomato (tamatar), lemon
(nimbu), aloe vera, and tulsi.

Possible findings are grouped into watering, nutrients, fungal or bacterial
disease, pests, environment, soil and pot, Karachi and seasonal conditions,
and plant-specific issues. Examples include overwatering, nutrient
deficiencies, powdery mildew, aphids, heat stress, poor drainage, sea-breeze
salt damage, and monsoon root stress. The precise diagnoses available are
defined in `DIAGNOSES` in `knowledge_base.py`.

## How the reasoning works

Gulzar-AI uses forward chaining: it starts with the user's input facts and
repeatedly checks rules until no more rules can fire.

Each rule can require:

- `if_all`: every listed fact must be present.
- `if_any`: at least one listed fact must be present, when this condition is
  specified.
- `if_none`: none of the listed facts may be present.

There are two kinds of rules:

- **Derived-fact rules** add an intermediate fact to working memory. For
  example, high humidity or monsoon season can imply `humid_air`.
- **Diagnosis rules** add evidence for a diagnosis. A diagnosis fact can also
  be used by a later rule, allowing chained reasoning.

The knowledge base currently contains 11 derived-fact rules and 66 diagnosis
rules. A rule fires at most once in an inference run. Rules are checked in
their listed order, and additional passes allow newly derived facts or
diagnoses to activate rules that were checked earlier.

Each matching diagnosis rule contributes a **certainty factor (CF)**. When
more than one rule supports the same diagnosis, the engine combines their
positive evidence using:

```text
combined CF = old CF + new CF * (1 - old CF)
```

The UI shows the result as a percentage and labels it **Very likely** at CF
0.85 or higher, **Likely** at 0.70 or higher, and **Possible** below 0.70.
These scores are rule-based indicators of how strongly the entered facts
match the rules. They are **not medical or botanical probabilities**, and
they do not guarantee that a diagnosis is correct.

The **How did Gulzar-AI reach this result?** section shows how many inference
cycles and rules were involved and lists the rule descriptions and CF values
supporting each displayed diagnosis.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit page, styling, input form, session result handling, and diagnosis/treatment display. |
| `engine.py` | Converts form answers to facts, performs forward chaining, combines certainty factors, and records the explanation trace. Also contains command-line demonstration cases. |
| `knowledge_base.py` | Supported plants, form choices, symptom and condition labels, diagnosis names, and all inference rules. |
| `treatments.py` | Summary, urgency, ordered treatment steps, and prevention advice for diagnoses. |
| `requirements.txt` | Python package requirements. |
| `README.md` | Project overview, instructions, and documentation. |

## Run locally

### Requirements

- Python 3.10 or later
- `pip`

### Install and start

From the project directory, run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit will print a local URL in the terminal; open it in a browser to use
the app. The only listed Python dependency is Streamlit (`>=1.32,<2.0`).

### Run the inference-engine demo

The engine includes three sample cases that print the knowledge-base
statistics, matching diagnoses, and rule IDs:

```powershell
python engine.py
```

## Deploy with Streamlit Community Cloud

1. Push the project to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and connect
   the GitHub repository.
3. Create an app using the desired branch and set the main file to `app.py`.
4. Deploy. Streamlit Community Cloud installs the requirements and starts the
   app.

The app does not currently require API keys, Streamlit secrets, or a database.
Do not commit passwords, tokens, or other credentials to the repository.

## Important limitations

- This is an educational decision-support tool, not a laboratory diagnosis or
  a substitute for advice from a qualified local agricultural expert.
- Results depend on the accuracy and completeness of the selected facts.
  Similar symptoms can have different causes, and the rule set does not cover
  every plant variety, disease, pest, or local growing condition.
- The displayed certainty factor is based on the rules; it is not a
  statistically calibrated probability.
- Treatment suggestions are general guidance. Check product labels and local
  expert advice before applying fertilizers, sprays, or other treatments,
  especially to edible plants.

For serious, rapidly spreading, or persistent plant problems, consult a local
agricultural expert.

## Contributor

- [Fatima Azfar](https://github.com/fatimaazfar4)

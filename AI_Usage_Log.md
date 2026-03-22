# AI Usage Log

## 1. AI Tools Used
- **Tools:** ChatGPT, Claude AI, Cloud AI
- **Purpose:** Support during development, code organization, feature implementation, debugging, validation of ideas, visualization design, documentation formatting, and deployment support

---

## 2. Purpose of AI Usage
AI was used to assist in:

- debugging Python, notebook, ETL, and Streamlit code
- organizing and cleaning notebook import cells
- checking available tickers and retrieving index level values by ticker
- creating data exploration views for raw company data and processed ETL data
- validating the proposed ETL dataset structure and selected features
- helping build evaluation functions for model outputs
- suggesting hyperparameter search grids for Gradient Boosting Classification
- generating visualization ideas and repetitive plotting code
- identifying which notebook cells were relevant to convert into Python scripts
- understanding how to use `joblib` to save trained models
- understanding how to use environment variables with `getenv` to avoid hardcoding API keys
- designing and improving Streamlit user interface and app structure
- implementing data transformations and API integration logic
- assisting with deployment troubleshooting in Streamlit Cloud
- helping format this AI usage log in markdown based on our spoken explanation and project review

---

## 3. Specific Tasks Where AI Was Used

## Part 1. ETL, Data Processing, Exploration, and Model Training

### A. Code Cleanup and Organization
AI helped reorganize a large imports cell in the notebook into a cleaner and more readable format, with comments explaining the purpose of different imports.

---

### B. Data Access and Ticker Handling
AI was used to clarify how to inspect available tickers and how to retrieve index level values by ticker when we were stuck on that part.

---

### C. Data Exploration
AI helped generate parts of the exploration functions for:
- raw company data
- processed ETL data

This included creating visualizations that made it easier to understand the structure and quality of the data before modeling.

---

### D. ETL Dataset Design Validation
We discussed the ETL dataset design with the professor and then used AI to confirm that our intended features were appropriate. These included:
- open
- close
- volume
- daily change percentage
- target value definition

AI did not fully generate this part, but it helped confirm that the approach made sense.

---

### E. Model Evaluation Functions
AI assisted in generating parts of the functions used to evaluate model outputs, especially for producing cleaner and more informative visualizations.

---

### F. Hyperparameter Tuning
AI suggested a parameter grid for Gradient Boosting Classification after we noticed the baseline performance was not very good. We then implemented that grid into our own tuning functions to search for better parameters.

---

### G. Visualization Support
AI helped generate some of the repetitive code for model comparison plots and output visualizations. This was especially useful for producing cleaner charts more efficiently.

---

### H. Notebook-to-Script Conversion
AI helped us identify which notebook cells were relevant to convert into standalone Python scripts. As a result, we prepared:
- an ETL Python script
- a generator Python script

---

### I. Model Serialization
AI helped us understand how to use the `joblib` library to save trained models, since we had not used it before.

---

### J. API Key Security
AI explained how to use `getenv` and environment files to avoid hardcoding API keys. We implemented this manually, but AI helped clarify what files were needed and how to structure them safely.

---

### K. AI Log Formatting
ChatGPT also helped us generate the format of this AI usage log. We reviewed the project progress, the code, and the different ways AI had been used throughout development, and then explained it by voice using speech recognition. Based on that explanation and the markdown structure we needed, ChatGPT helped translate our thoughts and spoken description into this `.md` format.

---

## Part 2. Streamlit App, Inference Flow, and Deployment

### A. Debugging and Error Fixes
AI helped identify and resolve issues such as:
- incorrect function arguments
- undefined variables
- incorrect model loading logic
- Streamlit deployment errors
- file path issues with images

It was also useful whenever we copied error messages directly into the AI tool, since it helped explain what the error meant, what part of the code caused it, and what next steps to take to avoid the same issue the next time we ran the code.

---

### B. Code Implementation
AI provided guidance and example code for:
- integrating the SimFin API wrapper
- building the watchlist page
- implementing multi-model selection based on ticker
- structuring the ETL pipeline for inference
- adding moving averages to charts
- implementing chart switching between line and candlestick views
- creating recommendation logic and UI components

---

### C. UI/UX Improvements
AI assisted with:
- restructuring page layouts for better usability
- organizing components such as metrics, charts, and controls
- improving chart readability
- creating a more consistent design across pages
- designing the team page layout with images

---

### D. Feature Design
AI helped design:
- recommendation interpretation logic
- recent trading patterns section
- watchlist filtering and snapshot logic
- timeframe selection system
- visual recommendation chart

---

## 4. What Worked Well

AI worked well when we ran into coding errors, because we could copy the error message and get help understanding what we were looking at, why the problem happened, and what steps to take next so that the error could be avoided in future runs.

It also worked well when we needed to understand new libraries, tools, or functions that we had not used before. This was especially useful with things like `joblib`, environment variables, and some implementation details that were new to us.

Another thing that worked well was using AI for repetitive tasks. When we already understood the idea behind what we wanted to build, but the code involved writing very similar structures again and again, AI helped save time and made the workflow more efficient.

It was also helpful when we got stuck on logic, implementation details, or understanding what was actually being asked of us in the project. In those moments, AI worked well as a very helpful support tool for bouncing ideas, clarifying expectations, and helping us move forward.

---

## 5. What Did Not Work Well

Sometimes the AI hallucinated or focused on problems that we had already solved, and it would continue suggesting fixes for issues that were no longer relevant.

Sometimes it also overcomplicated things and did not give the easiest or most practical solution until the prompt was made very explicit.

Another limitation was that AI-generated code sometimes looked correct at first but still needed careful testing, because it could miss project-specific context, assumptions, or dependencies between different parts of the system.

---

## 6. What We Learned

We learned that AI can be very useful as another teammate, but it cannot do the thinking for the whole project. It may help generate a notebook cell, a script, or a useful suggestion, but in a project with many connected parts, the team still needs to understand what is happening, why it is happening, and how each part connects to the others.

We also learned that AI is especially useful when we are stuck, debugging, learning something new, or trying to speed up repetitive work. It can reduce the time spent blocked on a problem and make development much more efficient.

At the same time, we learned that AI cannot be trusted blindly. Its outputs need to be reviewed, tested, and adapted. Human understanding is still necessary to make sure the full project remains coherent and correct.

Compared with older workflows where debugging often meant searching through forums such as Stack Overflow for a long time, using LLMs made the process much faster and more interactive. That said, the final understanding and responsibility still had to come from us.

---

## 7. Final Responsibility Statement
All AI-generated suggestions were reviewed, tested, and adapted by the team before being included in the project. AI was used as a support tool to improve efficiency, organization, debugging, and development workflow, while final responsibility for all code, design decisions, and implementation choices remained with the team.
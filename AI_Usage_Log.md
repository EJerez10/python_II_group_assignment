# AI Usage Log

## 1. AI Tool Used
- **Tool:** ChatGPT (OpenAI)
- **Version:** GPT-5.3 (via ChatGPT interface)

---

## 2. Purpose of AI Usage
AI was used to assist in:

- Debugging Python and Streamlit code  
- Designing and improving user interface (UI/UX) layout  
- Structuring the multi-page Streamlit application  
- Implementing data transformations and API integration logic  
- Improving readability and organization of code  
- Generating example code snippets for features such as:
  - watchlist functionality  
  - moving average overlays  
  - recommendation visualization  
- Assisting with deployment troubleshooting (Streamlit Cloud)

---

## 3. Specific Tasks Where AI Was Used

### A. Debugging & Error Fixes
AI helped identify and resolve issues such as:
- incorrect function arguments (e.g., `live_inference`)
- undefined variables (e.g., `rows_before`)
- incorrect model loading logic
- Streamlit deployment errors
- file path issues with images

---

### B. Code Implementation
AI provided guidance and example code for:
- integrating the SimFin API wrapper  
- building the watchlist page  
- implementing multi-model selection based on ticker  
- structuring the ETL pipeline for inference  
- adding moving averages to charts  
- implementing chart switching (line vs candlestick)  
- creating recommendation logic and UI components  

---

### C. UI/UX Improvements
AI assisted with:
- restructuring page layouts for better usability  
- organizing components (metrics, charts, controls)  
- improving chart readability (color schemes, overlays)  
- creating consistent design across pages  
- designing the team page layout with images  

---

### D. Feature Design
AI helped design:
- recommendation interpretation logic  
- recent trading patterns section  
- watchlist filtering and snapshot logic  
- timeframe selection system  
- visual recommendation chart (shaded signal zone)  

---

## 4. Level of Modification
All AI-generated code was:
- reviewed and tested manually  
- modified to fit project requirements  
- adapted to integrate with teammate contributions  
- adjusted to match UI/UX feedback from team members  

---

## 5. Limitations & Critical Thinking
The AI-generated suggestions were not used blindly. The following considerations were applied:

- verifying compatibility with SimFin data availability  
- adjusting logic to handle missing or outdated data  
- ensuring correct integration with the machine learning pipeline  
- refining UI decisions based on team feedback  

---

## 6. Final Responsibility Statement
All final code, design decisions, and implementation choices were reviewed, modified, and approved by the project team.  
AI was used as a support tool, not as a replacement for understanding or development.
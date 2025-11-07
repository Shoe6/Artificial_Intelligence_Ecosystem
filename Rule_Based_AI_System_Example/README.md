# Submission for the Building a Rule-Based AI System in Python project.

---

## Part 1: Initial Project Ideas

### 1. Project Idea 1: Simple Expert System for Medical Diagnosis
- **Description:** The system takes a user's symptoms and, based on a set of logical rules, suggests a possible condition. 
- **Rule-Based Approach:**  
  - IF temperature is **ABOVE 103**AND**mental_state` is CONFUSED THEN SUGGEST: "ER Visit: Possible Septic Shock or Meningitis." ACTION: Recommend immediate emergency medical attention. 
  - IF headache is SEVERE AND nausea is PRESENT AND vision is BLURRY THEN SUGGEST: "Severe Migraine with Aura." ACTION: Recommend immediate rest and dark environment.
### 2. Project Idea 2: Simple Chatbot
- **Description:** This system uses keyword matching and context to route the user's query to the correct canned response or action. Rules are prioritized from most specific to most general.
- **Rule-Based Approach:**  
  - IF input CONTAINS ("cancel" OR "refund") AND input CONTAINS ("order" OR "purchase") THEN RESPONSE: "I see you need help with an order. Please provide your order number to check eligibility for cancellation/refund." 
  - IF input CONTAINS ("password" OR "login" OR "account") THEN RESPONSE: "To secure your account, I'll send you a password reset link. Please check your email."
### 3. Basic E-commerce Recommendation Engine
- **Description:** Recommend items based on a user's current item, purchase history, or pre-defined relationships between products.
- **Rule-Based Approach:**  
  - IF current_item IS "Coffee Machine" THEN recommend "Coffee Beans" and "Milk Frother". 
  - IF user_history includes "Running Shoes" AND last_purchase IS within 30 days THEN recommend "Athletic Socks".
  - IF cart_value > $100 THEN recommend "Free Shipping Upgrade".

### **Chosen Idea:** Basic E-commerce Recommendation Engine
**Justification:** This system doesn't use complex collaborative filtering but instead relies on simple business logic and product attributes. It is also helpful whether your looking to buy something for personal reasons or for reselling.

---

## Part 2: Rules/Logic for the Chosen System

The **E-Commerce Recommender** system will follow these rules:

1. **Financial Heuristics (Arbitrage):**  
   - **IF** profit_potential of current_item_id is greater than $30.00 → **Display FINANCIAL ACTION message detailing the estimated profit..**

2. **Cross-Selling and Complementarity:**  
   - **IF** current_item_id is 'P101' (Digital Camera 50MP) → **Recommend 'P102' (Lens Cap) and 'P103' (Camera Bag)**  
   - **IF** current_item_id is 'P201' (Coffee Maker 12-Cup) → **Recommend 'P202' (Coffee Filters Subscription)**
   - **IF** current_item_id is 'P401' (Hiking Boots) → **Recommend 'P402' (Wool Hiking Socks)**

3. **Business and Promotional Logic:**  
   - **IF** user_cart_value is greater than or equal to $100.00 → **Display BUSINESS ACTION message: "You qualify for Free Premium Shipping!"**
   - **IF** ELSE IF current_item_id has tag 'clearance' → **Recommend all items in the clearance_items list (P302, P402)**

4. **Re-engagement:**  
   - **IF** last_purchase_days in user_history is greater than 90 days → **Recommend all items in the bestsellers list (P301, P101, P501)**


---

## Part 3: Rules/Logic for the Chosen System

=====================================================
 BASIC RULE-BASED E-COMMERCE AI SYSTEM
=====================================================
Available Products for testing:
- P101: Digital Camera 50MP (Cat: Electronics)
- P102: Camera Lens Cap (Cat: Accessories)
- P103: Leather Camera Bag (Cat: Accessories)
- P201: Coffee Maker 12-Cup (Cat: HomeGoods)
- P202: Subscription: Coffee Filters (Cat: HomeGoods)
- P301: Ergonomic Desk Chair (Cat: Office)
- P302: Bamboo Desk Mat (Cat: Office)
- P401: Hiking Boots - Summit (Cat: Apparel)
- P402: Wool Hiking Socks (Cat: Apparel)
- P501: Limited Edition Watch (Cat: Luxury)
=====================================================

Enter the Product ID you are viewing (e.g., P101, P501), or type 'quit': p101
Enter your current Cart Value (e.g., 55.00): $20
Days since your last purchase (e.g., 120): 7

--- Running Inference Engine for Item: P101 ---
Rule D1 Triggered: Arbitrage heuristic found high profit potential.
Rule A Triggered: Direct cross-sell rule found.

[RECOMMENDATION RESULTS]
-> FINANCIAL ACTION: High-Value Resale Opportunity for Digital Camera 50MP! Estimated Potential Profit: $45.00
-> Camera Lens Cap
-> Leather Camera Bag

=====================================================

## Part 4: Reflection

### How the Rule-Based System Works:
The implemented rule-based recommendation engine functions as a classic expert system, or knowledge-based AI. Its core architecture is separated into two parts: the Knowledge Base and the Inference Engine.

Knowledge Base: This is the static set of IF-THEN rules and associated product data (like profit_potential and tags). These rules encode explicit human and business expertise, such as "People who buy a coffee maker need filters" (Cross-Selling) or "We need to clear out items tagged 'clearance'" (Business Logic).

Inference Engine: This Python function (get_product_recommendations) acts as the decision-maker. It takes user inputs (e.g., the current item, cart value, and days since the last purchase) and systematically checks them against the rules in a prioritized order. The use of strict if-elif statements is crucial, as it determines which rules fire and in what sequence. For instance, the system always checks for a high-profit Arbitrage Opportunity (Rule D1) before checking for a lower-priority Clearance Push (Rule B2). The system is entirely deterministic: the same input will always yield the same recommendations, demonstrating the transparency and predictability that characterized pre-machine learning AI.

### Challenges Encountered with AI Assistance:
The primary challenge encountered while prompting the AI (Gemini) for assistance involved reconciling the generative nature of the LLM with the deterministic requirements of a rule-based system.

Generative models prefer flexibility and explanation, whereas an expert system demands rigid structure. Initially, the challenge was ensuring the AI delivered a system that was not just functional but also a perfect example of a rule-based design. This required specific prompting to:
- **Enforce Determinism:**  
The AI needed to clearly separate the data (Knowledge Base) from the logic (Inference Engine) and rely only on hard-coded if-elif-else statements, avoiding any internal randomness or complex machine learning libraries.
- **Define Priority:**  
  The AI had to be prompted to define and maintain a clear order of rule execution (e.g., ensuring Promotional Rule B1 fires before B2).
- **Produce Structured Output:**
The request for the rule sets in plain, copy-and-paste text format required several iterations to ensure the final output was a clean, organized table suitable for formal documentation rather than conversational text or code snippets.

The collaboration successfully resulted in a system that meets the assignment requirements while highlighting the architectural difference between modern, statistical AI and traditional, knowledge-based AI.














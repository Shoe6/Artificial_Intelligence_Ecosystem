# The Knowledge Base (KNOWLEDGE_BASE) defines the rules of the system.
# It is a dictionary where the keys are the target item/condition, and the value
# is a list of recommended items/actions.

# --- 1. MOCK DATA (Updated with 'profit_potential') ---
PRODUCTS = {
    # Added 'profit_potential' to P101, P302, and introduced P501.
    'P101': {'name': 'Digital Camera 50MP', 'category': 'Electronics', 'brand': 'Apex', 'tags': ['high-res'], 'profit_potential': 45.00},
    'P102': {'name': 'Camera Lens Cap', 'category': 'Accessories', 'brand': 'Apex', 'tags': ['accessory'], 'profit_potential': 5.00},
    'P103': {'name': 'Leather Camera Bag', 'category': 'Accessories', 'brand': 'Generic', 'tags': ['accessory'], 'profit_potential': 15.00},
    'P201': {'name': 'Coffee Maker 12-Cup', 'category': 'HomeGoods', 'brand': 'BrewMaster', 'tags': ['kitchen'], 'profit_potential': 8.00},
    'P202': {'name': 'Subscription: Coffee Filters', 'category': 'HomeGoods', 'brand': 'BrewMaster', 'tags': ['subscription'], 'profit_potential': 2.00},
    'P301': {'name': 'Ergonomic Desk Chair', 'category': 'Office', 'brand': 'ErgoMax', 'tags': ['bestseller'], 'profit_potential': 25.00},
    'P302': {'name': 'Bamboo Desk Mat', 'category': 'Office', 'brand': 'Eco-Brand X', 'tags': ['clearance'], 'profit_potential': 10.00},
    'P401': {'name': 'Hiking Boots - Summit', 'category': 'Apparel', 'brand': 'TrailBlaze', 'tags': ['winter'], 'profit_potential': 18.00},
    'P402': {'name': 'Wool Hiking Socks', 'category': 'Apparel', 'brand': 'TrailBlaze', 'tags': ['accessory'], 'profit_potential': 4.00},
    'P501': {'name': 'Limited Edition Watch', 'category': 'Luxury', 'brand': 'Timeless', 'tags': ['rare'], 'profit_potential': 60.00}, # NEW Product with High Resale Value
}

# --- 2. THE KNOWLEDGE BASE (RULES) ---
# Rules structure remains the same, but the logic now uses the new 'profit_potential' data.

KNOWLEDGE_BASE = {
    # Category A: Cross-Selling and Complementarity (Highest Priority)
    'P101': ['P102', 'P103'], 
    'P201': ['P202'],         
    'P401': ['P402'],         
    
    # Category B: Business Logic (Medium Priority - Check tags)
    'clearance_items': ['P302', 'P402'], 
    'bestsellers': ['P301', 'P101', 'P501'], 
}

# --- 3. THE INFERENCE ENGINE ---

def get_product_recommendations(current_item_id, user_cart_value, user_history=None):
    """
    Applies IF-THEN rules based on input data to generate recommendations.
    This function is the core rule-based AI engine.
    
    Args:
        current_item_id (str): The ID of the item the user is currently viewing.
        user_cart_value (float): The current total value of the user's shopping cart.
        user_history (dict): Mock historical data (e.g., {'last_purchase_days': 100}).

    Returns:
        list: A list of recommended product names and actions.
    """
    recommendations = []
    recommendation_ids = set() # Use a set to prevent duplicate product recommendations

    print(f"\n--- Running Inference Engine for Item: {current_item_id} ---")
    
    # Get the current product's details safely
    current_product = PRODUCTS.get(current_item_id, {})
    
    # --- RULE SET D: Financial Heuristics (ARBITRAGE RULE) ---
    # This rule checks if a product is valuable enough to warrant a special financial action.
    profit_potential = current_product.get('profit_potential', 0.0)
    
    # Rule D1: Arbitrage Opportunity Check
    if profit_potential > 30.00:
        print(f"Rule D1 Triggered: Arbitrage heuristic found high profit potential.")
        recommendations.append(
            f"FINANCIAL ACTION: High-Value Resale Opportunity for {current_product.get('name')}! "
            f"Estimated Potential Profit: ${profit_potential:.2f}"
        )

    # --- RULE SET A: Direct Cross-Selling (Highest Priority) ---
    # This rule looks for explicitly defined complementary products.
    if current_item_id in KNOWLEDGE_BASE:
        print(f"Rule A Triggered: Direct cross-sell rule found.")
        for rec_id in KNOWLEDGE_BASE[current_item_id]:
            recommendation_ids.add(rec_id)

    # --- RULE SET B: Business/Promotional Rules ---
    # These rules drive specific business outcomes like increasing average order value.
    
    # Rule B1: High Cart Value Incentive
    if user_cart_value >= 100.00:
        print("Rule B1 Triggered: Cart value is high.")
        recommendations.append("BUSINESS ACTION: You qualify for **Free Premium Shipping!**")
        
    # Rule B2: Clearance Push
    # Checks if the product has the 'clearance' tag and pushes other clearance items.
    elif current_product.get('tags') and 'clearance' in current_product['tags']:
        print("Rule B2 Triggered: Current item is 'Clearance', pushing related stock.")
        for rec_id in KNOWLEDGE_BASE['clearance_items']:
            recommendation_ids.add(rec_id)
    
    # Use 'else' to prevent B1 and B2 from firing together if B1 is prioritized
    # This sequential IF-ELIF structure is core to rule-based prioritization.


    # --- RULE SET C: Re-engagement/General Rules ---
    # This rule targets user behavior outside the current session.
    
    # Rule C1: User Re-engagement
    if user_history and user_history.get('last_purchase_days', 0) > 90:
        print("Rule C1 Triggered: User is inactive, pushing top bestsellers.")
        for rec_id in KNOWLEDGE_BASE['bestsellers']:
            recommendation_ids.add(rec_id)
            
    # --- 4. FINAL OUTPUT GENERATION ---
    
    # Convert unique product IDs to names
    final_product_names = [PRODUCTS[rec_id]['name'] for rec_id in recommendation_ids if rec_id in PRODUCTS]
    
    # Combine business actions/messages with product names
    return recommendations + final_product_names


# --- 5. INTERACTIVE TESTING CLI (Using input() for user interaction) ---

def run_recommendation_cli():
    """
    Runs the recommendation system in an interactive command-line loop.
    This fulfills the requirement to test the system with user input.
    """
    print("=====================================================")
    print(" BASIC RULE-BASED E-COMMERCE AI SYSTEM")
    print("=====================================================")
    print("Available Products for testing:")
    for pid, data in PRODUCTS.items():
        print(f"- {pid}: {data['name']} (Cat: {data['category']})")
    print("=====================================================")

    while True:
        # --- 1. Get User Input (current_item_id) ---
        item_id = input("\nEnter the Product ID you are viewing (e.g., P101, P501), or type 'quit': ").strip().upper()
        
        if item_id == 'QUIT':
            break

        if item_id not in PRODUCTS:
            print(f"Error: Product ID '{item_id}' not recognized. Please try again.")
            continue

        # --- 2. Get User Input (user_cart_value) ---
        try:
            cart_value_str = input("Enter your current Cart Value (e.g., 55.00): $").strip()
            user_cart_value = float(cart_value_str)
        except ValueError:
            print("Error: Invalid cart value. Using $0.00.")
            user_cart_value = 0.00
            
        # --- 3. Get User Input (user_history) ---
        try:
            days_inactive_str = input("Days since your last purchase (e.g., 120): ").strip()
            days_inactive = int(days_inactive_str)
        except ValueError:
            print("Error: Invalid days inactive. Using 0.")
            days_inactive = 0
            
        # Compile User History Data Structure
        user_history_data = {'last_purchase_days': days_inactive}
        
        # --- 4. Call Inference Engine and Output Results ---
        
        recommendations = get_product_recommendations(
            current_item_id=item_id, 
            user_cart_value=user_cart_value,
            user_history=user_history_data
        )

        print("\n[RECOMMENDATION RESULTS]")
        if recommendations:
            for rec in recommendations:
                print(f"-> {rec}")
        else:
            print("No rules matched. No recommendations at this time.")
        print("\n=====================================================")

if __name__ == "__main__":
    run_recommendation_cli()
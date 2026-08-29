def get_recommendations(age: int, glow_score: float) -> dict:
    """
    Generates customized skincare and lifestyle recommendations based on estimated Age and Glow Score.
    Categorized into Khao (Eat), Piyo (Drink), Lagao (Apply), and AM/PM Routines.
    """
    
    # 1. Determine Skincare Category based on Age
    if age < 25:
        age_group = "Youth (Sebum & Acne Control Focus)"
        diet_age_advice = "Avoid oily junk foods and excess sugar. Focus on zinc and antioxidant-rich foods to prevent acne flareups."
        apply_age_advice = "Use a gentle Salicylic Acid cleanser to keep pores clean and regulate excess oil. Avoid heavy, pore-clogging creams."
        am_routine = [
            "Wash with a Salicylic Acid based cleanser.",
            "Apply a lightweight, oil-free moisturizer.",
            "Apply a broad-spectrum gel sunscreen (SPF 50) to block UV rays and dust particles."
        ]
        pm_routine = [
            "Double-cleanse to completely remove dirt, pollution, and sweat accumulated during the day.",
            "Apply Aloe Vera gel or a spot treatment (like Tea Tree oil) on any active pimples.",
            "Hydrate with a non-comedogenic gel moisturizer."
        ]
    elif age <= 45:
        age_group = "Adult (Hydration & Pollution Defense)"
        diet_age_advice = "Focus on healthy fats (Omega-3 from walnuts/seeds) and Vitamin C (Oranges, Amla) to promote collagen synthesis and fight stress-induced dullness."
        apply_age_advice = "Incorporate Niacinamide or Vitamin C serums in the morning to fight pigmentation, and Hyaluronic acid for deep hydration."
        am_routine = [
            "Cleanse with a mild hydrating face wash.",
            "Apply 3-4 drops of Vitamin C / Niacinamide serum for antioxidant protection.",
            "Apply a hydrating sunscreen (SPF 40+) to create a shield against dust and smoke."
        ]
        pm_routine = [
            "Cleanse thoroughly with a gentle foaming cleanser.",
            "Apply a hydrating toner followed by Hyaluronic Acid or Retinol (for overnight skin cell turnover).",
            "Seal hydration with a nourishing night cream."
        ]
    else:
        age_group = "Mature (Collagen & Barrier Repair)"
        diet_age_advice = "Load up on high-protein, collagen-supporting foods, berries, tomatoes (rich in lycopene), and leafy greens to enhance skin elasticity."
        apply_age_advice = "Use ceramide-rich moisturizers to restore the skin barrier, and mild retinoids or peptides to reduce fine lines."
        am_routine = [
            "Cleanse with a creamy, non-foaming moisturizing cleanser.",
            "Apply a peptide or Vitamin C serum to boost brightness.",
            "Apply a rich moisturizing sunscreen with ceramide support."
        ]
        pm_routine = [
            "Cleanse with a nourishing cleansing balm, followed by a gentle face wash.",
            "Apply a barrier repair cream or a night oil rich in Vitamin E.",
            "Massage a nourishing under-eye cream to reduce puffiness and fine lines."
        ]

    # 2. Adjust Recommendations based on Glow Score
    if glow_score < 60:
        glow_status = "Dull & Dehydrated (Need Intensive Glow Recovery)"
        glow_diet = "Consume hydration-boosting fruits like watermelon, cucumber, and foods rich in Vitamin E (sunflower seeds, almonds). Limit coffee and tea."
        glow_drink = [
            "Lemon water with a drop of organic honey first thing in the morning to detoxify.",
            "Coconut water (Nariyal Paani) daily for electrolytes and immediate hydration.",
            "Drink at least 3.5 liters of clean water throughout the day."
        ]
        glow_apply = [
            "Exfoliate very gently 1-2 times a week using a mild Lactic Acid or fruit enzyme peeling gel to remove dead skin cells and dust build-up.",
            "Apply a DIY Papaya or Honey-Yogurt mask twice a week for instant natural glow.",
            "Use a hydrating sheet mask or sleeping mask once a week."
        ]
    elif glow_score <= 80:
        glow_status = "Healthy Skin (Maintain and Polish)"
        glow_diet = "Maintain a balanced diet including carrots (beta-carotene), spinach, walnuts, and dark chocolate (moderate) for polyphenol skin benefits."
        glow_drink = [
            "Green tea (2 cups daily) to flush toxins and protect skin cells from pollution damage.",
            "Fresh carrot-beetroot juice to boost internal blood circulation and natural cheek flush.",
            "Maintain a steady intake of 2.5 - 3 liters of water."
        ]
        glow_apply = [
            "Weekly clay mask (like Kaolin or Multani Mitti) on oily zones to extract deep-seated dust and pollution.",
            "Apply a lightweight Niacinamide serum daily to maintain skin clarity and even skin tone.",
            "Keep a facial mist handy to hydrate skin during long working hours."
        ]
    else:
        glow_status = "Radiant & Clear (Super Glow - Keep it up!)"
        glow_diet = "Keep doing what you are doing! Maintain high antioxidant intake through mixed berries, chia seeds, and green tea."
        glow_drink = [
            "Matcha green tea or herbal hibiscus tea for antioxidant maintenance.",
            "Infused water (cucumber + mint leaves) for keeping skin fresh and cooling.",
            "Ensure regular 2.5 liters of water daily."
        ]
        glow_apply = [
            "Continue with your daily sunscreen and gentle hydration routine.",
            "Avoid trying too many new skincare products; stick to what is working.",
            "Use a silk pillowcase to avoid friction and maintain skin smoothness."
        ]

    # 3. Specific Pollution & Dust Protection Tips (Hinglish/English Hybrid)
    pollution_tips = [
        "**Ghar aate hi double-cleanse karein**: Outdoor dust and oil stick to skin. First use micellar water or light oil, then wash with face wash.",
        "**Pimple ko bilkul na chhuein (Don't pop pimples)**: Touching transfers dirt from fingers to face, leading to more acne/infection. Use pimple patches.",
        "**Sunscreen is non-negotiable**: UV rays + pollution form a deadly combination that causes premature skin damage and hyperpigmentation.",
        "**Weekly steam and deep cleaning**: Take steam for 3-5 minutes, then wipe with a clean soft towel. It opens up pores to clear out trapped dust (dhul-mitti)."
    ]

    return {
        "age_group": age_group,
        "glow_status": glow_status,
        "diet_advice": f"{diet_age_advice} {glow_diet}",
        "apply_advice": apply_age_advice,
        "drinks": glow_drink,
        "apply_steps": glow_apply,
        "am_routine": am_routine,
        "pm_routine": pm_routine,
        "pollution_tips": pollution_tips
    }

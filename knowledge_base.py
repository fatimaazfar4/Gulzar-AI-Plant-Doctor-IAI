"""
knowledge_base.py  -  Gulzar-AI: Plant Doctor for Pakistani Home Gardens
-------------------------------------------------------------------------
Holds ALL domain knowledge:
  1. PLANTS            - the 10 supported plants
  2. SYMPTOM_GROUPS    - checkbox symptoms shown in the UI (fact ids + labels)
  3. EXTRA_CONDITIONS  - yes/no care, environment and Karachi factors
  4. DIAGNOSES         - every possible conclusion (id -> name, category)
  5. RULES             - 11 derived-fact rules + 66 diagnosis rules

A rule says:  IF all(if_all) AND any(if_any) AND NOT any(if_none)
              THEN conclude <concludes> with certainty factor <cf>.

kind="fact"      -> adds an intermediate fact to working memory (chaining)
kind="diagnosis" -> adds evidence for a diagnosis (also adds "dx_<id>" fact)
"""
from dataclasses import dataclass

# --------------------------------------------------------------------------
# 1. PLANTS
# --------------------------------------------------------------------------
PLANTS = {
    "money_plant": "Money Plant",
    "mint": "Mint (Pudina)",
    "rose": "Rose (Gulab)",
    "hibiscus": "Hibiscus (Gudhal)",
    "curry_leaf": "Curry Leaf (Kari Patta)",
    "chili": "Chili (Mirch)",
    "tomato": "Tomato (Tamatar)",
    "lemon": "Lemon (Nimbu)",
    "aloe": "Aloe Vera",
    "tulsi": "Tulsi (Holy Basil)",
}

# --------------------------------------------------------------------------
# 2. SYMPTOMS (checkboxes).  fact_id -> label
# --------------------------------------------------------------------------
SYMPTOM_GROUPS = {
    "Leaf colour": {
        "yellow_all": "Leaves yellow all over",
        "yellow_lower": "Lower / older leaves turning yellow",
        "yellow_new": "New leaves turning yellow",
        "interveinal_new": "New leaves yellow between green veins",
        "interveinal_old": "Old leaves yellow between green veins",
        "pale_new": "New leaves pale / light green",
        "purple_reddish": "Leaves purple or reddish",
        "dark_green_stunted": "Leaves very dark green and plant stunted",
        "bleached_patches": "Bleached / white-brown patches on leaves",
    },
    "Leaf damage": {
        "brown_tips": "Brown crispy leaf tips",
        "brown_edges": "Brown leaf edges",
        "brown_edges_old": "Brown edges on OLD leaves",
        "yellow_halo": "Spots surrounded by a yellow ring (halo)",
        "black_spots": "Black spots on leaves",
        "small_brown_spots": "Many small brown spots",
        "concentric_rings": "Brown spots with ring pattern (target-like)",
        "water_soaked": "Dark water-soaked patches",
        "soft_dark_spots": "Soft, dark, slimy-looking spots",
        "white_powder": "White powdery coating",
        "orange_pustules": "Orange pustules under leaves",
        "gray_fuzz": "Gray fuzzy mould",
        "curling": "Leaves curling",
        "distorted_new": "Small / distorted new leaves",
        "holes": "Holes in leaves",
        "stippling": "Tiny pale dots (stippling) on leaves",
        "silvery_streaks": "Silvery streaks on leaves",
        "leaf_tunnels": "Winding tunnels / trails inside leaves",
        "soft_translucent_leaves": "Leaves soft and translucent / mushy",
        "dust_on_leaves": "Leaves covered in dust",
    },
    "Whole plant": {
        "wilting": "Wilting / drooping",
        "wilting_midday": "Wilts at midday, recovers in evening",
        "leaf_drop": "Leaves dropping",
        "leggy": "Leggy, stretched growth",
        "stunted": "Stunted growth",
        "slow_growth": "Slow growth",
        "no_flowers": "No flowers",
        "bud_drop": "Buds / flowers dropping",
        "fruit_drop": "Fruit dropping",
        "blossom_end_rot": "Dark sunken patch at bottom of fruit",
        "seedling_collapse": "Seedling collapsed at soil level",
        "recently_moved": "Plant recently moved / repotted",
    },
    "Stem and roots": {
        "mushy_stem": "Mushy / soft stem base",
        "smelly_roots": "Black or foul-smelling roots",
        "white_crust": "White crust on soil or pot rim",
        "roots_out_holes": "Roots coming out of drainage holes",
        "brown_bumps": "Brown bumps on stems",
    },
    "Pests seen": {
        "tiny_bugs": "Tiny green / black bugs",
        "whiteflies": "Tiny white flies fly up when plant is shaken",
        "cotton_clumps": "White cotton-like clumps",
        "webbing": "Fine webbing",
        "sticky_leaves": "Sticky leaves",
        "sooty_coating": "Black sooty coating",
        "caterpillar_seen": "Caterpillar / worm visible",
        "ants_on_plant": "Many ants on the plant",
    },
}

# --------------------------------------------------------------------------
# 3. YES/NO CONDITIONS  (care, environment, Karachi factors)
# --------------------------------------------------------------------------
EXTRA_CONDITIONS = {
    "Care and soil": {
        "water_irregular": "I water irregularly (skip days, then flood)",
        "pot_no_holes": "Pot has no drainage holes",
        "water_pools": "Water pools on top of soil",
        "water_runs_off": "Water runs straight off / through instantly",
        "hard_soil": "Soil is hard and compacted",
        "soil_wet_4days": "Soil stays wet for 4+ days",
    },
    "Environment": {
        "wet_leaves_night": "Leaves stay wet at night (dew / evening watering)",
        "ac_on": "Plant sits in a room with AC running",
        "draft": "Plant is in a draft of AC / fan",
        "sudden_temp_swing": "Sudden temperature change recently",
        "post_rain": "Heavy rain in the last few days",
    },
    "Karachi factors": {
        "sea_breeze": "Plant is exposed to sea breeze",
    },
}

# Single-choice inputs: key -> {value: label}
CHOICES = {
    "location": {"pot": "In a pot", "ground": "In the ground"},
    "setting": {"indoor": "Indoor", "balcony": "Balcony", "rooftop": "Rooftop / open terrace"},
    "watering": {
        "daily": "Daily",
        "every_2_3_days": "Every 2-3 days",
        "weekly_or_less": "Weekly or less",
    },
    "drainage": {"good": "Good", "slow": "Slow", "none": "None / water stays"},
    "soil_feel": {"dry": "Dry", "moist": "Slightly moist", "soggy": "Soggy / wet"},
    "fertilizer": {
        "never_or_old": "Never / more than 6 months ago",
        "monthly": "About monthly",
        "heavy": "Heavy / very frequent",
    },
    "pot_size": {"small": "Too small for the plant", "ok": "About right"},
    "season": {
        "summer": "Summer (Apr-Jun)",
        "monsoon": "Monsoon (Jul-Sep)",
        "winter": "Winter (Nov-Feb)",
        "mild": "Mild (Mar / Oct)",
    },
    "humidity": {"low": "Low", "medium": "Medium", "high": "High / sticky"},
    "airflow": {"good": "Good", "poor": "Poor / still air"},
    "water_source": {
        "tanker": "Tanker / tanki water",
        "borewell": "Borewell",
        "ro": "RO / filtered",
        "rain": "Rain water",
        "tap": "Municipal tap",
    },
}

# --------------------------------------------------------------------------
# 4. DIAGNOSES   id -> (display name, category)
# --------------------------------------------------------------------------
DIAGNOSES = {
    # Watering
    "overwatering": ("Overwatering", "Watering"),
    "root_rot": ("Root rot", "Watering"),
    "underwatering": ("Underwatering", "Watering"),
    "inconsistent_watering": ("Inconsistent watering stress", "Watering"),
    "waterlogging_risk": ("Waterlogging risk (pot without holes)", "Watering"),
    # Nutrients
    "nitrogen_def": ("Nitrogen deficiency", "Nutrients"),
    "iron_def": ("Iron deficiency (chlorosis)", "Nutrients"),
    "magnesium_def": ("Magnesium deficiency", "Nutrients"),
    "potassium_def": ("Potassium deficiency", "Nutrients"),
    "phosphorus_def": ("Phosphorus deficiency", "Nutrients"),
    "calcium_def": ("Calcium deficiency (blossom end rot)", "Nutrients"),
    "zinc_def": ("Zinc deficiency", "Nutrients"),
    "nitrogen_excess": ("Nitrogen excess (over-fertilised)", "Nutrients"),
    "salt_burn": ("Fertiliser salt burn", "Nutrients"),
    "nutrient_depletion": ("General nutrient depletion", "Nutrients"),
    # Fungal / bacterial
    "powdery_mildew": ("Powdery mildew", "Disease"),
    "black_spot": ("Black spot fungus", "Disease"),
    "rust": ("Rust fungus", "Disease"),
    "early_blight": ("Early blight", "Disease"),
    "late_blight": ("Late blight", "Disease"),
    "sooty_mold": ("Sooty mould", "Disease"),
    "fungal_leaf_spot": ("Fungal leaf spot", "Disease"),
    "bacterial_leaf_spot": ("Bacterial leaf spot", "Disease"),
    "damping_off": ("Damping off", "Disease"),
    "gray_mold": ("Gray mould (Botrytis)", "Disease"),
    # Pests
    "aphids": ("Aphids", "Pests"),
    "whitefly": ("Whitefly", "Pests"),
    "mealybugs": ("Mealybugs", "Pests"),
    "spider_mites": ("Spider mites", "Pests"),
    "thrips": ("Thrips", "Pests"),
    "sap_pest_curl": ("Leaf curl from sap-sucking pests", "Pests"),
    "leaf_miner": ("Citrus leaf miner", "Pests"),
    "caterpillars": ("Caterpillar damage", "Pests"),
    "scale": ("Scale insects", "Pests"),
    "ant_colony": ("Hidden aphid / mealybug colony (ants farming them)", "Pests"),
    # Environment
    "sunburn": ("Sunburn", "Environment"),
    "heat_stress": ("Heat stress", "Environment"),
    "low_light": ("Insufficient light", "Environment"),
    "transplant_shock": ("Transplant / relocation shock", "Environment"),
    "cold_stress": ("Cold stress", "Environment"),
    "low_humidity": ("Low humidity (dry indoor air)", "Environment"),
    "env_drop": ("Bud drop from temperature swing", "Environment"),
    "draft_stress": ("Draft stress (AC / fan)", "Environment"),
    # Soil / pot
    "root_bound": ("Root-bound plant (needs repotting)", "Soil and pot"),
    "soil_compaction": ("Soil compaction", "Soil and pot"),
    "poor_drainage": ("Poor drainage", "Soil and pot"),
    "pot_too_small": ("Pot too small", "Soil and pot"),
    "heavy_soil": ("Heavy water-retaining soil mix", "Soil and pot"),
    "mineral_buildup": ("Mineral build-up in soil", "Soil and pot"),
    # Karachi / seasonal
    "salt_spray": ("Sea-breeze salt spray damage", "Karachi and season"),
    "hard_water_buildup": ("Hard / tanker water salt build-up", "Karachi and season"),
    "fungal_alert": ("High fungal risk (monsoon humidity)", "Karachi and season"),
    "dormancy": ("Normal winter slow-down (dormancy)", "Karachi and season"),
    "poor_airflow": ("Poor airflow on balcony", "Karachi and season"),
    "monsoon_root_stress": ("Monsoon root stress", "Karachi and season"),
    "dust_blocked": ("Dust blocking photosynthesis", "Karachi and season"),
    # Plant specific
    "aloe_rot": ("Aloe rot", "Plant-specific"),
    "hibiscus_bud_drop": ("Hibiscus heat-related bud drop", "Plant-specific"),
    "chili_flower_drop": ("Chili heat-induced flower drop", "Plant-specific"),
}


# --------------------------------------------------------------------------
# 5. RULES
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class Rule:
    id: str
    category: str
    description: str
    concludes: str
    cf: float
    if_all: tuple = ()
    if_any: tuple = ()
    if_none: tuple = ()
    kind: str = "diagnosis"  # "fact" or "diagnosis"


def _d(id, cat, desc, concl, cf, all=(), any=(), none=()):
    """Shortcut to build a diagnosis rule."""
    return Rule(id, cat, desc, concl, cf, tuple(all), tuple(any), tuple(none), "diagnosis")


def _f(id, desc, concl, all=(), any=()):
    """Shortcut to build a derived-fact (intermediate) rule."""
    return Rule(id, "Derived fact", desc, concl, 1.0, tuple(all), tuple(any), (), "fact")


# ---- Derived-fact rules (stage 1 of forward chaining) --------------------
DERIVED_RULES = [
    _f("D01", "Soil is wet if soggy or stays wet 4+ days", "wet_soil",
       any=["soil_soggy", "soil_wet_4days"]),
    _f("D02", "Soil is dry if it feels dry", "dry_soil", all=["soil_dry"]),
    _f("D03", "Hot weather: 35C+ or summer", "hot_weather",
       any=["temp_35plus", "season_summer"]),
    _f("D04", "Warm weather: 28C+ or summer or monsoon", "warm_weather",
       any=["temp_28plus", "season_summer", "season_monsoon"]),
    _f("D05", "Humid air: high humidity or monsoon", "humid_air",
       any=["humidity_high", "season_monsoon"]),
    _f("D06", "Dry air: low humidity or AC running", "dry_air",
       any=["humidity_low", "ac_on"]),
    _f("D07", "Fungal climate: humid air AND poor airflow", "fungal_climate",
       all=["humid_air", "airflow_poor"]),
    _f("D08", "Salty water: tanker or borewell", "salty_water",
       any=["water_tanker", "water_borewell"]),
    _f("D09", "Pest-prone: sap-sucking pests visible", "sap_pests_visible",
       any=["tiny_bugs", "whiteflies", "cotton_clumps"]),
    _f("D10", "Poor drainage fact", "bad_drainage",
       any=["drainage_slow", "drainage_none", "water_pools", "pot_no_holes"]),
    _f("D11", "Too much sun: 6+ hours direct sun", "too_much_sun", all=["sun_6plus"]),
]

# ---- A. Watering ----------------------------------------------------------
_A = "Watering"
_B = "Nutrients"
_C = "Disease"
_D = "Pests"
_E = "Environment"
_F = "Soil and pot"
_G = "Karachi and season"
_H = "Plant-specific"

DIAGNOSIS_RULES = [
    _d("R01", _A, "Yellow lower leaves + wet soil + daily watering", "overwatering", 0.85,
       all=["yellow_lower", "wet_soil", "water_daily"]),
    _d("R02", _A, "Mushy stem base + foul-smelling roots", "root_rot", 0.90,
       all=["mushy_stem", "smelly_roots"]),
    _d("R03", _A, "Wilting + dry soil", "underwatering", 0.80,
       all=["wilting", "dry_soil"]),
    _d("R04", _A, "Brown crispy tips + dry soil + hot weather", "underwatering", 0.70,
       all=["brown_tips", "dry_soil", "hot_weather"]),
    _d("R05", _A, "Wilting + wet soil (not thirst, it is the roots)", "root_rot", 0.80,
       all=["wilting", "wet_soil"]),
    _d("R06", _A, "Leaf drop + irregular watering", "inconsistent_watering", 0.65,
       all=["leaf_drop", "water_irregular"]),
    _d("R07", _A, "Pot without holes + slow/no drainage", "waterlogging_risk", 0.75,
       all=["pot_no_holes"], any=["drainage_slow", "drainage_none"]),
    _d("R08", _A, "Monsoon + wet soil + yellowing", "overwatering", 0.80,
       all=["season_monsoon", "wet_soil"], any=["yellow_all", "yellow_lower"]),

    # ---- B. Nutrients -----------------------------------------------------
    _d("R09", _B, "Yellow lower leaves + slow growth + soil NOT wet", "nitrogen_def", 0.80,
       all=["yellow_lower", "slow_growth"], none=["wet_soil"]),
    _d("R10", _B, "New leaves yellow between veins", "iron_def", 0.85,
       all=["interveinal_new"]),
    _d("R11", _B, "Old leaves yellow between veins", "magnesium_def", 0.85,
       all=["interveinal_old"]),
    _d("R12", _B, "Brown edges on old leaves", "potassium_def", 0.80,
       all=["brown_edges_old"]),
    _d("R13", _B, "Purple/reddish leaves + stunting", "phosphorus_def", 0.80,
       all=["purple_reddish", "stunted"]),
    _d("R14", _B, "Dark sunken patch at fruit bottom", "calcium_def", 0.90,
       all=["blossom_end_rot"]),
    _d("R15", _B, "Small distorted new leaves + yellow between veins", "zinc_def", 0.75,
       all=["distorted_new", "interveinal_new"]),
    _d("R16", _B, "Dark green stunted leaves + heavy fertiliser", "nitrogen_excess", 0.80,
       all=["dark_green_stunted", "fert_heavy"]),
    _d("R17", _B, "White crust + brown tips + frequent fertiliser", "salt_burn", 0.75,
       all=["white_crust", "brown_tips"], any=["fert_heavy", "fert_monthly"]),
    _d("R18", _B, "Potted plant never/long-ago fertilised + pale or yellow leaves",
       "nutrient_depletion", 0.65,
       all=["fert_never_or_old", "loc_pot"], any=["pale_new", "yellow_all", "yellow_lower"]),

    # ---- C. Fungal / bacterial -------------------------------------------
    _d("R19", _C, "White powder + humid air or still air", "powdery_mildew", 0.85,
       all=["white_powder"], any=["humid_air", "airflow_poor"]),
    _d("R20", _C, "Rose + black spots + yellow halo", "black_spot", 0.85,
       all=["plant_rose", "black_spots", "yellow_halo"]),
    _d("R21", _C, "Orange pustules under leaves", "rust", 0.90,
       all=["orange_pustules"]),
    _d("R22", _C, "Tomato + ring-patterned brown spots", "early_blight", 0.85,
       all=["plant_tomato", "concentric_rings"]),
    _d("R23", _C, "Tomato + water-soaked patches + humid air", "late_blight", 0.85,
       all=["plant_tomato", "water_soaked", "humid_air"]),
    _d("R24", _C, "Black sooty coating + sticky leaves", "sooty_mold", 0.90,
       all=["sooty_coating", "sticky_leaves"]),
    _d("R25", _C, "Small brown spots + leaves wet at night", "fungal_leaf_spot", 0.75,
       all=["small_brown_spots", "wet_leaves_night"]),
    _d("R26", _C, "Soft dark spots + yellow halo + warm and humid", "bacterial_leaf_spot", 0.75,
       all=["soft_dark_spots", "yellow_halo", "humid_air", "warm_weather"]),
    _d("R27", _C, "Seedling collapsed at soil level", "damping_off", 0.90,
       all=["seedling_collapse"]),
    _d("R28", _C, "Gray fuzzy growth + humid air", "gray_mold", 0.85,
       all=["gray_fuzz", "humid_air"]),

    # ---- D. Pests ---------------------------------------------------------
    _d("R29", _D, "Tiny bugs + sticky leaves", "aphids", 0.85,
       all=["tiny_bugs", "sticky_leaves"]),
    _d("R30", _D, "White flies fly up when shaken", "whitefly", 0.90,
       all=["whiteflies"]),
    _d("R31", _D, "White cotton clumps", "mealybugs", 0.90,
       all=["cotton_clumps"]),
    _d("R32", _D, "Webbing + stippling + hot or dry air", "spider_mites", 0.85,
       all=["webbing", "stippling"], any=["hot_weather", "dry_air"]),
    _d("R33", _D, "Silvery streaks + distorted new growth", "thrips", 0.80,
       all=["silvery_streaks", "distorted_new"]),
    _d("R34", _D, "Curling + sticky leaves + an identified sap-sucker (chained rule)",
       "sap_pest_curl", 0.75,
       all=["curling", "sticky_leaves"], any=["dx_aphids", "dx_whitefly", "dx_mealybugs"]),
    _d("R35", _D, "Lemon + winding leaf tunnels", "leaf_miner", 0.95,
       all=["plant_lemon", "leaf_tunnels"]),
    _d("R36", _D, "Holes in leaves + caterpillar seen", "caterpillars", 0.90,
       all=["holes", "caterpillar_seen"]),
    _d("R37", _D, "Brown bumps on stems + sticky leaves", "scale", 0.85,
       all=["brown_bumps", "sticky_leaves"]),
    _d("R38", _D, "Many ants on plant", "ant_colony", 0.70,
       all=["ants_on_plant"]),

    # ---- E. Environment ---------------------------------------------------
    _d("R39", _E, "Bleached patches + 6+ hours direct sun", "sunburn", 0.85,
       all=["bleached_patches", "too_much_sun"]),
    _d("R40", _E, "40C+ + midday wilting", "heat_stress", 0.80,
       all=["temp_40plus", "wilting_midday"]),
    _d("R41", _E, "Leggy growth + under 3 hrs light + pale/slow", "low_light", 0.80,
       all=["leggy", "sun_lt3"], any=["pale_new", "yellow_all", "slow_growth"]),
    _d("R42", _E, "Leaf drop + recently moved", "transplant_shock", 0.80,
       all=["leaf_drop", "recently_moved"]),
    _d("R43", _E, "Below 10C + curled or purple leaves", "cold_stress", 0.80,
       all=["temp_cold"], any=["curling", "purple_reddish"]),
    _d("R44", _E, "Brown tips + dry indoor air", "low_humidity", 0.70,
       all=["brown_tips", "dry_air", "loc_indoor"]),
    _d("R45", _E, "Bud drop + sudden temperature swing", "env_drop", 0.70,
       all=["bud_drop", "sudden_temp_swing"]),
    _d("R46", _E, "Leaf drop + AC/fan draft", "draft_stress", 0.70,
       all=["leaf_drop", "draft"]),

    # ---- F. Soil / pot ----------------------------------------------------
    _d("R47", _F, "Roots out of holes + stunted", "root_bound", 0.85,
       all=["roots_out_holes", "stunted"]),
    _d("R48", _F, "Water runs off + hard soil", "soil_compaction", 0.80,
       all=["water_runs_off", "hard_soil"]),
    _d("R49", _F, "Water pools on top of soil", "poor_drainage", 0.80,
       all=["water_pools"]),
    _d("R50", _F, "Small pot + wilting", "pot_too_small", 0.75,
       all=["pot_small", "wilting"]),
    _d("R51", _F, "Soil stays wet 4+ days", "heavy_soil", 0.75,
       all=["soil_wet_4days"]),
    _d("R52", _F, "White crust on soil or pot rim", "mineral_buildup", 0.75,
       all=["white_crust"]),

    # ---- G. Karachi / seasonal -------------------------------------------
    _d("R53", _G, "Sea-breeze exposure + brown leaf edges", "salt_spray", 0.80,
       all=["sea_breeze", "brown_edges"]),
    _d("R54", _G, "Tanker/borewell water + white crust + brown tips", "hard_water_buildup", 0.85,
       all=["salty_water", "white_crust", "brown_tips"]),
    _d("R55", _G, "Monsoon humidity + powder / spots / mould", "fungal_alert", 0.80,
       all=["season_monsoon", "humid_air"],
       any=["white_powder", "small_brown_spots", "soft_dark_spots", "gray_fuzz"]),
    _d("R56", _G, "Summer + rooftop + midday wilting", "heat_stress", 0.85,
       all=["season_summer", "loc_rooftop", "wilting_midday"]),
    _d("R57", _G, "Winter + slow growth + no pests", "dormancy", 0.70,
       all=["season_winter", "slow_growth"],
       none=["tiny_bugs", "whiteflies", "cotton_clumps", "webbing"]),
    _d("R58", _G, "Fungal climate (humid + still air) + balcony", "poor_airflow", 0.70,
       all=["fungal_climate", "loc_balcony"]),
    _d("R59", _G, "Post-rain + wet soil + pot + yellowing", "monsoon_root_stress", 0.80,
       all=["post_rain", "wet_soil", "loc_pot"], any=["yellow_all", "yellow_lower"]),
    _d("R60", _G, "Dusty leaves outside monsoon", "dust_blocked", 0.70,
       all=["dust_on_leaves"], none=["season_monsoon"]),

    # ---- H. Plant-specific ------------------------------------------------
    _d("R61", _H, "Aloe + soft translucent leaves", "aloe_rot", 0.90,
       all=["plant_aloe", "soft_translucent_leaves"]),
    _d("R62", _H, "Hibiscus + bud drop + hot weather", "hibiscus_bud_drop", 0.80,
       all=["plant_hibiscus", "bud_drop", "hot_weather"]),
    _d("R63", _H, "Curry leaf + yellowing new leaves", "iron_def", 0.85,
       all=["plant_curry_leaf", "yellow_new"]),
    _d("R64", _H, "Chili + flower drop + 38C+", "chili_flower_drop", 0.85,
       all=["plant_chili", "bud_drop", "temp_38plus"]),
    _d("R65", _H, "Mint + leggy overcrowded growth + orange pustules", "rust", 0.85,
       all=["plant_mint", "leggy", "orange_pustules"]),
    _d("R66", _H, "Lemon + yellow between veins on new leaves", "zinc_def", 0.75,
       all=["plant_lemon", "interveinal_new"]),
]

RULES = DERIVED_RULES + DIAGNOSIS_RULES


def kb_stats():
    """Quick summary of the knowledge base (handy for the UI and viva)."""
    return {
        "total_rules": len(RULES),
        "diagnosis_rules": len(DIAGNOSIS_RULES),
        "derived_fact_rules": len(DERIVED_RULES),
        "distinct_diagnoses": len({r.concludes for r in DIAGNOSIS_RULES}),
        "plants": len(PLANTS),
    }
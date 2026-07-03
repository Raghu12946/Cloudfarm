import os
from django.conf import settings
from django.core.files import File
from cloudfarm_app.models import Fertilizer

# Import fertilizers into the database
def import_fertilizers():
    # Example fertilizer data
    FERTILIZER_DATA = [
    {
        "name": "DAP",
        "suitable_crops": "Pulse crops, Oilseed crops, Sugarcane and Cotton",
        "description": (
            "Contains 18% Nitrogen and 46% Phosphorus, enhancing root growth and crop stand. "
            "Best suited for calcareous and alkaline soils. Increases flower number and fruit setting, "
            "improving crop quality and yield."
        ),
        "price": 500,
        "image": "DAP.png",
    },
    {
        "name": "MOP",
        "suitable_crops": "Cereals, Pulses, Oilseeds, Vegetables, and Fruit crops",
        "description": (
            "Contains 60% Potash in a highly water-soluble form. Improves produce quality and reduces pest management costs. "
            "Can be applied independently based on soil tests."
        ),
        "price": 300,
        "image": "MOP.png",
    },
    {
        "name": "SSP",
        "suitable_crops": "Sugarcane, Cotton, Oilseeds and Pulse crops",
        "description": (
            "Contains 16% Phosphorus (100% water soluble), 11% Sulphur, and 21% Calcium. "
            "Promotes vigorous root growth, white root development, and soil texture improvement. "
            "Reduces flower drop, increases fruit setting, and enhances crop pest resistance."
        ),
        "price": 400,
        "image": "SSP.png",
    },
    {
        "name": "Magnesium Sulphate",
        "suitable_crops": "All crops",
        "description": (
            "Plays a key role in chlorophyll synthesis, boosting photosynthesis. "
            "Increases crop greenness, leading to higher yield and quality. "
            "Essential for phosphate metabolism and enzyme system activation."
        ),
        "price": 350,
        "image": "Magnesium_Sulphate.png",
    },
    {
        "name": "Chilated-iron Micronutrient",
        "suitable_crops": "Fruit crops, Vegetable crops, Plantation and field crops",
        "description": (
            "Enhances micronutrient availability, improving crop quality and yields. "
            "Induces pest and disease tolerance, reducing farming losses. "
            "Suitable for drip and foliar applications, boosting nutrient use efficiency."
        ),
        "price": 450,
        "image": "chilated-iron.png",
    },
     {
        "name": "Chelated-Foliar-Grade 2 Micronutrient",
        "suitable_crops": "Fruit crops, Vegetable crops, Plantation and field crops",
        "description": (
            "Enhances micronutrient availability, improving crop quality and yields. "
            "Induces pest and disease tolerance, reducing farming losses. "
            "Suitable for drip and foliar applications, boosting nutrient use efficiency."
        ),
        "price": 450,
        "image": "Chelated-Foliar-Grade-2-1-kg-.jpg",
    },
     {
        "name": "Chelated-Zinc Micronutrient",
        "suitable_crops": "Fruit crops, Vegetable crops, Plantation and field crops",
        "description": (
            "Enhances micronutrient availability, improving crop quality and yields. "
            "Induces pest and disease tolerance, reducing farming losses. "
            "Suitable for drip and foliar applications, boosting nutrient use efficiency."
        ),
        "price": 450,
        "image": "Chelatedzn1-kg.jpg",
    },
     {
        "name": "Chilated Foilar Micronutrient",
        "suitable_crops": "Fruit crops, Vegetable crops, Plantation and field crops",
        "description": (
            "Enhances micronutrient availability, improving crop quality and yields. "
            "Induces pest and disease tolerance, reducing farming losses. "
            "Suitable for drip and foliar applications, boosting nutrient use efficiency."
        ),
        "price": 450,
        "image": "CHILATED FOILAR.jpg",
    },
    {
        "name": "Ammonium Sulphate",
        "suitable_crops": "Sugarcane, Tobacco, Paddy",
        "description": (
            "Contains 20.5% Nitrogen and 23% Sulphur, enhancing nitrogen use efficiency. "
            "Acts as a quick-acting acidic fertilizer, ideal for saline and alkaline soils. "
            "Reduces nitrogen loss through leaching, making it suitable for planting and top dressing."
        ),
        "price": 380,
        "image": "ammonium sulphate.png",
    },
    {
        "name": "19:19:19",
        "suitable_crops": "Grapes, Pomegranate, Banana, Cotton, Tomato, Onion, Sugarcane, Ginger, Turmeric, Watermelon",
        "description": (
            "Starter-grade fertilizer with balanced nutrients (Nitrogen, Phosphorus, Potassium) for overall crop health. "
            "Promotes root development and shoot growth, enhancing crop vigor. "
            "Ensures cost-effective farming by reducing expenses and increasing net income."
        ),
        "price": 420,
        "image": "19-19-19.png",
    },
    {
        "name": "10:26:26",
        "suitable_crops": "Sugarcane, Cotton, Groundnut, Soybean, Grapes, Pomegranates, Banana, Vegetables, and Pulses",
        "description": (
            "Coated with Smartek technology to enhance nutrient uptake and yield. "
            "Provides ammoniacal Nitrogen for longer green retention and water-soluble Phosphorus for better quality crops. "
            "Builds plant immunity and improves soil texture for healthier plant growth."
        ),
        "price": 440,
        "image": "10-26-26.png",
    },
    {
        "name": "12:32:16",
        "suitable_crops": "Soybean, Potato, and other commercial crops requiring high phosphate initially",
        "description": (
            "Contains Nitrogen, Phosphorus, and Potassium for balanced plant growth. "
            "Promotes faster growth of young plants, even in adverse conditions. "
            "Ideal for crops with high phosphate requirements during early stages."
        ),
        "price": 460,
        "image": "12-32-16.png",
    },
    {
        "name": "20:20:20",
        "suitable_crops": "Cereal crops, Fruit crops, Vegetable crops, and Pulses/Oilseeds",
        "description": (
            "Balanced blend of Nitrogen, Phosphorus, and Potassium for optimal growth. "
            "Enriched with micronutrients and organic humic acid for enhanced plant health. "
            "Improves flowering, fruiting, and overall productivity while being cost-effective."
        ),
        "price": 480,
        "image": "20-20-20.png",
    },
    {
        "name": "10:10:10",
        "suitable_crops": "All crops during early vegetative growth stages",
        "description": (
            "Supplies essential Nitrogen, Phosphorus, and Potassium for plant development. "
            "Promotes root growth, seed and flower formation, and bud ripening. "
            "100% water-soluble for efficient nutrient delivery."
        ),
        "price": 400,
        "image": "10-10-10.png",
    },
    {
        "name": "Hydrated Lime",
        "suitable_crops": "Lawns, gardens, and potted plants",
        "description": (
            "Raises soil pH and neutralizes acidity, improving nutrient uptake by plants. "
            "Enhances soil structure and strengthens plants by providing calcium. "
            "Versatile application for various growing seasons and plant types."
        ),
        "price": 200,
        "image": "hydrated-lime.png",
    },
    {
        "name": "White Potash",
        "suitable_crops": "Fruits, Vegetables, Flowers, and Trees",
        "description": (
            "Provides essential potassium, promoting healthy plant growth and aiding in bud and flower formation. "
            "Organic source derived from plant or wood ashes; acts as a natural fertilizer and soil pH adjuster. "
            "Best suited for pot plants; boosts growth and should be used in moderation to avoid nutrient imbalances."
        ),
        "price": 340,
        "image": "white-potash.png",
    },
    {
        "name": "Ferrous Sulphate",
        "suitable_crops": "Cereal crops, Pulses, Horticultural crops",
        "description": (
            "Catalyst for chlorophyll formation and oxygen carrier, improving plant vitality. "
            "Effective in correcting iron deficiency chlorosis, especially in high-lime soils. "
            "Best applied as a foliar spray; can also act as a lawn conditioner and moss killer."
        ),
        "price": 360,
        "image": "ferrous-sulphate.png",
    },
    {
        "name": "Sulphur Bentonite",
        "suitable_crops": "Agricultural crops, Horticultural crops, Oilseeds",
        "description": (
            "Enhances protein production, amino acid creation, and vitamin synthesis in plants. "
            "Decreases pH of alkaline soils, improving absorption of nitrogen, phosphates, and trace elements. "
            "Increases plant growth, resistance to cold, and acts as a natural fungicide."
        ),
        "price": 370,
        "image": "sulphur.png",
    },
    {
        "name": "Urea",
        "suitable_crops": "Nitrogen-heavy crops, Acid-loving plants, Vegetables and Fruits",
        "description": (
            "Supplies high nitrogen content, supporting vigorous growth, photosynthesis, and protein formation. "
            "Easy and safe to store; non-flammable with neutral pH, making it versatile for all soils. "
            "Ensures prolonged nitrogen availability in soil but requires monitoring to prevent leaching."
        ),
        "price": 320,
        "image": "urea.png",
    },
]

    for fertilizer in FERTILIZER_DATA:
        # Get or create a Fertilizer object
        fertilizer_obj, created = Fertilizer.objects.get_or_create(
            name=fertilizer['name'],
            defaults={
                "suitable_crops": fertilizer['suitable_crops'],
                "description": fertilizer['description'],
                "price": fertilizer['price'],
            }
        )

        if created:
            print(f"Created new fertilizer: {fertilizer['name']}")
            # Save the image if it exists
            if fertilizer['image']:
                image_path = os.path.join(settings.MEDIA_ROOT, fertilizer['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as image_file:
                        fertilizer_obj.image.save(
                            os.path.basename(fertilizer['image']),
                            File(image_file),
                            save=True
                        )
                else:
                    print(f"Image file not found: {image_path}")
        else:
            print(f"Fertilizer already exists: {fertilizer['name']}")

# Run the script
if __name__ == "__main__":
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
    django.setup()

    import_fertilizers()
    print("Fertilizer import completed.")

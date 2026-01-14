from flask import Flask, render_template, request, send_file

# ===================== EMISSIONS CALCULATIONS =====================
# Import functions responsible for computing baseline emissions
# and alternative low-carbon scenarios
from calculations.emissions import calculate_emissions
from calculations.scenarios import (
    scenario_modal_substitution,   # Shift from high-carbon to low-carbon transport modes
    scenario_digital_sobriety,      # Reduce digital-related emissions
    scenario_utility_aware,         # Adjust emissions based on the perceived utility of the mission
)

# ===================== PDF GENERATION =====================
# Function that generates a PDF report summarizing the results
from pdf.report import generate_scar_pdf

# Initialize the Flask application
app = Flask(__name__)


# ===================== HOME PAGE =====================
# Landing page of the SCAR application
@app.route("/")
def home():
    return render_template("scar_lasfargue.html")


# ===================== FORM PAGE =====================
# Page where users enter data about their research project
@app.route("/form")
def form():
    return render_template("form_scar.html")


# ===================== RESULTS PAGE =====================
# This route processes the submitted form and computes results
@app.route("/results", methods=["POST"])
def results():
    # Convert form inputs into a dictionary
    form_data = request.form.to_dict()

    # Compute baseline emissions and total carbon footprint
    baseline_emissions, baseline_total = calculate_emissions(form_data)
    baseline_total = round(baseline_total, 2)

    # Extract the declared utility level of the mission
    utility = int(form_data.get("mission_utility", 0))

    # Identify the dominant emission source and its relative weight
    if baseline_emissions and baseline_total > 0:
        dominant_post, dominant_value = max(
            baseline_emissions.items(),
            key=lambda x: x[1]
        )
        dominant_share = round(dominant_value / baseline_total * 100, 1)
    else:
        dominant_post, dominant_share = "", 0

    # Define emission categories for interpretation
    mobility_posts = {
        "flight_short", "flight_medium", "flight_long",
        "car_diesel", "car_essence", "train_tgv", "train_ter"
    }
    digital_posts = {
        "server", "cloud", "desktop", "laptops",
        "screen", "llm_usage", "ai_training"
    }

    # Aggregate emissions by major category
    mobility_sum = sum(v for k, v in baseline_emissions.items() if k in mobility_posts)
    digital_sum = sum(v for k, v in baseline_emissions.items() if k in digital_posts)

    # Classify the overall emissions profile of the project
    if baseline_total < 100:
        baseline_profile = "low"
    elif digital_sum / baseline_total > 0.6:
        baseline_profile = "digital"
    elif mobility_sum / baseline_total > 0.6:
        baseline_profile = "mobility"
    elif digital_sum / baseline_total > 0.3 and mobility_sum / baseline_total > 0.3:
        baseline_profile = "mixed"
    else:
        baseline_profile = "other"

    # Compute alternative emission scenarios
    scenario_modal = scenario_modal_substitution(baseline_emissions)
    scenario_digital = scenario_digital_sobriety(baseline_emissions)
    scenario_utility = scenario_utility_aware(baseline_emissions, utility)

    # Helper function to compute total emissions
    def total(e):
        return round(sum(e.values()), 2)

    # Store total emissions for each scenario
    totals = {
        "baseline": baseline_total,
        "modal": total(scenario_modal),
        "digital": total(scenario_digital),
        "utility": total(scenario_utility),
    }

    # Compute percentage reductions compared to the baseline
    reductions = {
        k: round((baseline_total - v) / baseline_total * 100, 2)
        if baseline_total > 0 else 0
        for k, v in totals.items() if k != "baseline"
    }

    # Render the results page with all computed indicators
    return render_template(
        "results.html",
        results=baseline_emissions,
        totals=totals,
        reductions=reductions,
        utility=utility,
        dominant_post=dominant_post.replace("_", " "),
        dominant_share=dominant_share,
        baseline_profile=baseline_profile,
    )


# ===================== PDF EXPORT =====================
# This route generates and returns a PDF report of the results
@app.route("/export-pdf", methods=["POST"])
def export_pdf():
    # Retrieve form data again for PDF generation
    form_data = request.form.to_dict()

    # Recompute baseline emissions
    baseline_emissions, baseline_total = calculate_emissions(form_data)
    baseline_total = round(baseline_total, 2)
    utility = int(form_data.get("mission_utility", 0))

    # Compute scenarios
    scenario_modal = scenario_modal_substitution(baseline_emissions)
    scenario_digital = scenario_digital_sobriety(baseline_emissions)
    scenario_utility = scenario_utility_aware(baseline_emissions, utility)

    # Aggregate totals for the PDF
    totals = {
        "baseline": baseline_total,
        "modal": round(sum(scenario_modal.values()), 2),
        "digital": round(sum(scenario_digital.values()), 2),
        "utility": round(sum(scenario_utility.values()), 2),
    }

    # Compute reductions for each scenario
    reductions = {
        k: round((baseline_total - v) / baseline_total * 100, 2)
        if baseline_total > 0 else 0
        for k, v in totals.items() if k != "baseline"
    }

    # Identify dominant emission source
    if baseline_emissions and baseline_total > 0:
        dominant_post, dominant_value = max(
            baseline_emissions.items(),
            key=lambda x: x[1]
        )
        dominant_share = round(dominant_value / baseline_total * 100, 1)
    else:
        dominant_post, dominant_share = "", 0

    # Simple profile classification for the PDF
    baseline_profile = (
        "digital"
        if dominant_post in {"server", "cloud", "desktop", "laptops"}
        else "other"
    )

    # Generate the PDF file in memory
    pdf_buffer = generate_scar_pdf(
    totals=totals,
    reductions=reductions,
    baseline_profile=baseline_profile,
    dominant_post=dominant_post.replace("_", " "),
    dominant_share=dominant_share,
    utility=utility,
    emissions=baseline_emissions   # ← CORRECTION CLÉ
)

    # Send the PDF to the user as a downloadable file
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="SCAR_report.pdf",
        mimetype="application/pdf",
    )


# ===================== STATIC INFORMATION PAGES =====================
@app.route("/this-project")
def this_project():
    return render_template("this_project.html")

@app.route("/methodology")
def methodology():
    return render_template("methodology.html")

@app.route("/references")
def references():
    return render_template("references.html")

@app.route("/acknowledgements")
def acknowledgements():
    return render_template("acknowledgements.html")


# ===================== APPLICATION ENTRY POINT =====================
# Run the Flask development server
if __name__ == "__main__":
    app.run(debug=True, port=5002)

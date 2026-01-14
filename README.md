# SCAR – Scientific Carbon Assessment for Research

## Presentation

SCAR (Scientific Carbon Assessment for Research) is a web-based decision-support tool designed to explore the carbon footprint of academic research projects. Rather than producing exhaustive life-cycle inventories, SCAR aims to make the environmental implications of research practices explicit, interpretable, and discussable, while remaining compatible with academic constraints and real-world decision-making.

The tool is not intended to provide definitive carbon accounting results, nor to rank projects, disciplines, or individuals. Its purpose is to support reflexive analysis of research practices by identifying where emissions arise within a project and how they relate to concrete scientific and organisational choices.

**Application URL:**  
https://scar-17cv.onrender.com

---

## Objectives and epistemological positioning

SCAR was conceived in response to a growing tension within contemporary academia. While research increasingly addresses environmental and climate-related issues, the environmental footprint of research practices themselves remains weakly quantified, poorly problematised, and rarely integrated into decision-making processes.

The primary objective of SCAR is therefore not to deliver exhaustive or definitive carbon accounting, but to provide an operational and reflexive framework enabling researchers to understand how emissions are generated within a given project and how these emissions relate to specific research configurations.

From an epistemological perspective, SCAR deliberately positions itself between two extremes. On the one hand, it does not attempt to reproduce the complexity of full Life Cycle Assessment (LCA) methodologies, which require detailed inventories, specialised expertise, and extensive datasets that are rarely available at the scale of individual projects. On the other hand, it avoids purely symbolic or declarative approaches that would reduce carbon assessment to generic averages disconnected from actual practices.

SCAR is therefore best understood as a decision-support and discussion tool. It is designed to inform choices when several research configurations are possible, to identify structural emission drivers, and to make trade-offs explicit. It does not prescribe a single optimal research model.

In this sense, SCAR addresses the following question:  
*Given a research objective, which activities generate emissions, and which levers can realistically be mobilised without undermining scientific integrity?*

---

## Scope definition and system boundaries

Defining system boundaries is a central methodological step in any carbon assessment. In SCAR, these boundaries are intentionally restricted in order to preserve both analytical relevance and practical usability.

Only emission sources that satisfy two criteria are included: first, they must represent a non-negligible contribution to the overall carbon footprint of research activities; second, they must be meaningfully influenced by project-level decisions.

Based on these criteria, SCAR includes several major categories of emissions, notably mobility (air, rail, and road transport), energy use during missions, digital practices (devices, servers, cloud computing, AI usage), food consumption associated with research travel, and accommodation related to conferences or fieldwork.

Conversely, emissions embedded in long-term institutional infrastructure—such as building construction, campus-wide energy systems, or central administrative services—are excluded. While these emissions are significant at the institutional level, they cannot be robustly attributed to individual projects without introducing arbitrary allocation rules that would obscure rather than clarify responsibility.

This boundary choice reflects a deliberate methodological trade-off: SCAR sacrifices exhaustiveness in order to preserve interpretability and to focus attention on emission levers that researchers can realistically discuss, negotiate, or influence.

---

## Emission factors and data sources

All numerical estimates produced by SCAR rely on emission factors expressed in kilograms of CO₂ equivalent (kgCO₂e) per unit of activity. These factors are drawn from publicly available and widely recognised sources, primarily national databases produced by ADEME and methodological frameworks such as GES 1point5.

Depending on the activity considered, emission factors may be expressed per kilometre travelled, per hour of use, per device-year, or per meal. For example, air travel emissions are computed as the product of travelled distance and a distance-specific emission factor, while digital equipment emissions are annualised over an estimated lifespan and allocated to project usage.

Emission factors are treated as order-of-magnitude estimates. SCAR does not claim high numerical precision, as such precision would be illusory given uncertainties in usage patterns, technological heterogeneity, and reporting practices. Precision is intentionally traded for transparency: the objective is to provide robust and interpretable approximations rather than exact measurements.

---

## Calculation logic and aggregation

The computational logic implemented in SCAR follows a deliberately simple and transparent structure. For each emission category, user-reported activity data are multiplied by the corresponding emission factor, yielding category-level emissions expressed in kgCO₂e.

The total carbon footprint of the project is then computed as the sum of all category-level emissions. Only categories with non-zero emissions are displayed in the results, a design choice intended to avoid visual clutter and to facilitate the identification of dominant emission drivers.

No weighting, normalisation, or optimisation procedure is applied. All emissions are treated symmetrically, reflecting the physical equivalence of CO₂e regardless of their source.

---

## Scenario construction and interpretation

Scenarios constitute a central analytical component of SCAR. They are not designed to predict future emissions, nor to prescribe mandatory reduction targets. Instead, they function as counterfactual explorations that examine how the carbon footprint of a given research project would change if a limited set of practices were modified, all other parameters being held constant.

Methodologically, scenarios are constructed by applying conservative adjustment coefficients to selected emission categories in the baseline configuration. Each scenario modifies only a subset of activities, ensuring that changes in total emissions can be directly attributed to the simulated transformation.

Scenario results quantify relative sensitivity rather than performance. They indicate where emissions are responsive to change, not where reductions are required.

### Modal substitution scenario

The modal substitution scenario focuses on mobility-related emissions, which often constitute a significant share of the carbon footprint in projects involving fieldwork, conferences, or international collaboration.

This scenario applies reduction factors to high-carbon transport modes—primarily short- and medium-haul flights—by partially reallocating them to lower-carbon alternatives such as rail transport. Travel volumes remain constant; only transport modes are modified where substitution is technically and organisationally plausible.

The resulting percentage reduction reflects the share of baseline emissions attributable to avoidable transport intensity.

### Digital sobriety scenario

The digital sobriety scenario addresses emissions related to computational infrastructure and digital practices, including servers, cloud services, data storage, and intensive computing tasks.

Rather than assuming radical technological change, this scenario simulates moderate efficiency gains, such as reduced server over-provisioning, shorter data retention periods, improved task scheduling, or the pooling of computational resources.

### Utility-aware scenario

The utility-aware scenario introduces an explicit reflection on proportionality. It does not assess the legitimacy of research activities, nor compare projects or disciplines. Instead, it explores how emissions may be contextualised when research activities are weighted by their perceived scientific or societal usefulness.

Adjustments are applied proportionally to selected emission categories based on a user-declared utility score. The resulting reductions should be interpreted as analytical illustrations rather than recommendations.

---

## Interpretation, limits, and responsible use

Results produced by SCAR are context-dependent and sensitive to assumptions, reporting choices, and project-specific constraints. They should therefore be interpreted as situated estimates rather than precise measurements.

SCAR does not evaluate the desirability or legitimacy of research activities, nor does it seek to minimise emissions at all costs. Scientific objectives, epistemic diversity, and academic freedom remain central considerations.

Ultimately, SCAR is designed to support informed discussion rather than judgement. Its value lies in its ability to make implicit trade-offs explicit and to provide a shared quantitative basis for dialogue between researchers, institutions, and funding bodies.

---

## Technical implementation

- Backend: Python, Flask  
- Frontend: HTML, CSS, JavaScript (D3.js)  
- PDF generation: ReportLab  
- Deployment: Render  

The repository is organised in a modular structure separating calculation logic, scenario construction, web templates, static assets, and PDF generation.

---

## Author

Manon Lasfargue  
Academic project – carbon assessment and research practices

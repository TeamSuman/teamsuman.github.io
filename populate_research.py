import os
import sys
import django
import urllib.parse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamsuman.settings')
django.setup()

from home.models import Research, Publication
from django.core.files import File

# Clear existing objects
Research.objects.all().delete()

# We won't delete all Publications as they might be used elsewhere, 
# but for this script we ensure the ones we need exist.

topics = [
    {
        "title": "Protein Allostery & Interactions",
        "description": "Our lab investigates the intricate mechanisms of protein allostery and protein-protein interactions (PPIs). We employ advanced molecular dynamics simulations to understand how distant site perturbations, such as phosphorylation or ligand binding, dynamically regulate protein function. A key focus is uncovering druggable cryptic pockets and designing allosteric modulators for therapeutic intervention in complex systems like the PCSK9-LDLR complex and Rho GTPases.",
        "detail_content": """
            <h2>The Mechanics of Allosteric Regulation</h2>
            <p>Protein allostery is a fundamental biological process where a perturbation at a site distant from the functional site modulates the protein's activity. Our lab focuses on deciphering the bidirectional nature of allosterically regulated systems. We investigate how conformational ensembles transition in response to ligand binding or post-translational modifications, such as phosphorylation.</p>
            
            <figure class="image">
                <img src="/media/images/research_detail_allostery.png" alt="Allostery Illustration">
                <figcaption>Figure 1: Detailed mapping of the allosteric communication network in a protein complex, highlighting the signal transduction pathway from a cryptic pocket to the primary interaction interface.</figcaption>
            </figure>

            <h3>Inhibiting Protein-Protein Interactions (PPIs)</h3>
            <p>A primary application of our allostery research is in the design of specific inhibitors for otherwise 'undruggable' protein-protein interfaces. For example, we have successfully modeled the <b>PCSK9–LDLR</b> complex, identifying druggable cryptic pockets in the C-terminal domain of PCSK9 that, when bound, disrupt the primary LDLR-binding interface through allosteric signal transduction.</p>
            
            <h3>Rho GTPase and Phosphorylation</h3>
            <p>We also explore the molecular mechanisms by which phosphorylation regulates the <b>Rac1–RhoGDI</b> complex. By combining QM/MM and classical MD simulations, we elucidate how altered protonation states induced by phosphorylation act as a switch for allosteric regulation, controlling the kinetics of RhoA GTPase release.</p>
        """,
        "image_path": "/home/dm/Dibyendu/Websites/teamsuman.org/website/media/images/research_detail_allostery.png",
        "my_order": 1,
        "pubs": [
            "Harnessing Allostery to Modulate Protein-Protein Interactions (PPIs)",
            "Leveraging Bidirectional Nature of Allostery To Inhibit PPIs: A Case Study of PCSK9–LDLR",
            "Phosphorylation induces altered protonation states and allosterically regulates Rac1–RhoGDI complex",
            "Molecular mechanism of regulation of RhoA GTPase by phosphorylation of RhoGDI",
            "Mixed-Solvent MD Simulation Reveals a Druggable Allosteric Pocket in the PCSK9 C-Terminal",
            "Conformational Diversity and Allosteric Network Enable Multi-Substrate Recognition in Laccase Enzyme"
        ]
    },
    {
        "title": "Machine Learning & Enhanced Sampling",
        "description": "We develop and apply cutting-edge machine learning and enhanced sampling techniques to overcome timescale limitations in classical molecular simulations. By integrating deep neural networks, variational autoencoders, and adaptive sampling strategies like PathGennie and WeTICA, we efficiently explore complex free energy landscapes. Our tools accurately predict rare event kinetics, ADMET properties, and phase transitions with remarkable computational efficiency.",
        "detail_content": """
            <h2>Overcoming the Timescale Challenge</h2>
            <p>Molecular dynamics simulations are often hampered by the 'timescale gap' between atomistic motions and biological functions. We address this using a suite of machine learning (ML) and enhanced sampling protocols developed in our lab. Our goal is to automate the discovery of reaction coordinates and the mapping of high-dimensional free energy landscapes.</p>
            
            <figure class="image">
                <img src="/media/images/research_detail_ml.png" alt="Free Energy Landscape ML">
                <figcaption>Figure 2: Integration of neural network architectures with 3D free energy landscapes to guide directed sampling of transition pathways between stable states.</figcaption>
            </figure>

            <h3>Adaptive Sampling with PathGennie & WeTICA</h3>
            <p>Our <b>PathGennie</b> algorithm utilizes direction-guided adaptive sampling for the rapid generation of rare event pathways. Complementing this, <b>WeTICA</b> (a directed search weighted ensemble method) enables the exploration of complex conformational transitions in proteins and crystal phase transitions with high statistical precision.</p>
            
            <h3>AI for Drug Discovery: MTAN-ADMET</h3>
            <p>Beyond dynamics, we develop ML tools for predictive pharmacology. <b>MTAN-ADMET</b> is a multi-task adaptive neural network that leverages cross-task knowledge to predict Absorption, Distribution, Metabolism, Excretion, and Toxicity properties of candidate drug molecules with state-of-the-art accuracy.</p>
        """,
        "image_path": "/home/dm/Dibyendu/Websites/teamsuman.org/website/media/images/research_detail_ml.png",
        "my_order": 2,
        "pubs": [
            "MTAN-ADMET: A Multi-Task Adaptive Neural Network for Prediction of ADMET Properties",
            "IceCoder: Identification of Ice phases in molecular simulation using variational autoencoder",
            "Challenges in Transferable Prediction of Solvation Free Energy via Machine Learning",
            "PathGennie: Rapid Generation of Rare Event Pathways via Direction-Guided Adaptive Sampling",
            "WeTICA: A directed search weighted ensemble based enhanced sampling method"
        ]
    },
    {
        "title": "Biophysics & Conformational Dynamics",
        "description": "Understanding the fundamental biophysics of conformational dynamics is central to our research. We explore complex folding pathways, dimensionality reduction of conformational landscapes, and the mechanical stability of biomolecules. Through rigorous mixed-solvent simulations and structural analyses, we map interaction hotspots and elucidate how conformational diversity dictates molecular function and recognition.",
        "detail_content": """
            <h2>Decoding Conformational Diversity</h2>
            <p>Bio-macromolecules exist as dynamic ensembles rather than static structures. We utilize rigorous biophysical methods to characterize these ensembles, focusing on the mechanical stability and conformational transitions of proteins, antigens, and photoreceptors.</p>
            
            <figure class="image">
                <img src="/media/images/research_detail_dynamics.png" alt="Manifold Learning Dynamics">
                <figcaption>Figure 3: 2D manifold learning (UMAP) of a protein folding trajectory, revealing transition state bottlenecks and the evolution of native state contacts.</figcaption>
            </figure>

            <h3>In silico Hotspot Mapping with PPIscout</h3>
            <p>We developed <b>PPIscout</b>, a methodology combining mixed amino acid-water molecular dynamics with structural analysis to identify high-affinity interaction hotspots. This approach is critical for understanding antibody-antigen recognition and the mechanical stabilization of protein scaffolds.</p>
            
            <h3>Dimensionality Reduction Benchmarking</h3>
            <p>A key aspect of our research is benchmarking manifold learning algorithms (t-SNE, UMAP, VAE) for the dimensionality reduction of protein folding trajectories. Our work provides a roadmap for selecting the most appropriate descriptors to map complex biophysical landscapes accurately.</p>
        """,
        "image_path": "/home/dm/Dibyendu/Websites/teamsuman.org/website/media/images/research_detail_dynamics.png",
        "my_order": 3,
        "pubs": [
            "Mapping conformational landscape in protein folding: Benchmarking dimensionality reduction",
            "Unraveling antibody-induced mechanical stability of antigen: Insights from single-molecule studies",
            "Conformational Effects on the Absorption Spectra of Phytochromes",
            "PPIscout: Protein–protein interaction site hotspot mapping using mixed amino acid–water MD"
        ]
    },
    {
        "title": "Solvation, Ionic Liquids & Phase Behavior",
        "description": "We investigate the microscopic origins of solvation thermodynamics and phase behaviors induced by complex solvent environments, including specialized ionic liquids and guanidinium salts. Our quantum chemical and molecular dynamics investigations reveal how specific ion-pairing propensities and surface-active molecules modulate protein (de)stabilization, hydrophobicity, and the delicate balance between protein-water and protein-protein interactions.",
        "detail_content": """
            <h2>A Microscopic View of Solvation</h2>
            <p>Our research delves into the molecular-level thermodynamics of solvation, particularly in non-ideal solvent environments. We explore how ions, organic solutes, and surface-active molecules interact with protein surfaces to influence their stability and folding behavior.</p>
            
            <figure class="image">
                <img src="/media/images/research_detail_solvation.png" alt="Solvation Ion Pairing">
                <figcaption>Figure 4: Molecular visualization of a protein in a complex ionic liquid environment, showcasing ion-pairing propensities and their role in modulating surface hydrophobicity.</figcaption>
            </figure>

            <h3>The Role of Guanidinium Salts</h3>
            <p>We leverage MD simulations to understand the 'ion-pairing propensity' of guanidinium salts. This fundamental property dictates whether a salt acts as a protein stabilizer or denaturant. Our findings reveal anti-correlations between protein-protein and protein-water interactions, providing a new perspective on HOFMEISTER series behavior.</p>
            
            <h3>Ionic Liquids: Hydrophobicity and Phase Behavior</h3>
            <p>We address fundamental questions in the physics of ionic liquids, such as why <b>[BMIM]+[PF6]-</b> is hydrophobic while <b>[BMIM]+[BF4]-</b> is hydrophilic. These investigations extend to the study of surface-active ionic liquids and their impact on human serum albumin binding kinetics.</p>
        """,
        "image_path": "/home/dm/Dibyendu/Websites/teamsuman.org/website/media/images/research_detail_solvation.png",
        "my_order": 4,
        "pubs": [
            "Ion-Pairing Propensity in Guanidinium Salts Dictates Their Protein (De)stabilization Behavior",
            "Conformational and Binding Behaviors of Human Serum Albumin Induced by Surface-Active Ionic Liquids",
            "Why [BMIM]+[PF6]− is hydrophobic and [BMIM]+[BF4]− hydrophilic in nature?",
            "Microscopic origin of observed anti-correlation between protein-protein and protein-water interactions"
        ]
    }
]

for t in topics:
    print(f"Creating topic {t['title']}...")
    try:
        with open(t['image_path'], 'rb') as fp:
            imgFile = File(fp)
            r = Research.objects.create(
                title=t['title'],
                description=t['description'],
                content=t['detail_content'],  # New comprehensive content field
                my_order=t['my_order']
            )
            basename = os.path.basename(t['image_path'])
            r.image.save(basename, imgFile, save=True)
            
            for pub_title in t['pubs']:
                search_url = "https://scholar.google.com/scholar?q=" + urllib.parse.quote(pub_title)
                pub_obj, created = Publication.objects.get_or_create(
                    title=pub_title,
                    defaults={'link': search_url, 'authors': 'Chakrabarty Lab', 'year': 2024}
                )
                r.selected_publications.add(pub_obj)
    except Exception as e:
        print(f"Error for {t['title']}: {e}")

print("Successfully injected data.")

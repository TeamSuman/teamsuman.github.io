# import joblib  # type: ignore
import os

from django.conf import settings

OPTIONAL_DEPENDENCY_ERROR = None

try:
    import numpy as np  # type: ignore
    import pandas as pd  # type: ignore
    from pypmml import Model
    from rdkit import Chem  # type: ignore

    # from rdkit.Chem import AllChem  # type: ignore
    from rdkit.Chem import Descriptors  # type: ignore

    # from rdkit.Chem import Draw  # type: ignore
    from rdkit.Chem.Draw import rdMolDraw2D
    from rdkit.ML.Descriptors import MoleculeDescriptors  # type: ignore
except ModuleNotFoundError as exc:
    OPTIONAL_DEPENDENCY_ERROR = exc


class molproperties:
    """
    Class to calculate various molecular properties from a given SMILES string.

    Args:
        smiles (str): The SMILES string representing the molecule.

    Returns:
        None

    This class calculates various molecular properties such as exact molecular weight, number of hydrogen bond donors,
    number of rotatable bonds, etc., from a given SMILES string. It also provides a prediction using a pre-trained model.
    """

    def __init__(self, smiles=None):
        if OPTIONAL_DEPENDENCY_ERROR is not None:
            raise RuntimeError(
                f"Pharmocast dependency is not installed: {OPTIONAL_DEPENDENCY_ERROR.name}"
            ) from OPTIONAL_DEPENDENCY_ERROR

        smiles = self.remove_whitespace(smiles)
        mol = Chem.MolFromSmiles(smiles)
        self.smiles = smiles
        self.valid = "Valid" if mol is not None else "Invalid"

        self.mol = mol
        base_path = settings.BASE_DIR

        self.delg_xgb_model = Model.fromFile(os.path.join(base_path, "pharmocast/assets/delg_models/xgbr.pmml"))
        self.delg_rfr_path = os.path.join(base_path, "pharmocast/assets/delg_models/rfr.joblib")
        self.delg_svr_path = os.path.join(base_path, "pharmocast/assets/delg_models/svr.joblib")
        self.delg_gpr_path = os.path.join(base_path, "pharmocast/assets/delg_models/gpr.joblib")
        self.delg_krr_path = os.path.join(base_path, "pharmocast/assets/delg_models/krr.joblib")

        self.solu_xgb_model = Model.fromFile(os.path.join(base_path, "pharmocast/assets/solu_models/xgbr.pmml"))
        self.solu_rfr_path = os.path.join(base_path, "pharmocast/assets/solu_models/rfr.joblib")
        self.solu_svr_path = os.path.join(base_path, "pharmocast/assets/solu_models/svr.joblib")
        self.solu_gpr_path = os.path.join(base_path, "pharmocast/assets/solu_models/gbr_model.joblib")
        self.solu_krr_path = os.path.join(base_path, "pharmocast/assets/solu_models/krr.joblib")

        self.pka_xgb_model = Model.fromFile(os.path.join(base_path, "pharmocast/assets/pka_models/xgbr.pmml"))
        self.pka_rfr_path = os.path.join(base_path, "pharmocast/assets/pka_models/rfr.joblib")
        self.pka_svr_path = os.path.join(base_path, "pharmocast/assets/pka_models/svr.joblib")
        self.pka_gpr_path = os.path.join(base_path, "pharmocast/assets/pka_models/gpr.joblib")
        self.pka_krr_path = os.path.join(base_path, "pharmocast/assets/pka_models/krr.joblib")

    def predict_from_joblib(self, model_path, input_dict):
        import joblib
        import pandas as pd

        model = joblib.load(model_path)

        # Compatibility patch for scikit-learn >= 1.4 when loading older models
        def patch_sklearn_model(obj):
            if hasattr(obj, "estimators_"):
                for est in obj.estimators_:
                    patch_sklearn_model(est)
            if hasattr(obj, "steps"):
                for _, step in obj.steps:
                    patch_sklearn_model(step)
            if hasattr(obj, "base_estimator_"):
                patch_sklearn_model(obj.base_estimator_)

            # Set missing attributes that newer sklearn versions expect
            if not hasattr(obj, "monotonic_cst"):
                try:
                    obj.monotonic_cst = None
                except:
                    pass

        patch_sklearn_model(model)

        input_df = pd.DataFrame([input_dict])
        prediction = model.predict(input_df)
        return np.array(prediction).ravel()[0]

    # --- ROBUST DESCRIPTOR CALCULATION FUNCTION ---
    def calc_descriptors(self, smiles, features=[]):
        """
        Calculates specified RDKit descriptors with error handling for individual calculations.
        """
        # Ensure descriptor list is valid
        all_descriptors_available = [x[0] for x in Descriptors._descList]
        selected_descriptors = [d for d in all_descriptors_available if d in features]

        # Check if all requested features are available
        if len(selected_descriptors) != len(features):
            missing = set(features) - set(selected_descriptors)
            print(
                f"Warning: The following requested descriptors are not available in RDKit and will be ignored: {missing}"
            )

        calc = MoleculeDescriptors.MolecularDescriptorCalculator(selected_descriptors)
        desc_names = calc.GetDescriptorNames()

        descriptors = []

        mol = Chem.MolFromSmiles(smiles)
        # Handle invalid SMILES strings
        if mol is None or mol.GetNumHeavyAtoms() == 0:
            pass

        # Try to sanitize mol before AddHs
        try:
            Chem.SanitizeMol(mol)
        except:
            print(f"Skipping unsanitizable SMILES: {smiles}")

        if mol is not None:
            mol = Chem.AddHs(mol)
            # Use a try-except block to handle calculation errors like the one from SPS
            try:
                descriptors = calc.CalcDescriptors(mol)
            except Exception as e:
                # If any descriptor fails for this molecule, record NaNs and print a warning
                print(f"Warning: Could not calculate descriptors for SMILES '{smiles}'. Error: {e}. Appending NaNs.")

        if not descriptors or len(descriptors) != len(desc_names):
            descriptors = [0.0] * len(desc_names)

        # Convert to float to avoid numpy types causing issues with pypmml/py4j
        feature_dict = {desc_names[i]: float(descriptors[i]) for i in range(len(desc_names))}
        return feature_dict

    def calc(self):
        """
        Calculate molecular properties and generate molecular image.

        Parameters:
        self: The instance of the class.

        Returns:
        None.
        """
        mol = self.mol
        d2d = rdMolDraw2D.MolDraw2DSVG(380, 380)
        dopts = d2d.drawOptions()
        # dopts.atomLabelFontSize = 100  # Note: in modern RDKit this might be different
        dopts.bondLineWidth = 10.0
        dopts.setBackgroundColour((1, 1, 1, 0))
        dopts.updateAtomPalette({9: (0.7, 0, 0.7)})
        # dopts.legendFraction = 5
        dopts.legendFontSize = 35
        d2d.DrawMolecule(mol)  # legend = self.smiles)
        d2d.FinishDrawing()
        text1 = d2d.GetDrawingText()

        self.img = self.remove_whitespace(text1)

        common_features = [
            "SlogP_VSA10",
            "SMR_VSA5",
            "SMR_VSA7",
            "HallKierAlpha",
            "MinEStateIndex",
            "VSA_EState4",
            "MinPartialCharge",
            "VSA_EState8",
            "PEOE_VSA13",
            "MaxAbsEStateIndex",
            "PEOE_VSA10",
            "SlogP_VSA1",
            "SMR_VSA10",
            "VSA_EState6",
            "PEOE_VSA9",
            "MaxPartialCharge",
            "PEOE_VSA1",
            "EState_VSA10",
            "SlogP_VSA2",
            "PEOE_VSA3",
            "NHOHCount",
            "EState_VSA8",
            "SMR_VSA3",
            "VSA_EState2",
            "BalabanJ",
            "TPSA",
            "NumHeteroatoms",
            "NumRotatableBonds",
            "MinAbsEStateIndex",
            "fr_amide",
            "qed",
            "SMR_VSA6",
        ]

        self.features_delg = self.calc_descriptors(self.smiles, features=common_features)

        common_features = [
            "PEOE_VSA9",
            "SlogP_VSA12",
            "SPS",
            "MolWt",
            "MinPartialCharge",
            "VSA_EState5",
            "MaxAbsEStateIndex",
            "Kappa1",
            "qed",
            "PEOE_VSA12",
            "PEOE_VSA3",
            "BalabanJ",
            "EState_VSA10",
            "SlogP_VSA8",
            "fr_halogen",
            "SMR_VSA6",
            "SlogP_VSA4",
            "PEOE_VSA8",
            "Kappa3",
            "EState_VSA2",
            "VSA_EState3",
            "EState_VSA9",
            "SlogP_VSA2",
            "SlogP_VSA7",
            "HallKierAlpha",
            "MolLogP",
            "fr_phos_acid",
            "NumRadicalElectrons",
            "PEOE_VSA14",
            "NHOHCount",
            "SMR_VSA4",
            "SlogP_VSA10",
            "PEOE_VSA4",
            "SMR_VSA5",
            "fr_Ar_NH",
            "PEOE_VSA13",
            "AvgIpc",
            "PEOE_VSA7",
            "SMR_VSA10",
            "MinAbsEStateIndex",
            "VSA_EState8",
            "SlogP_VSA1",
            "VSA_EState2",
            "SlogP_VSA3",
            "Kappa2",
            "VSA_EState4",
            "PEOE_VSA1",
            "MinAbsPartialCharge",
            "PEOE_VSA2",
            "TPSA",
            "SMR_VSA3",
            "PEOE_VSA10",
            "MinEStateIndex",
            "FpDensityMorgan1",
            "VSA_EState9",
            "EState_VSA8",
            "SMR_VSA7",
            "fr_ester",
            "SMR_VSA2",
            "FractionCSP3",
            "PEOE_VSA11",
            "VSA_EState6",
            "PEOE_VSA6",
        ]
        self.features_solu = self.calc_descriptors(self.smiles, features=common_features)

        common_features = [
            "fr_COO",
            "SlogP_VSA3",
            "PEOE_VSA8",
            "fr_ArN",
            "MinEStateIndex",
            "PEOE_VSA4",
            "fr_lactone",
            "fr_bicyclic",
            "fr_hdrzine",
            "SlogP_VSA12",
            "fr_halogen",
            "fr_aniline",
            "fr_lactam",
            "PEOE_VSA12",
            "VSA_EState7",
            "MinAbsEStateIndex",
            "VSA_EState8",
            "SlogP_VSA8",
            "PEOE_VSA3",
            "PEOE_VSA5",
            "SMR_VSA4",
            "SMR_VSA6",
            "SMR_VSA3",
            "SMR_VSA5",
            "fr_pyridine",
            "PEOE_VSA11",
            "VSA_EState5",
            "TPSA",
            "VSA_EState10",
            "fr_NH0",
            "PEOE_VSA7",
            "SMR_VSA9",
            "SlogP_VSA4",
            "PEOE_VSA10",
            "SlogP_VSA7",
            "fr_Al_OH",
            "fr_amide",
            "fr_amidine",
            "NumAromaticHeterocycles",
            "fr_guanido",
            "VSA_EState3",
            "SlogP_VSA1",
            "FractionCSP3",
            "VSA_EState6",
            "VSA_EState2",
            "NHOHCount",
            "SlogP_VSA2",
            "Ipc",
            "EState_VSA10",
            "MinAbsPartialCharge",
            "PEOE_VSA14",
            "EState_VSA8",
            "fr_ketone",
            "SMR_VSA10",
            "fr_C_S",
            "PEOE_VSA9",
            "fr_allylic_oxid",
            "Kappa3",
            "PEOE_VSA1",
            "fr_NH1",
            "fr_Ar_N",
            "MinPartialCharge",
            "SlogP_VSA10",
            "HallKierAlpha",
            "SMR_VSA2",
            "VSA_EState9",
        ]

        self.features_pka = self.calc_descriptors(self.smiles, features=common_features)

        # print(self.features_pka)

    def prediction(self):
        """
        Predicts the DeltaGsolv, solubility, and pKa values using machine learning models.
        """

        ### Predicted DeltaGsolv..
        self.xgb_predict_delg = self.delg_xgb_model.predict(self.features_delg)["predicted_DeltaGsolv"]
        self.rfr_predict_delg = self.predict_from_joblib(self.delg_rfr_path, self.features_delg)
        self.svr_predict_delg = self.predict_from_joblib(self.delg_svr_path, self.features_delg)
        self.gpr_predict_delg = self.predict_from_joblib(self.delg_gpr_path, self.features_delg)
        self.krr_predict_delg = self.predict_from_joblib(self.delg_krr_path, self.features_delg)

        self.xgb_predict_solu = self.solu_xgb_model.predict(self.features_solu)["predicted_y"]
        self.rfr_predict_solu = self.predict_from_joblib(self.solu_rfr_path, self.features_solu)
        self.svr_predict_solu = self.predict_from_joblib(self.solu_svr_path, self.features_solu)
        self.gpr_predict_solu = self.predict_from_joblib(self.solu_gpr_path, self.features_solu)
        self.krr_predict_solu = self.predict_from_joblib(self.solu_krr_path, self.features_solu)

        self.xgb_predict_pka = self.pka_xgb_model.predict(self.features_pka)["predicted_y"]
        self.rfr_predict_pka = self.predict_from_joblib(self.pka_rfr_path, self.features_pka)
        self.svr_predict_pka = self.predict_from_joblib(self.pka_svr_path, self.features_pka)
        self.gpr_predict_pka = self.predict_from_joblib(self.pka_gpr_path, self.features_pka)
        self.krr_predict_pka = self.predict_from_joblib(self.pka_krr_path, self.features_pka)

    def availibility(self):
        """
        Check the availability of the molecule's properties in the provided datasets.

        Parameters:
        None

        Returns:
        None

        This function reads the datasets containing the properties of molecules,
        then checks if the molecule's cannonized SMILES is present in the datasets.
        If present, it assigns the corresponding property values to the instance variables.
        """
        base_path = settings.BASE_DIR
        full_delg_df = pd.read_csv(os.path.join(base_path, "pharmocast/assets/full.csv"), delimiter=";")
        full_solu_df = pd.read_csv(os.path.join(base_path, "pharmocast/assets/solubility_data.csv"))
        full_pka_df = pd.read_csv(os.path.join(base_path, "pharmocast/assets/pka_data.csv"))

        # Check for DeltaGsolv availability
        match_delg = full_delg_df[full_delg_df["cannon_smiles"] == Chem.CanonSmiles(self.smiles)]
        if len(match_delg["DeltaGsolv"].values):
            self.delg = np.round(match_delg["DeltaGsolv"].values[0], 3)

        # Check for Solubility availability
        match_solu = full_solu_df[full_solu_df["SMILES"] == Chem.CanonSmiles(self.smiles)]
        if len(match_solu["Solubility"].values):
            self.solu = np.round(match_solu["Solubility"].values[0], 3)

        # Check for pKa availability
        match_pka = full_pka_df[full_pka_df["SMILES"] == Chem.CanonSmiles(self.smiles)]
        if len(match_pka["pKa"].values):
            self.pka = np.round(match_pka["pKa"].values[0], 3)

    # remove whitespace from text
    def remove_whitespace(self, text):
        """
        Remove whitespace from the given text.

        Parameters:
        text (str): The input text with whitespace.

        Returns:
        str: The text without any whitespace.

        This function splits the input text into a list of words using the split() method,
        then joins the words back together without any whitespace using the join() method.
        """
        return " ".join(text.split())

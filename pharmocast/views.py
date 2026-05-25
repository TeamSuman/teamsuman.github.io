# import html
# from time import sleep

# import joblib  # type: ignore
try:
    import numpy as np
except ModuleNotFoundError:
    np = None

# from .forms import ContactForm
from django.http import JsonResponse  # type: ignore
from django.shortcuts import render  # type: ignore
from django.templatetags.static import static

from .classes import OPTIONAL_DEPENDENCY_ERROR, molproperties

fail_emoji = """<svg viewBox="0 0 170 170" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" fill="#ffdd67" r="30"/><path d="m40.6 46.4c-5.4-2.5-11.8-2.5-17.2 0-1.3.6.3 4.2 1.7 3.5 3.6-1.7 8.9-2.3 13.9 0 1.3.6 3-2.8 1.6-3.5" fill="#664e27"/><path d="m54 31c0 5-4 9-9 9s-9-4-9-9 4-9 9-9 9 4 9 9" fill="#fff"/><circle cx="45" cy="31" fill="#664e27" r="6"/><g fill="#fff"><ellipse cx="46.6" cy="35.5" rx="2.8" ry="3.2"/><ellipse cx="42.8" cy="31" rx="1.6" ry="1.9"/><path d="m28 31c0 5-4 9-9 9s-9-4-9-9 4-9 9-9 9 4 9 9"/></g><circle cx="19" cy="31" fill="#664e27" r="6"/><g fill="#fff"><ellipse cx="20.6" cy="35.5" rx="2.8" ry="3.2"/><ellipse cx="16.8" cy="31" rx="1.6" ry="1.9"/></g><path d="m47 36c-5.1 6.8-8 13-8 18.1 0 4.4 3.6 7.9 8 7.9s8-3.5 8-7.9c0-5.1-3-11.4-8-18.1" fill="#65b1ef"/><path d="m53.2 20.7c-3.2-2.7-7.5-3.9-11.7-3.1-.6.1-1.1-2-.4-2.2 4.8-.9 9.8.5 13.5 3.6.6.5-1 2.1-1.4 1.7m-30.7-3.3c-4.2-.7-8.5.4-11.7 3.1-.4.4-2-1.2-1.4-1.7 3.7-3.2 8.7-4.5 13.5-3.6.7.2.2 2.3-.4 2.2" fill="#917524"/></svg>"""


def home(request):
    return render(request, "home/pharmocast.html")


def _round(value, ndigits=3):
    if np is not None:
        return np.round(value, ndigits)
    return round(float(value), ndigits)


# TODO Rename this here and in `home`
def _extracted_from_home_8(mp, arg1):
    mp.calc()
    mp.prediction()
    mp.valid = arg1


def test(request):
    return render(request, "home/test.html")


def contact(request):
    data = request.POST
    # print(data)
    smiles = None

    if OPTIONAL_DEPENDENCY_ERROR is not None:
        if "name" in data.keys() and len(data["name"]):
            smiles = "".join(data["name"].split(" "))
        return JsonResponse(
            {
                "status": "error",
                "smiles": str(smiles),
                "valid": "False",
                "img": fail_emoji,
                "invalidImage": static("invalid.jpg"),
                "message": f"Pharmocast dependency is not installed: {OPTIONAL_DEPENDENCY_ERROR.name}",
            },
            status=503,
        )

    if "name" in data.keys():
        if len(data["name"]):
            try:
                smiles = data["name"]
                smiles = "".join(smiles.split(" "))
                # TODO: Better way to parse input values
                mp = molproperties(smiles)
                _extracted_from_home_8(mp, "Valid")
                mp.availibility()
            except Exception:
                smiles = "C"
                mp = molproperties(smiles)
                _extracted_from_home_8(mp, "Invalid")
                mp.img = fail_emoji
        else:
            mp = molproperties("C")
            mp.valid = "False"
    else:
        mp = molproperties("C")
        mp.valid = "False"

    validity = mp.valid
    print(mp.valid)
    img = mp.img
    invalidImage = static("invalid.jpg")
    try:
        dgsolv = mp.delg
    except Exception:
        dgsolv = "-"
    try:
        pka = mp.pka
    except Exception:
        pka = "-"
    try:
        solu = mp.solu
    except Exception:
        solu = "-"
    ## Predicted mol properties
    gbr_solu = _round(mp.xgb_predict_solu, 3)
    gbr_pka = _round(mp.xgb_predict_pka, 3)
    gbr_delg = _round(mp.xgb_predict_delg, 3)

    gpr_solu = _round(mp.gpr_predict_solu, 3)
    gpr_pka = _round(mp.gpr_predict_pka, 3)
    gpr_delg = _round(mp.gpr_predict_delg, 3)

    svr_solu = _round(mp.svr_predict_solu, 3)
    svr_pka = _round(mp.svr_predict_pka, 3)
    svr_delg = _round(mp.svr_predict_delg, 3)

    krr_solu = _round(mp.krr_predict_solu, 3)
    krr_pka = _round(mp.krr_predict_pka, 3)
    krr_delg = _round(mp.krr_predict_delg, 3)

    rfr_solu = _round(mp.rfr_predict_solu, 3)
    rfr_pka = _round(mp.rfr_predict_pka, 3)
    rfr_delg = _round(mp.rfr_predict_delg, 3)

    ## Calculated values
    exactmw = _round(mp.features_solu["MolWt"], 3)
    num_o = _round(mp.features_delg["BalabanJ"], 3)
    tpsa = _round(mp.features_delg["TPSA"], 3)
    crplog = _round(mp.features_solu["MolLogP"], 3)
    frcsp3 = _round(mp.features_solu["FractionCSP3"], 3)
    num_amide = mp.features_delg["fr_amide"]
    num_rings = mp.features_delg["NumRotatableBonds"]
    lipinskihbd = _round(mp.features_delg["qed"], 3)

    return JsonResponse(
        {
            "status": "success",
            "smiles": str(smiles),
            "valid": str(validity),
            "img": img,
            "invalidImage": invalidImage,
            "dgsolv": dgsolv,
            "pka": pka,
            "solu": solu,
            "gbr_delg": gbr_delg,
            "gpr_delg": gpr_delg,
            "rfr_delg": rfr_delg,
            "krr_delg": krr_delg,
            "svr_delg": svr_delg,
            "gbr_pka": gbr_pka,
            "rfr_pka": rfr_pka,
            "svr_pka": svr_pka,
            "krr_pka": krr_pka,
            "gpr_pka": gpr_pka,
            "gbr_solu": gbr_solu,
            "rfr_solu": rfr_solu,
            "gpr_solu": gpr_solu,
            "krr_solu": krr_solu,
            "svr_solu": svr_solu,
            "exactmw": exactmw,
            "num_o": num_o,
            "tpsa": tpsa,
            "crplog": crplog,
            "frcsp3": frcsp3,
            "num_amide": num_amide,
            "num_rings": num_rings,
            "lipinskihbd": lipinskihbd,
        }
    )

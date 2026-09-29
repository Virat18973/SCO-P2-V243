import optimizer as opt


def load_master(uploaded_file):
    """Load a Streamlit UploadedFile through the backend loader.

    The backend loader matches the worksheet by column headers (not by name), treats
    Tech_Min_kg_t / Tech_Max_kg_t / Fines_% / CV_kcal_kg / FC_Pct / Material_Role as
    optional, and reads blank Tech limits as "no limit".
    """
    if uploaded_file is None:
        raise ValueError("No Excel file supplied.")
    df = opt.load_master_chemistry_excel({uploaded_file.name: uploaded_file.getvalue()})
    return opt._ensure_material_role(df)
